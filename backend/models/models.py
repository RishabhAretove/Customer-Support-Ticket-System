from pydantic import BaseModel
from datetime import datetime
from typing import List

class TicketCreate(BaseModel):
    title: str
    description: str

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime
