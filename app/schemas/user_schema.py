from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    password: str
    email: str = None  # Optional
    
class LoginSchema(BaseModel):
    username: str
    password: str
