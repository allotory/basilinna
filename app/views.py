# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Ellery'

from flask import Flask, render_template, request, session, abort, redirect, url_for, make_response
from sqlalchemy import and_, func
from app import app, models, csrf
from app.main import valid_account, encryption, invitation, db_service, upload_file
from datetime import datetime
import json, os
from werkzeug import secure_filename

# register page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        # show the signup form
        return render_template('signup.html')
    elif request.method == 'POST':
        # do the signup
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # whether the email address is exist
        is_exist = valid_account.valid_email_exist(email)
        if is_exist:
            return render_template('signup.html', 
                error_message='该email地址已被注册',
                signup_form=request.form)
        else:
            if password != confirm_password:
                return render_template('signup.html', 
                    error_message='两次密码输入不一致',
                    signup_form=request.form)

            # encryption password
            new_password, salt = encryption.encrypt_pass_salt(password)

            # ip address
            ip = request.remote_addr

            # Invitation link
            invite_string = invitation.invite_url()
            invite_link = app.config.get('HOST') + invite_string

            # initial user and member db data
            u = models.User(email=email, password=new_password, salt=salt,
                create_time=str(datetime.now()), last_login_time=str(datetime.now()),
                last_login_ip=ip, status=1, remark='user', invent=invite_link)
            db_service.db_insert(u)
            db_service.db_commit()
            
            avatar_path = 'image/avatar/avatar.jpg'
            m = models.Member(fullname=nickname, gender=None, avatar_path=avatar_path,
                year=None, month=None, day=None,
                location_province=None, location_city=None, location_area=None, 
                hometown_province=None, hometown_city=None, hometown_area=None, 
                description=None, autograph=None,
                personality_url=invite_string, is_email_actived=None, user_id=u.id)
            db_service.db_insert(m)
            db_service.db_commit()

            return redirect(url_for('login', info='注册成功，请先登录'))
    else:
        pass


# login page
@app.route('/login', methods = ['GET', 'POST'])
@app.route('/login/<info>', methods = ['GET', 'POST'])
def login(info=None):
    if request.method == 'POST':
        # do the login
        email = request.form.get('email')
        password = request.form.get('password')
        rememberme = request.form.get('rememberme')

        # encrypt password with salt
        u = models.User.query.filter_by(email=email).first()
        
        # email not exist
        if u is None:
            return render_template('login.html', error_message='当前邮件账户不存在')

        new_pass = encryption.encrypt_pass(password, u.salt)
        if u.password != new_pass:
            return render_template('login.html', error_message='邮件地址或密码错误')

        # render index page with data
        m = models.Member.query.filter_by(user_id=u.id).first()
        session['member_id'] = m.id

        # set cookie
        response = make_response(redirect(url_for('index')))
        if rememberme:
            response.set_cookie('email', email)
            response.set_cookie('password', password)
        else:
            response.delete_cookie('email')
            response.delete_cookie('password')
        return response
    else:
        # show the login form
        email = request.cookies.get('email')
        password = request.cookies.get('password')
        return render_template('login.html', info=info, email=email, password=password)


# index page
@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
def index(page = 1):
    if 'member_id' in session:
        member_id = session['member_id']
        m = models.Member.query.filter_by(id=member_id).first()
        if m is None:
            redirect(url_for('error'))

        # followee id list
        followees = models.Relation.query.filter(models.Relation.member_id == m.id).all()
        relation_list = [x.followee_id for x in followees]
        relation_list.append(m.id)

        # blog detail
        blog_list_paginate = models.Blog.query.filter(models.Blog.member_id.in_(relation_list)).order_by(models.Blog.id.desc()).paginate(page, app.config.get('POSTS_PER_PAGE'), True)
        blog_list = blog_list_paginate.items

        # paginate
        has_prev = blog_list_paginate.has_prev
        has_next = blog_list_paginate.has_next
        prev_num = blog_list_paginate.prev_num
        next_num = blog_list_paginate.next_num

        blog_info_list = []

        # blog collected
        for blog in blog_list:
            # whether or not collected
            c = models.Collection.query.filter(and_(models.Collection.member_id==member_id, models.Collection.blog_id==blog.id)).first()
            if c is None:
                blog_dict = dict(blog=blog, collection='uncollect')
            else:
                blog_dict = dict(blog=blog, collection='collecting')

            origin_pic_path = blog.pic_path
            if blog.exist_pic != 0:
                origin_pic_path = blog.pic_path.replace('_thumbnail', '')
                blog_dict['origin_pic_path'] = origin_pic_path

            # current blog author
            blog_author = models.Member.query.filter_by(id=blog.member_id).first()
            blog_dict['blog_member'] = blog_author

            # a blog repeat list
            re_list = []

            if blog.post_type == 'REPEAT':
                re_from = None
                re_member_id = None
                
                re_blog = models.Blog.query.filter_by(id=blog.re_from).first()
                re_member = models.Member.query.filter_by(id=blog.re_member_id).first()
                re_origin_pic_path = re_blog.pic_path
                if re_blog.exist_pic != 0:
                    re_origin_pic_path = re_blog.pic_path.replace('_thumbnail', '')

                re_list.append(dict(blog=re_blog, blog_member=re_member, re_origin_pic_path=re_origin_pic_path))

                re_from = re_blog.re_from    
                re_member_id = re_blog.re_member_id

                # exist reblog
                while re_from :
                    re_blog_t = models.Blog.query.filter_by(id=re_from).first()
                    re_member_t = models.Member.query.filter_by(id=re_member_id).first()
                    re_list.append(dict(blog=re_blog_t, blog_member=re_member_t))
                    
                    re_from = re_blog_t.re_from
                    re_member_id = re_blog_t.re_member_id

                blog_dict['re_list'] = re_list

            blog_info_list.append(blog_dict)

        # follow detail
        following_count = models.Relation.query.filter(models.Relation.member_id == m.id).count()
        session['following_count'] = following_count

        fans_count = models.Relation.query.filter(models.Relation.followee_id == m.id).count()
        session['fans_count'] = fans_count

        # blog count 
        blog_count = models.Blog.query.filter(models.Blog.member_id == m.id).count()
        session['blog_count'] = blog_count

        # friends list
        followees = models.Relation.query.filter(models.Relation.member_id == m.id).limit(8).all()
        followee_list = []
        if followees :
            for followee in followees:
                followee_info = models.Member.query.filter(models.Member.id == followee.followee_id).first()
                followee_list.append(followee_info)

        return render_template('index.html', member=m, blog_list=blog_info_list, 
            following_count=following_count, fans_count=fans_count, 
            blog_count = blog_count, followee_list=followee_list, has_prev=has_prev,
            has_next=has_next, prev_num=prev_num, next_num=next_num)

    return redirect(url_for('login', info='访问当前内容，请先登录'))


# post blog
@app.route('/post', methods = ['POST'])
def post():
    member_id = session['member_id']

    # get blog content from ajax data
    data = json.loads(request.form.get('data'))
    content = data['content']
    re_from = int(data['re_from'])
    re_member_id = int(data['re_member_id'])
    post_type = data['post_type']
    file_name = data['file_name']

    if re_from == 0:
        re_from = None
    if re_member_id == 0:
        re_member_id = None

    exist_pic = 0
    pic_path = None
    if file_name and file_name != "":
        exist_pic = 1
        # pic_path = os.path.join('../static/uploads', (os.path.splitext(file_name)[0] + '_thumbnail' + os.path.splitext(file_name)[1]))
        pic_path = 'uploads/' + os.path.splitext(file_name)[0] + '_thumbnail' + os.path.splitext(file_name)[1]

    # insert blog
    b = models.Blog(content=content, create_time=str(datetime.now()),
        post_type=post_type, via='Web', exist_pic=exist_pic, pic_path=pic_path,
        location=None, member_id=member_id, re_from=re_from, re_member_id=re_member_id)
    db_service.db_insert(b)
    db_service.db_commit()

    origin_pic_path = os.path.join('uploads', file_name)

    # build a blog dict for json
    blog_dict = dict(id=b.id, content=b.content, create_time=str(b.create_time),
        post_type=b.post_type, exist_pic=b.exist_pic, pic_path=b.pic_path,
        origin_pic_path=origin_pic_path, via=b.via)
    temp = json.dumps(blog_dict)

    return temp


# space page
@app.route('/space', methods = ['GET'])
@app.route('/space/<url>', methods = ['GET'])
@app.route('/space/<int:page>', methods = ['GET', 'POST'])
@app.route('/space/<url>/<int:page>', methods = ['GET', 'POST'])
def space(url = None, page = 1):
    if request.method == 'GET':
        # current member
        member_id = session['member_id']
        m = models.Member.query.filter_by(id=member_id).first()
        if m is None:
            redirect(url_for('error'))

        if url:
            if url != m.personality_url:
                # selected member space
                selected_member = models.Member.query.filter_by(personality_url=url).first()
                blog_list_paginate = models.Blog.query.filter_by(member_id=selected_member.id).order_by(models.Blog.id.desc()).paginate(page, app.config.get('POSTS_PER_PAGE'), True)
                blog_list = blog_list_paginate.items

                # paginate
                has_prev = blog_list_paginate.has_prev
                has_next = blog_list_paginate.has_next
                prev_num = blog_list_paginate.prev_num
                next_num = blog_list_paginate.next_num

                blog_info_list = []

                # blog collected
                for blog in blog_list:
                    c = models.Collection.query.filter(and_(models.Collection.member_id==m.id, models.Collection.blog_id==blog.id)).first()
                    if c is None:
                        blog_dict = dict(blog=blog, collection='uncollect', blog_member=selected_member)
                    else:
                        blog_dict = dict(blog=blog, collection='collecting', blog_member=selected_member)

                    origin_pic_path = blog.pic_path
                    if blog.exist_pic != 0:
                        origin_pic_path = blog.pic_path.replace('_thumbnail', '')
                        blog_dict['origin_pic_path'] = origin_pic_path

                    # a blog repeat list
                    re_list = []

                    if blog.post_type == 'REPEAT':
                        re_from = None
                        re_member_id = None
                        
                        re_blog = models.Blog.query.filter_by(id=blog.re_from).first()
                        re_member = models.Member.query.filter_by(id=blog.re_member_id).first()
                        re_origin_pic_path = re_blog.pic_path
                        if re_blog.exist_pic != 0:
                            re_origin_pic_path = re_blog.pic_path.replace('_thumbnail', '')
                        re_list.append(dict(blog=re_blog, blog_member=re_member, re_origin_pic_path=re_origin_pic_path))

                        re_from = re_blog.re_from    
                        re_member_id = re_blog.re_member_id

                        # exist reblog
                        while re_from :
                            re_blog_t = models.Blog.query.filter_by(id=re_from).first()
                            re_member_t = models.Member.query.filter_by(id=re_member_id).first()
                            re_list.append(dict(blog=re_blog_t, blog_member=re_member_t))
                            
                            re_from = re_blog_t.re_from
                            re_member_id = re_blog_t.re_member_id

                        blog_dict['re_list'] = re_list

                    blog_info_list.append(blog_dict)

                # follow detail
                following_count = models.Relation.query.filter(models.Relation.member_id == selected_member.id).count()
                fans_count = models.Relation.query.filter(models.Relation.followee_id == selected_member.id).count()

                # blog count 
                blog_count = models.Blog.query.filter(models.Blog.member_id == selected_member.id).count()
                
                return render_template('space.html', member=selected_member, blog_list=blog_info_list, 
                    following_count=following_count, fans_count=fans_count, not_me=True, blog_count=blog_count, 
                    has_prev=has_prev, has_next=has_next, prev_num=prev_num, next_num=next_num, url=url)
            else :
                # my space
                blog_list_paginate = models.Blog.query.filter_by(member_id=member_id).order_by(models.Blog.id.desc()).paginate(page, app.config.get('POSTS_PER_PAGE'), True)
                blog_list = blog_list_paginate.items

                # paginate
                has_prev = blog_list_paginate.has_prev
                has_next = blog_list_paginate.has_next
                prev_num = blog_list_paginate.prev_num
                next_num = blog_list_paginate.next_num
                
                blog_info_list = []

                # blog collected
                for blog in blog_list:
                    c = models.Collection.query.filter(and_(models.Collection.member_id==member_id, models.Collection.blog_id==blog.id)).first()
                    if c is None:
                        blog_dict = dict(blog=blog, collection='uncollect', blog_member=m)
                    else:
                        blog_dict = dict(blog=blog, collection='collecting', blog_member=m)

                    origin_pic_path = blog.pic_path
                    if blog.exist_pic != 0:
                        origin_pic_path = blog.pic_path.replace('_thumbnail', '')
                        blog_dict['origin_pic_path'] = origin_pic_path

                    # a blog repeat list
                    re_list = []

                    if blog.post_type == 'REPEAT':
                        re_from = None
                        re_member_id = None
                        
                        re_blog = models.Blog.query.filter_by(id=blog.re_from).first()
                        re_member = models.Member.query.filter_by(id=blog.re_member_id).first()
                        re_origin_pic_path = re_blog.pic_path
                        if re_blog.exist_pic != 0:
                            re_origin_pic_path = re_blog.pic_path.replace('_thumbnail', '')
                        re_list.append(dict(blog=re_blog, blog_member=re_member, re_origin_pic_path=re_origin_pic_path))

                        re_from = re_blog.re_from    
                        re_member_id = re_blog.re_member_id

                        # exist reblog
                        while re_from :
                            re_blog_t = models.Blog.query.filter_by(id=re_from).first()
                            re_member_t = models.Member.query.filter_by(id=re_member_id).first()
                            re_list.append(dict(blog=re_blog_t, blog_member=re_member_t))
                            
                            re_from = re_blog_t.re_from
                            re_member_id = re_blog_t.re_member_id

                        blog_dict['re_list'] = re_list

                    blog_info_list.append(blog_dict)

                # follow detail
                following_count = models.Relation.query.filter(models.Relation.member_id == m.id).count()
                fans_count = models.Relation.query.filter(models.Relation.followee_id == m.id).count()

                # blog count 
                blog_count = models.Blog.query.filter(models.Blog.member_id == m.id).count()
                
                return render_template('space.html', member=m, blog_list=blog_info_list, 
                    following_count=following_count, fans_count=fans_count, blog_count = blog_count, 
                    has_prev=has_prev, has_next=has_next, prev_num=prev_num, next_num=next_num, url=url)
        else:
            # my space
            blog_list_paginate = models.Blog.query.filter_by(member_id=member_id).order_by(models.Blog.id.desc()).paginate(page, app.config.get('POSTS_PER_PAGE'), True)
            blog_list = blog_list_paginate.items

            # paginate
            has_prev = blog_list_paginate.has_prev
            has_next = blog_list_paginate.has_next
            prev_num = blog_list_paginate.prev_num
            next_num = blog_list_paginate.next_num

            blog_info_list = []

            # blog collected
            for blog in blog_list:
                c = models.Collection.query.filter(and_(models.Collection.member_id==member_id, models.Collection.blog_id==blog.id)).first()
                if c is None:
                    blog_dict = dict(blog=blog, collection='uncollect', blog_member=m)
                else:
                    blog_dict = dict(blog=blog, collection='collecting', blog_member=m)

                origin_pic_path = blog.pic_path
                if blog.exist_pic != 0:
                    origin_pic_path = blog.pic_path.replace('_thumbnail', '')
                    blog_dict['origin_pic_path'] = origin_pic_path

                # a blog repeat list
                re_list = []

                if blog.post_type == 'REPEAT':
                    re_from = None
                    re_member_id = None
                    
                    re_blog = models.Blog.query.filter_by(id=blog.re_from).first()
                    re_member = models.Member.query.filter_by(id=blog.re_member_id).first()
                    re_origin_pic_path = re_blog.pic_path
                    if re_blog.exist_pic != 0:
                        re_origin_pic_path = re_blog.pic_path.replace('_thumbnail', '')
                    re_list.append(dict(blog=re_blog, blog_member=re_member, re_origin_pic_path=re_origin_pic_path))

                    re_from = re_blog.re_from    
                    re_member_id = re_blog.re_member_id

                    # exist reblog
                    while re_from :
                        re_blog_t = models.Blog.query.filter_by(id=re_from).first()
                        re_member_t = models.Member.query.filter_by(id=re_member_id).first()
                        re_list.append(dict(blog=re_blog_t, blog_member=re_member_t))
                        
                        re_from = re_blog_t.re_from
                        re_member_id = re_blog_t.re_member_id

                    blog_dict['re_list'] = re_list

                blog_info_list.append(blog_dict)

            # follow detail
            following_count = models.Relation.query.filter(models.Relation.member_id == m.id).count()
            fans_count = models.Relation.query.filter(models.Relation.followee_id == m.id).count()

            # blog count 
            blog_count = models.Blog.query.filter(models.Blog.member_id == m.id).count()

            return render_template('space.html', member=m, blog_list=blog_info_list, 
                following_count=following_count, fans_count=fans_count, blog_count = blog_count, 
                    has_prev=has_prev, has_next=has_next, prev_num=prev_num, next_num=next_num)

        return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


# follow people
@app.route('/follow', methods = ['POST'])
def follow():
    if request.method == 'POST':
        member_id = session['member_id']

        # # get followee id from ajax data
        data = json.loads(request.form.get('data'))
        followee_id = data['followee_id']

        # insert relation
        r = models.Relation(member_id=member_id, followee_id=followee_id)
        db_service.db_insert(r)
        db_service.db_commit()

        return 'followsuccess'
    else:
        return redirect(url_for('error'))


# unfollow people
@app.route('/unfollow', methods = ['POST'])
def unfollow():
    if request.method == 'POST':
        member_id = session['member_id']

        # # get followee id from ajax data
        data = json.loads(request.form.get('data'))
        followee_id = data['followee_id']

        # delete relation
        r = models.Relation.query.filter(and_(models.Relation.member_id==member_id, models.Relation.followee_id==followee_id)).first()
        if r is None:
            redirect(url_for('error'))
        db_service.db_delete(r)
        db_service.db_commit()

        return 'unfollowsuccess'
    else:
        return redirect(url_for('error'))


# blog collect
@app.route('/collect', methods = ['POST'])
def collect():
    if request.method == 'POST':
        member_id = session['member_id']

        # get blog id
        data = json.loads(request.form.get('data'))
        blog_id = data['blog_id']

        # insert collection
        c = models.Collection(blog_id=blog_id, member_id=member_id)
        db_service.db_insert(c)
        db_service.db_commit()

        return 'collectsuccess'
    else:
        return redirect(url_for('error'))


# blog uncollect
@app.route('/uncollect', methods = ['POST'])
def uncollect():
    if request.method == 'POST':
        member_id = session['member_id']

        # get blog id
        data = json.loads(request.form.get('data'))
        blog_id = data['blog_id']

        # delete collection
        c = models.Collection.query.filter(and_(models.Collection.member_id==member_id, models.Collection.blog_id==blog_id)).first()
        if c is None:
            redirect(url_for('error'))
        db_service.db_delete(c)
        db_service.db_commit()

        return 'uncollectsuccess'
    else:
        return redirect(url_for('error'))

# blog collections
@app.route('/collections', methods = ['GET'])
@app.route('/collections/<url>', methods = ['GET'])
@app.route('/collections/<int:page>', methods = ['GET', 'POST'])
@app.route('/collections/<url>/<int:page>', methods = ['GET', 'POST'])
def collections(url=None, page=1):
    if request.method == 'GET':

        member_id = session['member_id']
        m = models.Member.query.filter_by(id=member_id).first()
        if m is None:
            redirect(url_for('error'))

        if url and url != m.personality_url:
            # selected collections
            # collections detail
            selected_member = models.Member.query.filter_by(personality_url=url).first()
            collection_list_paginate = models.Collection.query.filter_by(member_id=selected_member.id).order_by(models.Collection.id.desc()).paginate(page, app.config.get('POSTS_PER_PAGE'), True)
            collection_list = collection_list_paginate.items

            # paginate
            has_prev = collection_list_paginate.has_prev
            has_next = collection_list_paginate.has_next
            prev_num = collection_list_paginate.prev_num
            next_num = collection_list_paginate.next_num


            blog_info_list = []

            # blog collected
            for collection in collection_list:
                blog = models.Blog.query.filter_by(id=collection.blog_id).first()
                
                # blog author
                collect_member = None
                if blog.member_id != m.id:
                    # not mine
                    collect_member = models.Member.query.filter_by(id=blog.member_id).first()
                else:
                    collect_member = m
                blog_dict = dict(blog=blog, collection='collecting', collect_member=collect_member)

                origin_pic_path = blog.pic_path
                if blog.exist_pic != 0:
                    origin_pic_path = blog.pic_path.replace('_thumbnail', '')
                    blog_dict['origin_pic_path'] = origin_pic_path

                # a blog repeat list
                re_list = []

                if blog.post_type == 'REPEAT':
                    re_from = None
                    re_member_id = None
                    
                    re_blog = models.Blog.query.filter_by(id=blog.re_from).first()
                    re_member = models.Member.query.filter_by(id=blog.re_member_id).first()
                    re_origin_pic_path = re_blog.pic_path
                    if re_blog.exist_pic != 0:
                        re_origin_pic_path = re_blog.pic_path.replace('_thumbnail', '')
                    re_list.append(dict(blog=re_blog, blog_member=re_member, re_origin_pic_path=re_origin_pic_path))

                    re_from = re_blog.re_from    
                    re_member_id = re_blog.re_member_id

                    # exist reblog
                    while re_from :
                        re_blog_t = models.Blog.query.filter_by(id=re_from).first()
                        re_member_t = models.Member.query.filter_by(id=re_member_id).first()
                        re_list.append(dict(blog=re_blog_t, blog_member=re_member_t))
                        
                        re_from = re_blog_t.re_from
                        re_member_id = re_blog_t.re_member_id

                    blog_dict['re_list'] = re_list

                blog_info_list.append(blog_dict)

            # follow detail
            following_count = models.Relation.query.filter(models.Relation.member_id == selected_member.id).count()
            fans_count = models.Relation.query.filter(models.Relation.followee_id == selected_member.id).count()

            # blog count 
            blog_count = models.Blog.query.filter(models.Blog.member_id == selected_member.id).count()

            return render_template('collections.html', member=selected_member, blog_list=blog_info_list, 
                following_count=following_count, fans_count=fans_count, not_me=True, blog_count = blog_count,
                has_prev=has_prev, has_next=has_next, prev_num=prev_num, next_num=next_num, url=url)
    
        else:
            # my collections
            # collections detail
            collection_list_paginate = models.Collection.query.filter_by(member_id=member_id).order_by(models.Collection.id.desc()).paginate(page, app.config.get('POSTS_PER_PAGE'), True)
            collection_list = collection_list_paginate.items

            # paginate
            has_prev = collection_list_paginate.has_prev
            has_next = collection_list_paginate.has_next
            prev_num = collection_list_paginate.prev_num
            next_num = collection_list_paginate.next_num

            blog_info_list = []

            # blog collected
            for collection in collection_list:
                blog = models.Blog.query.filter_by(id=collection.blog_id).first()
                
                # blog author
                collect_member = None
                if blog.member_id != m.id:
                    # not mine
                    collect_member = models.Member.query.filter_by(id=blog.member_id).first()
                else:
                    collect_member = m
                blog_dict = dict(blog=blog, collection='collecting', collect_member=collect_member)

                origin_pic_path = blog.pic_path
                if blog.exist_pic != 0:
                    origin_pic_path = blog.pic_path.replace('_thumbnail', '')
                    blog_dict['origin_pic_path'] = origin_pic_path

                # a blog repeat list
                re_list = []

                if blog.post_type == 'REPEAT':
                    re_from = None
                    re_member_id = None
                    
                    re_blog = models.Blog.query.filter_by(id=blog.re_from).first()
                    re_member = models.Member.query.filter_by(id=blog.re_member_id).first()
                    re_origin_pic_path = re_blog.pic_path
                    if re_blog.exist_pic != 0:
                        re_origin_pic_path = re_blog.pic_path.replace('_thumbnail', '')
                    re_list.append(dict(blog=re_blog, blog_member=re_member, re_origin_pic_path=re_origin_pic_path))

                    re_from = re_blog.re_from    
                    re_member_id = re_blog.re_member_id

                    # exist reblog
                    while re_from :
                        re_blog_t = models.Blog.query.filter_by(id=re_from).first()
                        re_member_t = models.Member.query.filter_by(id=re_member_id).first()
                        re_list.append(dict(blog=re_blog_t, blog_member=re_member_t))
                        
                        re_from = re_blog_t.re_from
                        re_member_id = re_blog_t.re_member_id

                    blog_dict['re_list'] = re_list

                blog_info_list.append(blog_dict)

            # follow detail
            following_count = models.Relation.query.filter(models.Relation.member_id == m.id).count()
            fans_count = models.Relation.query.filter(models.Relation.followee_id == m.id).count()

            # blog count 
            blog_count = models.Blog.query.filter(models.Blog.member_id == m.id).count()

            return render_template('collections.html', member=m, blog_list=blog_info_list, 
                following_count=following_count, fans_count=fans_count, blog_count = blog_count,
                has_prev=has_prev, has_next=has_next, prev_num=prev_num, next_num=next_num, url=url)
    
    elif request.method == 'POST':
        return 'hah'


# blog delete
@app.route('/delpost', methods = ['POST'])
def delpost():
    if request.method == 'POST':
        member_id = session['member_id']

        # get blog id
        data = json.loads(request.form.get('data'))
        blog_id = data['blog_id']

        # delete post
        b = models.Blog.query.filter_by(id=blog_id).first()

        if b.exist_pic != 0:
            filename = os.path.basename(b.pic_path)
            upload_file.image_delete(filename)

        if b is None:
            redirect(url_for('error'))
        db_service.db_delete(b)
        db_service.db_commit()

        return 'delpostsuccess'
    else:
        return redirect(url_for('error'))


# explore
@app.route('/explore', methods = ['GET', 'POST'])
@app.route('/explore/<int:page>', methods = ['GET', 'POST'])
def explore(page=1):
    if request.method == 'GET':
        if 'member_id' in session:
            member_id = session['member_id']
            m = models.Member.query.filter_by(id=member_id).first()
            if m is None:
                redirect(url_for('error'))

            # blog detail
            blog_list_paginate = models.Blog.query.order_by(models.Blog.id.desc()).paginate(page, app.config.get('POSTS_PER_PAGE'), True)

            blog_list = blog_list_paginate.items

            # paginate
            has_prev = blog_list_paginate.has_prev
            has_next = blog_list_paginate.has_next
            prev_num = blog_list_paginate.prev_num
            next_num = blog_list_paginate.next_num

            blog_info_list = []

            # blog collected
            for blog in blog_list:
                # collection
                c = models.Collection.query.filter(and_(models.Collection.member_id==member_id, models.Collection.blog_id==blog.id)).first()
                if c is None:
                    blog_dict = dict(blog=blog, collection='uncollect')
                else:
                    blog_dict = dict(blog=blog, collection='collecting')

                origin_pic_path = blog.pic_path
                if blog.exist_pic != 0:
                    origin_pic_path = blog.pic_path.replace('_thumbnail', '')
                    blog_dict['origin_pic_path'] = origin_pic_path

                # current blog author, is me?
                blog_author = models.Member.query.filter_by(id=blog.member_id).first()
                blog_dict['blog_member'] = blog_author
                if blog_author.id == m.id:
                    blog_dict['is_me'] = True


                # a blog repeat list
                re_list = []

                if blog.post_type == 'REPEAT':
                    re_from = None
                    re_member_id = None
                    
                    re_blog = models.Blog.query.filter_by(id=blog.re_from).first()
                    re_member = models.Member.query.filter_by(id=blog.re_member_id).first()
                    re_origin_pic_path = re_blog.pic_path
                    if re_blog.exist_pic != 0:
                        re_origin_pic_path = re_blog.pic_path.replace('_thumbnail', '')
                    re_list.append(dict(blog=re_blog, blog_member=re_member, re_origin_pic_path=re_origin_pic_path))

                    re_from = re_blog.re_from    
                    re_member_id = re_blog.re_member_id

                    # exist reblog
                    while re_from :
                        re_blog_t = models.Blog.query.filter_by(id=re_from).first()
                        re_member_t = models.Member.query.filter_by(id=re_member_id).first()
                        re_list.append(dict(blog=re_blog_t, blog_member=re_member_t))
                        
                        re_from = re_blog_t.re_from
                        re_member_id = re_blog_t.re_member_id

                    blog_dict['re_list'] = re_list

                blog_info_list.append(blog_dict)

            return render_template('explore.html', member=m, blog_list=blog_info_list, has_prev=has_prev,
                has_next=has_next, prev_num=prev_num, next_num=next_num)

        return redirect(url_for('login', info='访问当前内容，请先登录'))
    elif request.method == 'POST':
        pass
    else:
        return redirect(url_for('error'))


# get private message receiver
@app.route('/receiver', methods = ['GET', 'POST'])
def receiver():
    if request.method == 'GET':
        if 'member_id' in session:
            member_id = session['member_id']
            m = models.Member.query.filter_by(id=member_id).first()
            if m is None:
                redirect(url_for('error'))

            # friends list
            followees = models.Relation.query.filter(models.Relation.member_id == m.id).all()
            followee_list = []
            if followees :
                for followee in followees:
                    followee_info = models.Member.query.filter(models.Member.id == followee.followee_id).first()
                    
                    member_dict = dict(id=followee_info.id, fullname=followee_info.fullname,
                        personality_url=followee_info.personality_url)
                    followee_list.append(member_dict)

            return json.dumps(followee_list)

        return redirect(url_for('login', info='访问当前内容，请先登录'))
    elif request.method == 'POST':
        pass
    else:
        return redirect(url_for('error'))


# send message
@app.route('/sender', methods = ['GET', 'POST'])
def sender():
    if request.method == 'POST':
        if 'member_id' in session:
            member_id = session['member_id']
            m = models.Member.query.filter_by(id=member_id).first()
            if m is None:
                redirect(url_for('error'))

            # get message info
            data = json.loads(request.form.get('data'))
            receiver_id = data['receiver_id']
            msg_content = data['msg_content']
            msg_type = data['msg_type']
            re_msg_id = data['re_msg_id']

            if msg_type == 'NORMAL':
                # add private message text
                message_txt = models.Message_text(content=msg_content, message_name='')
                db_service.db_insert(message_txt)
                db_service.db_commit()

                # add message log
                message_log = models.Message_log(sender_id=m.id, receiver_id=receiver_id,
                    text_id=message_txt.id, send_time=str(datetime.now()), read_time=str(datetime.now()),
                    message_type=msg_type, sender_isdel=0, receiver_isdel=0, is_read=0, re_msg_id=re_msg_id)
                db_service.db_insert(message_log)
                db_service.db_commit()

                # return reciever info and send time
                receiver_info = models.Member.query.filter_by(id=receiver_id).first()

                normal_msg = dict(msg_lid=message_log.id, p_url=receiver_info.personality_url, rfullname=receiver_info.fullname, 
                    ravatar_path=receiver_info.avatar_path, send_time=str(datetime.now()))

                return json.dumps(normal_msg)

            elif msg_type == 'REPLAY':
                # add private message text
                message_txt = models.Message_text(content=msg_content, message_name='')
                db_service.db_insert(message_txt)
                db_service.db_commit()

                # add message log
                message_log = models.Message_log(sender_id=m.id, receiver_id=receiver_id,
                    text_id=message_txt.id, send_time=str(datetime.now()), read_time=str(datetime.now()),
                    message_type=msg_type, sender_isdel=0, receiver_isdel=0, is_read=0, re_msg_id=re_msg_id)
                db_service.db_insert(message_log)
                db_service.db_commit()

                # return reciever info and send time
                receiver_info = models.Member.query.filter_by(id=receiver_id).first()

                replay_msg = dict(msg_lid=message_log.id, p_url=receiver_info.personality_url, rfullname=receiver_info.fullname, 
                    ravatar_path=receiver_info.avatar_path, send_time=str(datetime.now()))

                return json.dumps(replay_msg)

        return redirect(url_for('login', info='访问当前内容，请先登录'))
    elif request.method == 'GET':
        pass
    else:
        return redirect(url_for('error'))


# send message list
@app.route('/sendlist', methods = ['GET'])
def sendlist():
    if request.method == 'GET':
        if 'member_id' in session:
            member_id = session['member_id']
            m = models.Member.query.filter_by(id=member_id).first()
            if m is None:
                redirect(url_for('error'))

            # message list
            messages = models.Message_log.query.filter(and_(models.Message_log.sender_id == m.id, models.Message_log.sender_isdel == 0)).order_by(models.Message_log.id.desc()).all()
            msg_list = []
            for msg in messages:
                # message content
                message_text = models.Message_text.query.filter(models.Message_text.id == msg.text_id).first()
           
                # receiver info
                receiver = models.Member.query.filter_by(id=msg.receiver_id).first()

                # message type
                message_type = msg.message_type
                re_msg_content = None
                if message_type == 'REPLAY':
                    # exist re_msg
                    re_msg = models.Message_log.query.filter(models.Message_log.id == msg.re_msg_id).first()
                    re_msg_text = models.Message_text.query.filter(models.Message_text.id == re_msg.text_id).first()
                    re_msg_content = re_msg_text.content

                # message dict
                msg_dict = dict(msg_lid=msg.id, mp_url=m.personality_url, mfullname=m.fullname, mavatar_path=m.avatar_path, 
                    content=message_text.content, p_url=receiver.personality_url, rfullname=receiver.fullname, 
                    send_time=str(msg.send_time), message_type=message_type, re_msg_content=re_msg_content)

                msg_list.append(msg_dict)
            
            return json.dumps(msg_list)

        return redirect(url_for('login', info='访问当前内容，请先登录'))
    else:
        return redirect(url_for('error'))


# private message
@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        if 'member_id' in session:
            member_id = session['member_id']
            m = models.Member.query.filter_by(id=member_id).first()
            if m is None:
                redirect(url_for('error'))

            # message list
            messages = models.Message_log.query.filter(and_(models.Message_log.receiver_id == m.id, models.Message_log.receiver_isdel == 0)).order_by(models.Message_log.id.desc()).all()
            msg_list = []
            for msg in messages:
                # message content
                message_text = models.Message_text.query.filter(models.Message_text.id == msg.text_id).first()
           
                # sender info
                sender = models.Member.query.filter_by(id=msg.sender_id).first()

                # message type
                message_type = msg.message_type
                re_msg_content = None
                if message_type == 'REPLAY':
                    # exist re_msg
                    re_msg = models.Message_log.query.filter(models.Message_log.id == msg.re_msg_id).first()
                    re_msg_content = models.Message_text.query.filter(models.Message_text.id == re_msg.text_id).first()

                # message dict
                msg_dict = dict(msg_lid=msg.id, sender_id=sender.id, sp_url=sender.personality_url, sfullname=sender.fullname, savatar_path=sender.avatar_path, 
                    content=message_text.content, send_time=str(msg.send_time), 
                    message_type=message_type, re_msg_content=re_msg_content)

                msg_list.append(msg_dict)
            
            return render_template('messages.html', msg_list=msg_list, following_count=session.get('following_count'),
                fans_count=session.get('fans_count'), blog_count=session.get('blog_count'),
                fullname=m.fullname, avatar_path=m.avatar_path, autograph=m.autograph)

        return redirect(url_for('login', info='访问当前内容，请先登录'))
    else:
        return redirect(url_for('error'))


# blog delete
@app.route('/delmsg', methods = ['POST'])
def delmsg():
    if request.method == 'POST':
        member_id = session['member_id']

        # get blog id
        data = json.loads(request.form.get('data'))
        msg_id = data['msg_id']
        del_type = data['del_type']

        # delete msg
        message = models.Message_log.query.filter(models.Message_log.id == msg_id).first()

        if del_type == 1:
            message.sender_isdel = 1
        elif del_type == 2:
            message.receiver_isdel = 1
            
        db_service.db_commit()

        return 'delmsgsuccess'
    else:
        return redirect(url_for('error'))


# upload image
@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and upload_file.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            src_path = os.path.join(app.config.get('UPLOAD_FOLDER'), filename)

            new_name = app.config.get('SITE_NAME') + '_' + upload_file.unique_name() + os.path.splitext(src_path)[1]
            new_path = os.path.join(app.config.get('UPLOAD_FOLDER'), new_name)
            
            file.save(new_path)

            # create thumbsnail
            upload_file.image_thumbnail(new_name)
            
            return new_name


# delete image
@app.route('/delimage', methods = ['POST'])
def delimage():
    if request.method == 'POST':

        # get filename
        data = json.loads(request.form.get('data'))
        filename = data['filename']

        # remove file
        os.remove(os.path.join(app.config.get('UPLOAD_FOLDER'), filename))
        return 'removefilesuccess'


# setting
@app.route('/setting', methods = ['GET'])
def setting():
    if request.method == 'GET':
        if 'member_id' in session:
            member_id = session['member_id']
            m = models.Member.query.filter_by(id=member_id).first()
            if m is None:
                redirect(url_for('error'))

            h = models.Hobby.query.filter_by(member_id=m.id).first()
            
            return render_template('setting.html', member=m, hobby=h)

        return redirect(url_for('login', info='访问当前内容，请先登录'))
    else:
        return redirect(url_for('error'))


# setting info
@app.route('/setting_info', methods = ['POST'])
def setting_info():
    if request.method == 'POST':
        if 'member_id' in session:
            member_id = session['member_id']
            m = models.Member.query.filter_by(id=member_id).first()
            if m is None:
                redirect(url_for('error'))
        
            fullname = request.form.get('fullname')
            personality_url = request.form.get('personality_url')
            gender = request.form.get('gender')
            year = request.form.get('year')
            month = request.form.get('month')
            day = request.form.get('day')
            location_province = request.form.get('location_province')
            location_city = request.form.get('location_city')
            location_area = request.form.get('location_area')
            hometown_province = request.form.get('hometown_province')
            hometown_city = request.form.get('hometown_city')
            hometown_area = request.form.get('hometown_area')
            autograph =  request.form.get('autograph')
            description = request.form.get('description')

            if year == '' or year == '0':
                year = 0
                month = 0
                day = 0

            m.fullname = fullname
            m.personality_url = personality_url
            m.gender = gender
            m.year = year
            m.month = month
            m.day = day
            m.location_province = location_province
            m.location_city = location_city
            m.location_area = location_area
            m.hometown_province = hometown_province
            m.hometown_city = hometown_city
            m.hometown_area = hometown_area
            m.autograph = autograph
            m.description = description
            db_service.db_commit()
            
            # return '更新信息成功'
            return redirect(url_for('info', infos='更新个人信息成功', url='setting'))
        
        return redirect(url_for('login', info='访问当前内容，请先登录'))
    else:
        return redirect(url_for('error'))


# setting hobby
@app.route('/setting_hobby', methods = ['POST'])
def setting_hobby():
    if request.method == 'POST':
        if 'member_id' in session:
            member_id = session['member_id']
            m = models.Member.query.filter_by(id=member_id).first()
            if m is None:
                redirect(url_for('error'))

            favor = request.form.get('favor')
            music = request.form.get('music')
            movie = request.form.get('movie')
            book = request.form.get('book')
            sport = request.form.get('sport')

            h = models.Hobby(favor=favor, music=music, movie=movie, book=book,
                sport=sport, member_id=m.id)
            db_service.db_insert(h)
            db_service.db_commit()
        
            # return '更新爱好成功'
            return redirect(url_for('info', infos='更新爱好成功', url='setting'))

        return redirect(url_for('login', info='访问当前内容，请先登录'))
    else:
        return redirect(url_for('error'))


# setting new password
@app.route('/setting_newpass', methods = ['POST'])
def setting_newpass():
    if request.method == 'POST':
        if 'member_id' in session:
            member_id = session['member_id']
            m = models.Member.query.filter_by(id=member_id).first()
            if m is None:
                redirect(url_for('error'))

            # user info 
            u = models.User.query.filter_by(id=m.user_id).first()
            if u is None:
                redirect(url_for('error'))

            # form
            src_pass = request.form.get('src_pass')
            new_pass = request.form.get('new_pass')
            confirm_pass = request.form.get('confirm_pass')

            if new_pass != confirm_pass:
                # return '两次密码不一致'
                return redirect(url_for('info', infos='两次密码不一致', url='setting'))

            src_pass_encrypt = encryption.encrypt_pass(src_pass, u.salt)
            if src_pass_encrypt != u.password:
                # return '原密码错误'
                return redirect(url_for('info', infos='原密码错误', url='setting'))
            else:
                new_pass_encrypt = encryption.encrypt_pass(new_pass, u.salt)
                u.password = new_pass_encrypt
                db_service.db_commit()

                # return redirect(url_for('logout'))
                return redirect(url_for('info', infos='修改密码成功，请重新登录', url='logout'))

        return redirect(url_for('login', info='访问当前内容，请先登录'))
    else:
        return redirect(url_for('error'))

@app.route('/test', methods=['GET'])
def test():
    return redirect(url_for('info', infos='访问成功', url='setting'))


# info
@app.route('/info', methods = ['GET', 'POST'])
def info():
    if request.method == 'GET':
        infos = request.args.get('infos')
        url = request.args.get('url')
        return render_template('info.html', infos=infos, url=url)
    else:
        return redirect(url_for('error'))


# search
@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        pass
    else:
        return redirect(url_for('error'))


# logout
@app.route('/logout', methods = ['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login', info='注销成功，请重新登录'))


# error
@app.route('/error', methods = ['GET'])
def sys_error():
    return render_template('error_sys.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404


@app.errorhandler(500)
def server_syntax_error(error):
    return render_template('error_500.html'), 500


@csrf.error_handler
def csrf_error(reason):
    return render_template('error_csrf.html', reason=reason), 400