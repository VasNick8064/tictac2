from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, validator

Base = declarative_base()


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True)
    is_guesses = Column(Boolean, default=False)


class Guess(BaseModel):  # Модель для ввода ответа
    guess: str

    @validator('guess')
    def guess_length(cls, v):
        if len(v) > 1:
            raise ValueError("Введите не более одного символа")
        if not v.isalpha():
            raise ValueError("Введите букву")
        return v