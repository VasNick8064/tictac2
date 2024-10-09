import random
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.responses import HTMLResponse
from models import Base, Word
from fastapi import FastAPI, Depends, HTTPException, Form, Request
from models import Guess, Create_Word

SQLALCHEMY_DB_URL = "sqlite:///./words.db"
engine: Engine = create_engine(
    SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False}
)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TicTac API",
    version="1.0.0")
templates = Jinja2Templates(directory="template")


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


'Получение всех слов из БД'


@app.get("/word")
def read_words(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    words = db.query(Word).offset(skip).limit(limit).all()
    count_words = len(words)  # Количество слов в БД
    return words, f"Слов всего: {count_words}"


'Добавление слова в БД'


@app.post("/cw")
def create_word(db: Session = Depends(get_db), request: Request = None, word: Create_Word = Form(...)):
    db_word = Word(word=word)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return templates.TemplateResponse(
        "create_word.html", {"request": request, "word": db_word, "message": "Слово добавлено в БД"}
    )


@app.get("/create_word", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "create_word.html", {"request": request}
    )


'Удаление слова из БД'


@app.delete("/delete_word/{word_id}")
def delete_word(word_id: int, db: Session = Depends(get_db)):
    word = db.query(Word).filter(Word.id == word_id).first()
    if word:
        db.delete(word)
        db.commit()
        return {"message": "Слово удалено"}
    else:
        return {"message": "Слово не найдено"}


'Получение рандомного слова из БД'


def get_random_word(session):
    words = session.query(Word).all()
    if words:
        return random.choice(words).word
    return None


'Шифрование слова'


def hide_letters(word):
    hidden_word = ["*" for _ in word]
    reveal_indices = random.sample(range(len(word)), 2)
    for i in reveal_indices:
        hidden_word[i] = word[i]
    return hidden_word


'Корневой эндпоинт проекта'


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with session_local() as session:
        word = get_random_word(session)
        if word:
            hidden_word = hide_letters(word)
            return templates.TemplateResponse(
                "index.html", {"request": request, "hidden_word": hidden_word}
            )
        return {"message": "No words in the database"}


"Логика угадывания слова"


@app.post("/guess")
async def guess_letter(request: Request, guess: Guess = Form(...)):  # Добавлена модель структуры данных
    # (наследуемая от BaseModel), а так же валидация данных.
    with session_local() as session:
        word = get_random_word(session)
        if word:
            hidden_word = hide_letters(word)
            guessed_letter = guess.guess
            if guessed_letter in word:
                for i, letter in enumerate(word):
                    if letter == guessed_letter:
                        hidden_word[i] = guessed_letter
            return templates.TemplateResponse(
                "index.html", {"request": request, "hidden_word": hidden_word}
            )
        return {"message": "No words in the database"}

# Как можно применить HTTPException?
# Можно ли в /word/ перенести количество слов всего на др строку?
# Почему в /guess Query параметр request: Request, а в /cw request: Request = None?
# Использование // и / в эндпоинтах
