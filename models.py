from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import Column, String, Integer, Float, LargeBinary
from database import Base

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

# Nuevo modelo para Embeddings
class Embedding(Base):
    __tablename__ = 'embeddings'

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, index=True)
    embedding = Column(LargeBinary)