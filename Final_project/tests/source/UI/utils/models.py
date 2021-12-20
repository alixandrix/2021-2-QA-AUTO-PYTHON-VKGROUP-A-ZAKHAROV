from sqlalchemy import Column, Integer, VARCHAR, SmallInteger, DATETIME, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class App_tb(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(16), nullable=True)
    password = Column(VARCHAR(256), nullable=False)
    email = Column(VARCHAR(64), nullable=False)
    access = Column(SmallInteger, nullable=True)
    active = Column(SmallInteger, nullable=True)
    start_active_time = Column(DATETIME, nullable=True)

    UniqueConstraint('email', name=email)
    UniqueConstraint('ix_test_users_username', name=username)




