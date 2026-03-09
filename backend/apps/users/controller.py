from ninja import Router
from .schemas import LoginRegisterIn
from .services import GoogleAuthService,TokenService
from apps.middleware import *
from django.http import JsonResponse
router = Router()

# Login and Register with google account
@router.post('/google-login')
def google_auth(request,data: LoginRegisterIn):
  user = GoogleAuthService.login_or_create_user(data.id_token)

  access_token = TokenService.create_access_token(user.id)
  refresh_token = TokenService.create_refresh_token(user.id)

  return {
    'access_token':access_token,
    'refresh_token':refresh_token
  }

# Forget Password
@router.get('/refresh')
def refresh_token(request):

  refresh_token = request.COOKIES.get('refresh_token')

  if not refresh_token:
    return JsonResponse({"error": "Refresh token missing"}, status=401)
  
  access_token = TokenService.refresh_access_token(refresh_token)
  return {
    'access_token':access_token
  }
