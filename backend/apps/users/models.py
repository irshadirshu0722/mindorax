from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from ..utils import CreateUpdateAt
# Create your models here.



class UserManager(BaseUserManager):
  def create_user(self,email,password=None,**extra_fields):
    if not email:
      raise ValueError("Email Required")

    email = self.normalize_email(email)
    user = self.model(email=email,**extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self,email,password,**extra_fields):
    extra_fields.setdefault('is_staff',True)
    extra_fields.setdefault('is_superuser',True)
    return self.create_user(email,password,**extra_fields)
  
class User(AbstractUser,CreateUpdateAt):
  username = None
  email = models.EmailField(unique=True)
  password = models.CharField(blank=True,null=True)
  oauth_provider = models.CharField(max_length=30)
  oauth_id = models.CharField(max_length=244)
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []
  objects = UserManager()
  def __str__(self):
    return self.email