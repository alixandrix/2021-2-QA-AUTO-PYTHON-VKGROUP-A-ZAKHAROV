from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class VK_ID(Base):
    __tablename__ = 'user_vk'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(30), nullable=False)


