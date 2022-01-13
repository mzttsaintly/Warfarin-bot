import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, BLOB
from .sqlite import Base


class Setu(Base):
    __tablename__ = "setu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Group_id = Column(String(32))
    user_id = Column(Integer)
    image = Column(String(32))
    type = Column(String(32))
    time = Column(DateTime, default=datetime.datetime.now())
