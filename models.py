from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, validator
from typing import List

Base = declarative_base()


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True)
    is_guesses = Column(Boolean, default=False)


class Guess(BaseModel):  # Определяем модель структуры данных для Guess, а так же валидируем данные
    guess: str

    @validator('guess')
    def guess_length(cls, v):
        if len(v) > 1:
            raise ValueError("Введите не более одного символа")
        if not v.isalpha():
            raise ValueError("Введите букву")
        return v