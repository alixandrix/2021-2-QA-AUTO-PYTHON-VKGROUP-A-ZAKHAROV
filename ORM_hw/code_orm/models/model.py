from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class First(Base):
    __tablename__ = 'first_task'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<First" \
               f"id='{self.id}'," \
               f"sum_request='{self.sum_request}' " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sum_request = Column(Integer, nullable=False)


class Second(Base):
    __tablename__ = 'second_task'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Second" \
               f"id='{self.id}'," \
               f"type_request='{self.type_request}'," \
               f"sum_request='{self.sum_request}' " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_request = Column(String(20), nullable=False)
    sum_request = Column(Integer, nullable=False)


class Third(Base):
    __tablename__ = 'third_task'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Third" \
               f"id='{self.id}'," \
               f"url='{self.url}'," \
               f"sum_request='{self.sum_request}' " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(100), nullable=False)
    sum_request = Column(Integer, nullable=False)

    class Fourth(Base):
        __tablename__ = 'fourth_task'
        __table_args__ = {'mysql_charset': 'utf8'}

        def __repr__(self):
            return f"<Third" \
                   f"id='{self.id}'," \
                   f"url='{self.url}'," \
                   f"sum_request='{self.sum_request}' " \
                   f")>"

        id = Column(Integer, primary_key=True, autoincrement=True)
        url = Column(String(100), nullable=False)
        sum_request = Column(Integer, nullable=False)