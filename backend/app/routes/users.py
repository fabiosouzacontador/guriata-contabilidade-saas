from fastapi import APIRouter, HTTPException
from typing import List, Optional

router = APIRouter()

# Sample User Model
class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

# Sample in-memory user "database"
users_db = {}  # user_id: User

@router.post("/users/", response_model=User)
async def create_user(name: str, email: str):
    user_id = len(users_db) + 1  # Simple ID assignment
    user = User(id=user_id, name=name, email=email)
    users_db[user_id] = user
    return user

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/", response_model=List[User])
async def read_users():
    return list(users_db.values())

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, name: Optional[str] = None, email: Optional[str] = None):
    user = users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if name:
        user.name = name
    if email:
        user.email = email
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = users_db.pop(user_id, None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
