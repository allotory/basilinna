from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
blog = Table('blog', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('content', Text),
    Column('create_time', DateTime, nullable=False),
    Column('post_type', String(length=256), nullable=False),
    Column('re_from', Integer),
    Column('re_member_id', Integer),
    Column('via', String(length=256), nullable=False),
    Column('exist_pic', Integer, nullable=False),
    Column('pic_path', String(length=256)),
    Column('location', String(length=256)),
    Column('member_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['blog'].columns['re_from'].create()
    post_meta.tables['blog'].columns['re_member_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['blog'].columns['re_from'].drop()
    post_meta.tables['blog'].columns['re_member_id'].drop()
