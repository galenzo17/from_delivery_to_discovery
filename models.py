from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    username: str
    token: str

class Ticket(BaseModel):
    id: str
    title: str
    description: Optional[str]
    acceptance_criteria: Optional[List[str]]

class TicketUpdateRequest(BaseModel):
    description: Optional[str]
    acceptance_criteria: Optional[List[str]]
