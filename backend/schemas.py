
from typing import List, Optional
from pydantic import BaseModel

class ActionItem(BaseModel):
    owner: Optional[str] = None
    description: str
    due_date: Optional[str] = None
    priority: Optional[str] = "medium"

class Decision(BaseModel):
    summary: str
    rationale: Optional[str] = None

class Participant(BaseModel):
    name: str
    role: Optional[str] = None
    spoke_time_sec: Optional[float] = None

class InsightPayload(BaseModel):
    transcript: str
    participants: List[Participant] = []
    action_items: List[ActionItem] = []
    decisions: List[Decision] = []

class MeetingOut(BaseModel):
    id: int
    title: str

class SearchHit(BaseModel):
    text: str
    distance: float
    meeting_id: int
