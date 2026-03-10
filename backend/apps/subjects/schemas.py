from ninja import Schema,ModelSchema
from datetime import datetime
from enum import Enum
from .models import Subject
class DifficultyLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Status(str, Enum):
    active = "active"
    completed = "completed"
    archived = "archived"

class SubjectExtractResponse(Schema):
    id: int
    raw_text: str
    processed_summary: str
    extracted_topics: dict
    created_at: datetime
    updated_at: datetime

class SubjectFileResponse(Schema):
    id: int
    file: str
    file_type: str
    created_at: datetime
    updated_at: datetime
    subject_extract: SubjectExtractResponse | None



class SubjectCreate(ModelSchema):
    class Meta:
        model = Subject
        fields = [
            'title','description','goal','deadline','difficulty_level','status'
        ]


class SubjectResponse(ModelSchema):
    files: list[SubjectFileResponse] = []
    class Meta:
        model = Subject
        fields = [
            'title','description','goal','deadline','difficulty_level','status'
        ]
