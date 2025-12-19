import os
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import psycopg2.extras

app = FastAPI()

# Читаем строку подключения из переменной окружения
DATABASE_URL = os.environ["DATABASE_URL"]


def get_conn():
    """
    Каждый раз создаём новое соединение.
    Для наших небольших нагрузок это ок.
    """
    return psycopg2.connect(DATABASE_URL)


@app.on_event("startup")
def startup():
    """
    При старте сервера создаём таблицу, если её нет.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL
                );
                """
            )
            conn.commit()


class NoteIn(BaseModel):
    text: str


class NoteOut(BaseModel):
    id: int
    text: str


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on your home server!"}


@app.get("/notes", response_model=List[NoteOut])
def get_notes():
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT id, text FROM notes ORDER BY id;")
            rows = cur.fetchall()
            return [NoteOut(id=row["id"], text=row["text"]) for row in rows]


@app.post("/notes", response_model=NoteOut)
def create_note(note: NoteIn):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                "INSERT INTO notes (text) VALUES (%s) RETURNING id, text;",
                (note.text,),
            )
            row = cur.fetchone()
            conn.commit()
            return NoteOut(id=row["id"], text=row["text"])
