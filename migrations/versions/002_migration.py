from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
message_log = Table('message_log', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('sender_id', Integer),
    Column('receiver_id', Integer),
    Column('text_id', Integer),
    Column('send_time', DateTime, nullable=False),
    Column('read_time', DateTime, nullable=False),
    Column('message_type', String(length=64), nullable=False),
    Column('sender_isdel', SmallInteger, nullable=False),
    Column('receiver_isdel', SmallInteger, nullable=False),
    Column('is_read', SmallInteger, nullable=False),
    Column('re_msg_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['message_log'].columns['re_msg_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['message_log'].columns['re_msg_id'].drop()
