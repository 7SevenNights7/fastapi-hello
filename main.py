import os
import datetime
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



class NoteIn(BaseModel):
    text: str


class NoteOut(BaseModel):
    id: int
    text: str
    created_at: datetime.datetime


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on your home server!"}


@app.get("/notes", response_model=List[NoteOut])
def get_notes():
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT id, text, created_at FROM notes ORDER BY id;")
            rows = cur.fetchall()
            return [NoteOut(id=row["id"], text=row["text"], create_at=row["created_at"],) for row in rows]


@app.post("/notes", response_model=NoteOut)
def create_note(note: NoteIn):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                "INSERT INTO notes (text) VALUES (%s) RETURNING id, text, created_at;",
                (note.text,),
            )
            row = cur.fetchone()
            conn.commit()
            return NoteOut(id=row["id"], text=row["text"], created_at=row["created_at"],)
