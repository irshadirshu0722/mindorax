from django.db import models
from apps.utils import CreateUpdateAt,DIFFICULTY_LEVEL_CHOICES
from apps.users.models import User
# Create your models here.



class Subject(CreateUpdateAt):
  
  STATUS_CHOICES = [
    ('active','Active'),
    ('completed','Completed'),
    ('archived','Archived')
  ]
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='subjects')
  title = models.CharField(max_length=200)
  description = models.TextField()
  goal = models.TextField()
  deadline = models.DateField()
  is_analyzing = models.BooleanField(default=False)
  is_failed_analyze =  models.BooleanField(default=False)
  status =  models.CharField(choices=STATUS_CHOICES,default='active')

class SubjectFile(CreateUpdateAt):
  FILE_TYPE = [
    ('pdf','PDF'),
    ('txt','Text Document')
  ]
  subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='files')
  file = models.FileField(upload_to="subjects/")
  file_type = models.CharField(choices=FILE_TYPE,default='pdf')
  title = models.CharField(max_length=1024)
  description = models.TextField()

  
class SubjectAnalyze(CreateUpdateAt):
  subject = models.OneToOneField(Subject,on_delete=models.CASCADE,related_name='subject_analyze')
  difficulty_level = models.CharField(choices=DIFFICULTY_LEVEL_CHOICES,default='low')
  summary = models.TextField()
  topics = models.JSONField()
  subtopics = models.JSONField()
  concepts = models.JSONField()
  topic_wise_priority = models.JSONField(null=True)
  key_points = models.JSONField()
  recommended_focus = models.JSONField()
  estimated_hours = models.IntegerField()