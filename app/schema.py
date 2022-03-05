from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    author = Column(String)
    text = Column(String)
