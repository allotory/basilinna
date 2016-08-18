create database basilinna;

use basilinna;

/*
 * 用户表
 */
CREATE TABLE IF NOT EXISTS user (
    id int unsigned NOT NULL AUTO_INCREMENT,    /* 用户 ID（唯一标识） */
    email varchar(128) NOT NULL,                /* 邮箱*/
    password varchar(256) NOT NULL,
    salt varchar(128) NOT NULL,                 /* 密码加密盐 */
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,       /* 创建时间（时间戳） */
    last_login_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  /* 最近一次登录时间（时间戳）*/
    last_login_ip varchar(16) NOT NULL,         /* 最近登录的IP地址 */
    status tinyint(1) unsigned NOT NULL,        /* 启用状态：0-表示禁用，1-表示启用 */
    remark varchar(256) DEFAULT NULL,           /* 备注信息 */
    invent varchar(256) NOT NULL,               /* 邀请链接 */
    PRIMARY KEY(id),
    KEY username (username),
    KEY password (password(40)),                /* 没必要做256长度的索引，取前40即可，否则报：“Specified key was too long; max key length is 767 bytes” */
    KEY email (email),
    KEY last_login_time (last_login_time)
);

/* 
 * 成员信息表
 */
CREATE TABLE IF NOT EXISTS member (
    id int(11) NOT NULL AUTO_INCREMENT,             /* 成员ID（唯一标识） */
    fullname varchar(64) NOT NULL,                  /* 全名 */
    gender int(11) NOT NULL DEFAULT '0',            /* 性别  1:male , 2:female , 3: other */
    avatar_path varchar(256) DEFAULT NULL,          /* 头像路径 */
    year varchar(16) DEFAULT NULL,                  /* 年 */
    month varchar(16) DEFAULT NULL,                 /* 月 */
    day varchar(16) DEFAULT NULL,                   /* 日 */
    location_province varchar(128) DEFAULT NULL,    /* 居住位置 */
    location_city varchar(128) DEFAULT NULL,        /* 居住位置 */
    location_area varchar(128) DEFAULT NULL,        /* 居住位置 */
    hometown_province varchar(128) DEFAULT NULL,    /* 家乡位置 */
    hometown_city varchar(128) DEFAULT NULL,        /* 家乡位置 */
    hometown_area varchar(128) DEFAULT NULL,        /* 家乡位置 */
    description varchar(256) DEFAULT NULL,          /* 个人描述 */
    autograph varchar(128) DEFAULT NULL,            /* 签名 */
    personality_url varchar(64) DEFAULT NULL,       /* 个性网址 */
    is_email_actived int(11) NOT NULL DEFAULT '0',  /* 邮箱是否激活 0：否， 1：是 */
    user_id int NOT NULL DEFAULT '0',               /* 用户ID */
    PRIMARY KEY (id)
);

/* 
 * 用户关注表
 *
 *  关注
 *  粉丝
 *  双向关注(互粉)
 *  无关系
    
 *  查询关注列表
 *  查询粉丝列表
 *  查询双向关注列表
 *  判断两个用户的关系
 *  查询带关系状态的任一列表
 * */
CREATE TABLE IF NOT EXISTS relationship (
    id int(11) NOT NULL AUTO_INCREMENT,         /* 关系ID（唯一标识） */
    member_id int(11) NOT NULL,                 /* 成员ID */
    followee_id int(11) NOT NULL,               /* 当前成员关注的人  */     
    PRIMARY KEY (id)
);

/*
* 微博表
*
* */
CREATE TABLE IF NOT EXISTS blog (
    id int(11) NOT NULL AUTO_INCREMENT,         /* ID（唯一标识） */
    content text DEFAULT NULL,                  /* 微博内容表 */
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  /* 更新时间 */
    post_type  varchar(256) NOT NULL,           /* 微博类型：正常NORMAL，转发REPEAT， 回复REPLAY */
    re_from int(11) DEFAULT NULL,               /* 被转发、回复的blog id */
    re_member_id int(11) DEFAULT NULL,          /* 被转发、回复的用户id */
    via varchar(256) NOT NULL,                  /* 提交方式 */
    exist_pic int(11) NOT NULL DEFAULT '0',     /* 是否有图片 */
    pic_path varchar(256) DEFAULT NULL,         /* 图片路径 */
    location varchar(256) DEFAULT NULL,         /* 当前位置 */
    member_id int(11) NOT NULL,                 /* 用户ID */
    PRIMARY KEY (id)
);

/* 
 * 收藏表 
 */
CREATE TABLE IF NOT EXISTS collection (
    id int(11) NOT NULL AUTO_INCREMENT,         /* 收藏ID（唯一标识） */
    blog_id int(11) NOT NULL,                   /* 被收藏的微博ID */
    member_id int(11) NOT NULL,                 /* 收藏用户ID */
    PRIMARY KEY (id)
);

/*
 * 屏蔽用户
 */
CREATE TABLE IF NOT EXISTS block (
    id int(11) NOT NULL AUTO_INCREMENT,     /* 屏蔽表ID（唯一标识） */
    blocked_id int(11) NOT NULL,            /* 被屏蔽用户ID */
    member_id int(11) NOT NULL,             /* 当前用户ID */
    PRIMARY KEY (id)
);

/*
 * 消息内容表
 */
CREATE TABLE IF NOT EXISTS message_text (
    id int(11) NOT NULL AUTO_INCREMENT,         /* 消息内容ID（唯一标识） */
    content text NOT NULL,                      /* 消息内容 */
    message_name varchar(64) NOT NULL,          /* 消息英文名称  */
    PRIMARY KEY (id)
);

/*
 * 消息记录表
 */
CREATE TABLE IF NOT EXISTS message_log (
    id int(11) NOT NULL AUTO_INCREMENT,         /* 用户消息ID（唯一标识） */
    sender_id int(11) NOT NULL,                 /* 发送用户ID */
    receiver_id int(11) NOT NULL,               /* 接收用户ID */
    text_id int(11) NOT NULL,                   /* 消息内容ID */
    send_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, /* 发送时间  设置时间时不需要更新*/
    read_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, /* 阅读时间 */
    message_type varchar(64) NOT NULL,          /* 消息类型 NORMAL / REPLAY */
    sender_isdel smallint NOT NULL,             /* 发送用户是否删除 0:否 ，1：是 */
    receiver_isdel smallint NOT NULL,           /* 接收用户是否删除 0:否 ，1：是 */
    is_read smallint NOT NULL,                  /* 是否已读 0:否 ，1：是  */
    re_msg_id int(11) DEFAULT NULL,
    PRIMARY KEY (id)
);

/*
 * 兴趣爱好表
 */
CREATE TABLE IF NOT EXISTS hobby (
    id int(11) NOT NULL AUTO_INCREMENT,         /* 兴趣爱好ID（唯一标识）*/
    favor varchar(256) NOT NULL,                /* 兴趣爱好 */
    music varchar(256) NOT NULL,                /* 喜欢的音乐 */
    movie varchar(256) NOT NULL,                /*  喜欢的电影 */
    book varchar(256) NOT NULL,                 /* 喜欢的书 */
    sport varchar(256) NOT NULL,                /* 喜欢的运动 */
    member_id int(11) NOT NULL,                 /* 当前用户ID */
    PRIMARY KEY (id)
);

/*
 * 隐私表
 */
CREATE TABLE IF NOT EXISTS privacy (
    id int(11) NOT NULL AUTO_INCREMENT,         /* 兴趣爱好ID（唯一标识）*/
    allow_access int(11) NOT NULL DEFAULT '0',  /* 需要我批准才能查看我的消息 */
    allow_pm int(11) NOT NULL DEFAULT '0',      /* 只接收我关注的人发的私信 */
    allow_findme int(11) NOT NULL DEFAULT '0',  /* 知道我的 MSN/Gtalk/QQ 或 Email 也没法找到我 */
    member_id int(11) NOT NULL,             /* 当前用户ID */
    PRIMARY KEY (id)
);

/*
 * 邮件通知表
 */
CREATE TABLE IF NOT EXISTS emailme (
    id int(11) NOT NULL AUTO_INCREMENT,                 /* 兴趣爱好ID（唯一标识）*/
    allow_pri_msg int(11) NOT NULL DEFAULT '0',         /* 当有新私信时，发 Email 通知我 (每天最多一封) */
    allow_follow_me int(11) NOT NULL DEFAULT '0',       /* 当有人关注我时，发 Email 通知我 */
    allow_new_trend int(11) NOT NULL DEFAULT '0',       /* 当发布最新动态时，发 Email 通知我 (一个月最多一封) */
    allow_follow_care int(11) NOT NULL DEFAULT '0',     /* 我关注别人时通知关注我的人 */
    allow_show_follow_msg int(11) NOT NULL DEFAULT '0',  /* 在首页消息列表中显示关注消息 */
    allow_illegal_login int(11) NOT NULL DEFAULT '0',   /* 将非法登陆尝试通过私信发给我 */
    member_id int(11) NOT NULL,                         /* 当前用户ID */
    PRIMARY KEY (id)
);