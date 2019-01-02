from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import MONEY

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    published = Column(Date)
    price = Column(MONEY)

    def __repr__(self):
        return "<Book(title='{}', author='{}', pages={}, published={}, price={})>" \
            .format(self.title, self.author, self.pages, self.published, self.price)
