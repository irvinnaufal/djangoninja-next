from ninja import NinjaAPI
from .middleware.jwt_auth import jwt_auth  # ✅ Import JWT auth
from .apis.item_api import item_api
from .apis.auth_api import auth_api

api = NinjaAPI(
    title="My Project API",
    version="1.0.0",
    description="This is a structured API with multiple endpoints."
)

# ✅ Apply JWT authentication only for "/items" endpoints
api.add_router("/items", item_api, auth=jwt_auth)
api.add_router("/auth", auth_api)