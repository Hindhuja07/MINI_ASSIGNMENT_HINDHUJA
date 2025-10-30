from typing import Optional, List
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    embedding: Optional[str] = None

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteOut(BaseModel):
    id: int
    title: str
    content: str
