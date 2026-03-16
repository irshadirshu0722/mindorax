from django.db import models
from ninja.errors import HttpError
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
    
    def create(self, **data):
        return self.model.objects.create(**data)
    def get(self, **filters):
        return self.model.objects.get(**filters)
    
    def filter(self, **filters):
        return self.model.objects.filter(**filters)
    def update(self, instance, **data):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    def delete(self, instance):
        instance.delete()
    def get_with_is_author(self,user,**filter):
        instance = self.get(**filter)
        if instance.user != user:
            raise HttpError(status_code=403,message="You are not allowed to view this item")
        return instance

DIFFICULTY_LEVEL_CHOICES = [
    ('low','LOW'),
    ('medium','Medium'),
    ('high','High')
  ]