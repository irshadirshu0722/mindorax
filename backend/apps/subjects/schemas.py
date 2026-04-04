from ninja import Schema,ModelSchema
from datetime import datetime
from enum import Enum
from .models import Subject,SubjectFile,SubjectAnalyze
from typing import List, TypeVar, Generic
T = TypeVar("T")


class DifficultyLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Status(str, Enum):
    active = "active"
    completed = "completed"
    archived = "archived"

class SubjectAnalyzeResponse(ModelSchema):
    class Meta:
        model = SubjectAnalyze
        fields = '__all__'

class SubjectFileResponse(ModelSchema):
    full_url: str | None = None

    class Meta:
        model = SubjectFile
        fields = '__all__'
    @staticmethod
    def resolve_full_url(obj, context):
        if not obj.file:
            return None
        request = context["request"]
        return request.build_absolute_uri(obj.file.url)



class SubjectCreate(ModelSchema):
    class Meta:
        model = Subject
        fields = [
            'title','description','goal','deadline','status'
        ]
class SubjectUpdate(ModelSchema):
    class Meta:
        model = Subject
        fields = [
            'title','description','goal','deadline','status'
        ]
        fields_optional = "__all__"


class SubjectResponse(ModelSchema):
    files: list[SubjectFileResponse] = []
    subject_analyze: SubjectAnalyzeResponse | None = None
    class Meta:
        model = Subject
        fields = [
            'title','description','goal','deadline','status','id'
        ]


class SubjectFileCreate(ModelSchema):

    class Meta:
        model = SubjectFile
        fields = ['title','description']
    
