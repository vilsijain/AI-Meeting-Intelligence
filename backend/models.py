
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Meeting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = "Untitled Meeting"
    file_path: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    insights: List["Insight"] = Relationship(back_populates="meeting")

class Insight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    meeting_id: int = Field(foreign_key="meeting.id")
    transcript: str = ""
    participants: str = "[]"
    action_items: str = "[]"
    decisions: str = "[]"

    meeting: Optional[Meeting] = Relationship(back_populates="insights")
