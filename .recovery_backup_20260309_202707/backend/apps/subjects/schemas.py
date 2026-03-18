from ninja import Schema
from datetime import datetime
from enum import Enum

class DifficultyLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Status(str, Enum):
    active = "active"
    completed = "completed"
    archived = "archived"

class BaseSubject(Schema):
  id : int
  title : str
  description : str
  goal : str
  deadline : datetime
  status : Status
  updated_at : datetime
  created_at : datetime

class SubjectCreate(BaseSubject):
  updated_at: None | datetime = None
  created_at: None |datetime = None
  id : None | datetime =  None


class SubjectResponse(BaseSubject):
  pass
