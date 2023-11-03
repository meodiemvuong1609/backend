from app.auth.oauth2 import OAuth2

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