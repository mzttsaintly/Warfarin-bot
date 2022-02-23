import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, BLOB
from .sqlite import Base


class Setu(Base):
    __tablename__ = "setu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Group_id = Column(Integer)
    user_id = Column(Integer)
    image = Column(String(32))
    type = Column(String(32))
    time = Column(DateTime, default=datetime.datetime.now())


class ImageInformation(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "image_information"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_name = Column(String(32))
    path_name = Column(String(32))
    character = Column(String(32))
    title = Column(String(32))
    hair = Column(String(32))
    tags = Column(String(32))
    ero = Column(Integer)

    class KeyWord(Base):
        __tablename__ = "KeyWord"
        id = Column(Integer, primary_key=True, autoincrement=True)
        alias = Column(String(32))
        direction = Column(String(32))
