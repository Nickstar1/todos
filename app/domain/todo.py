import uuid
from typing import Optional
from datetime import datetime

from app.domain.location import Location


class Todo:
    def __init__(self, 
                 id: uuid.UUID, 
                 task: str, 
                 created_at: datetime, 
                 completed: bool = False, 
                 location: Optional[Location] = None, 
                 due_date: Optional[datetime] = None, 
                 updated_at: Optional[datetime] = None):
        self.id: uuid.UUID = id
        self.task: str = task
        self.completed: bool = completed
        self.location: Optional[Location] = location
        self.due_date: Optional[datetime] = due_date
        self.created_at: datetime = created_at
        self.updated_at: Optional[datetime] = updated_at
