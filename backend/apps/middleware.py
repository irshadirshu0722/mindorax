

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from .jwt import *
from apps.users.models import User


class JWTMiddleware(MiddlewareMixin):
  def process_request(self,request):
    """
    Overriding process_request to run custom JWT middleware
    """
    from apps.users.services import TokenService
    token = request.COOKIES.get('access_token')
    if not token:
      request.user = AnonymousUser()
      return
    
    payload = TokenService.verify_token(token)
    if not payload:
      request.user = AnonymousUser()
    print(payload)
    try:
      user = User.objects.get(id=payload['user_id'])
      request.user = user
      print("user Assigned",user)
    except:
      request.user = AnonymousUser()