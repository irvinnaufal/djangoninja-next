from ninja import Router
from ..services.auth_service import register_user_service, login_user_service
from ..schemas.user_schema import UserSchema, LoginSchema  # ✅ Import schema

auth_api = Router()

@auth_api.post("/register", response=dict)
def register_user(request, user_data: UserSchema):
    return register_user_service(user_data.username, user_data.password, user_data.email)

@auth_api.post("/login", response=dict)
def login_user(request, credentials: LoginSchema):
    return login_user_service(credentials.username, credentials.password)
