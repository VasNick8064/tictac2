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


class Guess(BaseModel):  # Определяем модель структуры данных для /guess, а так же валидируем данные
    guess: str

    @validator('guess')
    def guess_length(cls, v):
        if len(v) > 1:
            raise ValueError("Введите не более одного символа")
        if not v.isalpha():
            raise ValueError("Введите букву")
        return v


class Create_Word(BaseModel):  # Определяем модель структуры данных для /cw, а так же валидируем данные
    word: str

    @validator("word")
    def word_valid(cls, v):
        if len(v) < 2:
            raise ValueError("Слово не может быть короче 2х символов")
        if not v.isalpha():
            raise ValueError("Слово должно состоять из символов")
        return v
