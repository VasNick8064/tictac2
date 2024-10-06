from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True)
    is_guesses = Column(Boolean, default=False)
