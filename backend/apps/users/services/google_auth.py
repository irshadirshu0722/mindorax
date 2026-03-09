from apps.users.models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from apps.middleware import *
from apps.users.repository.user_repository import UserRepository


class GoogleAuthService:

  @staticmethod
  def verify_google_token(token: str):
    """
    Verifying google token to proceed with either login or register
    """
    idinfo = id_token.verify_oauth2_token(
          token,
          requests.Request(),
          settings.GOOGLE_CLIENT_ID
      )
    
    return {
      "email":idinfo['email'],
      "oauth_id":idinfo["sub"],
      "oauth_provider":"google"
    }
  
  @staticmethod
  def login_or_create_user(token: str):
    """
    Service for making decision either login or register
    """
    google_data = GoogleAuthService.verify_google_token(token)
    
    user = UserRepository.get_by_email(google_data.get('email'))

    if not user:
      user = UserRepository.create_user(
        **google_data
      )
    return user