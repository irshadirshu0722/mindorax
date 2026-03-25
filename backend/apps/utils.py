from django.db import models
from ninja.errors import HttpError
from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime

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

    def create(self, **data):
        data = self._normalize_datetime_fields(data)
        return self.model.objects.create(**data)

    def get(self, **filters):
        return self.model.objects.get(**filters)

    def filter(self, **filters):
        return self.model.objects.filter(**filters)

    def update(self, instance, **data):
        data = self._normalize_datetime_fields(data)
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

DIFFICULTY_LEVEL_CHOICES = [
    ('low','LOW'),
    ('medium','Medium'),
    ('high','High')
  ]