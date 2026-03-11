from django.db import models
from apps.utils import CreateUpdateAt
from apps.users.models import User
# Create your models here.



class Subject(CreateUpdateAt):
  DIFFICULTY_LEVEL_CHOICES = [
    ('low','LOW'),
    ('medium','Medium'),
    ('high','High')
  ]
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
  difficulty_level = models.CharField(choices=DIFFICULTY_LEVEL_CHOICES,default='low')
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

  
class SubjectExtract(CreateUpdateAt):
  subject_file = models.OneToOneField(SubjectFile,on_delete=models.CASCADE,related_name='subject_extract')
  raw_text = models.TextField()
  processed_summary = models.TextField()
  extracted_topics = models.JSONField()