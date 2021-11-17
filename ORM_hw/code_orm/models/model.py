from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class First(Base):
    __tablename__ = 'first_task'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    sum_request = Column(Integer, nullable=False)


class Second(Base):
    __tablename__ = 'second_task'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_request = Column(String(20), nullable=False)
    sum_request = Column(Integer, nullable=False)


class Third(Base):
    __tablename__ = 'third_task'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(100), nullable=False)
    sum_request = Column(Integer, nullable=False)


class Fourth(Base):
    __tablename__ = 'fourth_task'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(300), nullable=False)
    status = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    ip_addr = Column(String(20), nullable=False)


class Fifth(Base):
    __tablename__ = 'fifth_task'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_addr = Column(String(20), nullable=False)
    sum_request = Column(Integer, nullable=False)
