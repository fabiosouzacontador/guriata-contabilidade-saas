# Updated User Schemas

# Removed UserUpdate schema and retained only the following:

# UserCreate schema
# UserResponse schema
# UserLogin schema
# TokenResponse schema

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

