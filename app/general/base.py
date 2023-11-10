from app.auth.oauth2 import OAuth2
from fastapi import Depends, Request, Response
from fastapi.routing import APIRoute

oauth2 = OAuth2("secret_key", "HS256", 30)

def convert_response(message, status_code, data=None, count=None):
  """
    Convert body response to normalization.
  """
  
  response = {
    "message": message,
    "code": status_code,
  }
  
  if data is not None:
    response.update({"data": data})
  if count is not None:
    response.update({"count": count})

  return response

def is_authenticated(func):
  def wrapper(request: Request):
    access_token = request.cookies.get("access_token")
    if access_token is None:
      return convert_response("Missing access token", 400)
    payload = oauth2.verify_token(access_token)
    if not payload:
      return convert_response("Invalid access token", 400)
    request.user_id = payload["sub"]
    return func(request)
  return wrapper