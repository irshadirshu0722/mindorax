import jwt
from datetime import timedelta,datetime
from django.conf import settings


class TokenService:
  @staticmethod
  def create_access_token(user_id):
    """
    Create Access Token
    """
    payload = {
      "user_id":user_id,
      'exp':datetime.utcnow() + timedelta(minutes = settings.JWT_ACCESS_EXPIRE_MINUTES),
      "type":"access"
    }
    return jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.JWT_ALGORITHM)
  @staticmethod
  def create_refresh_token(user_id):
    
    payload = {
          "user_id": str(user_id),
          "exp": datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS),
          "type": "refresh"
      }
    return jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.JWT_ALGORITHM)
  @staticmethod
  def verify_token(token):
    try:
      payload = jwt.decode(token,settings.JWT_SECRET,algorithms=[settings.JWT_ALGORITHM])
      return payload
    except jwt.ExpiredSignatureError:
        print("1")
        return None
    except jwt.InvalidTokenError:
        print('2')
        return None
  @staticmethod
  def refresh_access_token(token):
    try:
      payload = TokenService.verify_token(token)
      if payload.get('type') != 'refresh':
        raise Exception("Invalid token type")
      
      user_id = payload['user_id']
      access_token = TokenService.create_access_token(user_id)
      return access_token
    except jwt.ExpiredSignatureError:
      return {'error':'Refresh token expired'}
    except jwt.InvalidTokenError:
      return {'error':"Invalid token"}
