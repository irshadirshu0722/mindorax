from django.db import models
from apps.utils import CreateUpdateAt
from apps.subjects.models import Subject
# Create your models here.


class StudyPlan(CreateUpdateAt):
  subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name="study_plans")
  ai_generated = models.BooleanField(default=True)
  total_hours = models.IntegerField(null=True,blank=True)
  daily_study_hours = models.IntegerField(null=True,blank=True)
  starting_date = models.DateField()
  end_date = models.DateField()
  is_completed = models.BooleanField(default=False)
  topics = models.JSONField(null=True,blank=True)
  description = models.TextField()
  is_creating = models.BooleanField(default=True)
  is_failed = models.BooleanField(default=False)


class PlanItems(CreateUpdateAt):
  plan = models.ForeignKey(StudyPlan,on_delete=models.CASCADE,related_name="plan_items")
  topic = models.CharField(max_length=1024)
  description = models.TextField()
  estimated_hours = models.IntegerField()
  starting_date_time = models.DateTimeField()
  end_date_time = models.DateTimeField()

class StudySession(CreateUpdateAt):
  plan_item = models.OneToOneField(PlanItems,on_delete=models.CASCADE,related_name="plan_session")
  start_date_time= models.DateTimeField()
  end_date_time = models.DateTimeField()
  duration = models.IntegerField(null=True,blank=True)

  def save(self, *args, **kwargs):
    minutes = int((self.end_date_time - self.start_date_time).total_seconds() // 60)
    self.duration = minutes
    super().save(*args, **kwargs)

