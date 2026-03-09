from apps.users.models import User


class UserRepository:

  @staticmethod
  def get_by_email(email):
    return User.objects.get(email=email)
  
  @staticmethod
  def create_user(**data):
    return User.objects.create_user(**data)
