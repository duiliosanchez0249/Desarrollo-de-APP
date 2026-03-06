from sqlmodel import SQLModel, Field
from typing import Optional

class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    genre: str
    rating: float = Field(default=0.0, ge=0, le=10)
    cover_image: Optional[str] = None
    