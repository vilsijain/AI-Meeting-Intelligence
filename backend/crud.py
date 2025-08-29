
from typing import Optional
from sqlmodel import Session, select
from .models import Meeting, Insight

def create_meeting(session: Session, file_path: str, title: str = "Untitled Meeting") -> Meeting:
    m = Meeting(file_path=file_path, title=title)
    session.add(m)
    session.commit()
    session.refresh(m)
    return m

def create_insight(session: Session, meeting_id: int, transcript: str, participants: str, action_items: str, decisions: str) -> Insight:
    ins = Insight(meeting_id=meeting_id, transcript=transcript, participants=participants, action_items=action_items, decisions=decisions)
    session.add(ins)
    session.commit()
    session.refresh(ins)
    return ins

def get_meetings(session: Session):
    return session.exec(select(Meeting).order_by(Meeting.created_at.desc())).all()

def get_meeting_detail(session: Session, meeting_id: int) -> Optional[Meeting]:
    return session.get(Meeting, meeting_id)

def get_insight_by_meeting(session: Session, meeting_id: int) -> Optional[Insight]:
    return session.exec(select(Insight).where(Insight.meeting_id == meeting_id)).first()
