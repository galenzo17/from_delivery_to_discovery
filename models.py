from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    username: str
    token: str

class Ticket(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None

class TicketUpdateRequest(BaseModel):
    description: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None