# jwt_auth.py (Middleware)

from ninja.security import HttpBearer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from ..services.auth_service import verify_jwt

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        print(f"Received token: {token}")  # Log the received token for debugging

        payload = verify_jwt(token)  # Get the decoded payload directly
        if not payload:
            print("Invalid or expired token")  # Log if token is invalid or expired
            return None  # ❌ Invalid token or expired token

        try:
            # Fetch the user by id from the payload
            user = User.objects.get(id=payload["id"])  # Fetch the user based on the 'id' from the payload
            return user  # ✅ Return the authenticated user
        except ObjectDoesNotExist:
            print("User not found")  # Log if user is not found
            return None  # ❌ User not found (invalid token)

# Instantiate the JWT authentication class
jwt_auth = JWTAuth()
