from ninja import Schema

class LoginRegisterIn(Schema):
  # Google OAuth id for login and register
  id_token: str
