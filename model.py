from sqlalchemy import String, Integer, Column, Boolean
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    isMale = Column(Boolean, nullable=False)

