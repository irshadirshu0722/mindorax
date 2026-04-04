from django.db import models
from ninja.errors import HttpError
from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from typing import List, TypeVar, Generic
from ninja import Schema
T = TypeVar("T")
class CreateUpdateAt(models.Model):
  """
  Reusable create and update field for every models
  """
  created_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def _normalize_datetime_fields(self, data):
        normalized = data.copy()
        default_tz = timezone.get_default_timezone()

        datetime_fields = {
            field.name
            for field in self.model._meta.fields
            if isinstance(field, models.DateTimeField)
        }

        for field_name in datetime_fields:
            value = normalized.get(field_name)

            if value is None:
                continue

            if isinstance(value, str):
                parsed = parse_datetime(value)
                if parsed is None:
                    raise ValueError(f"Invalid datetime for {field_name}: {value}")
                value = parsed

            if isinstance(value, datetime) and timezone.is_naive(value):
                value = timezone.make_aware(value, default_tz)

            normalized[field_name] = value

        return normalized

    def filter_by_pagination(self,page,page_size,**filter):
        offset = (page - 1) * page_size
        filtered = self.filter(**filter)
        count = filtered.count()
        has_next = count <  offset+page_size 
        return filtered.all()[offset: offset+page_size],count,has_next

    def create(self, **data):
        data = self._normalize_datetime_fields(data)
        return self.model.objects.create(**data)

    def get(self, **filters):
        return self.model.objects.get(**filters)

    def filter(self, **filters):
        return self.model.objects.filter(**filters)

    def update(self, instance, **data):
        data = self._normalize_datetime_fields(data)
        print(data)
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()

    def get_with_is_author(self, user, **filter):
        instance = self.get(**filter)
        if instance.user != user:
            raise HttpError(status_code=403, message="You are not allowed to view this item")
        return instance

class BasePaginationService:
    def _build_pagination_response(self,items,count,page,page_size,has_next):
        return {
            'next': f"?page={page + 1}&page_size={page_size}" if has_next else None,
            'prev': f"?page={page - 1}&page_size={page_size}" if page > 1 else None,
            'items': items,
            'count': count
        }

class PaginationResponse(Schema,Generic[T]):
    next: str | None
    prev: str | None
    items : List[T]
    count: int

DIFFICULTY_LEVEL_CHOICES = [
    ('low','LOW'),
    ('medium','Medium'),
    ('high','High')
  ]