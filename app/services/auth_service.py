import jwt  # PyJWT
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime
from ..utils.response import success_response, error_response
from ..utils.logging import handle_service_call

# ✅ Generate JWT Token
def generate_jwt(user):
    payload = {
        "id": user.id,
        "username": user.username,
        "exp": datetime.utcnow() + settings.JWT_SETTINGS["ACCESS_TOKEN_LIFETIME"],
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_SETTINGS["ALGORITHM"])
    return token

# ✅ Verify JWT Token
def verify_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_SETTINGS["ALGORITHM"]])
        return payload  # Return payload if the token is valid
    except jwt.ExpiredSignatureError:
        return None  # Return None if the token has expired
    except jwt.InvalidTokenError:
        return None  # Return None if the token is invalid

# ✅ User Login Service
@handle_service_call
def login_user_service(username: str, password: str):
    user = authenticate(username=username, password=password)
    if not user:
        return error_response("Invalid credentials", 401)

    token = generate_jwt(user)
    if not token:
        return error_response("Error generating token", 500)

    return success_response({"token": token}, "Login successful")


# ✅ User Registration Service
@handle_service_call
def register_user_service(username: str, password: str, email: str = None):
    if User.objects.filter(username=username).exists():
        return error_response("Username already taken", 400)

    user = User.objects.create_user(username=username, password=password, email=email)
    return success_response({"id": user.id, "username": user.username}, "User registered successfully", 201)
