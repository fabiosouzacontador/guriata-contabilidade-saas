from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, models, oauth2
from app.database import get_db

router = APIRouter()

@router.post('/login', response_model=schemas.TokenResponse)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await models.User.authenticate(user_credentials.username, user_credentials.password, db)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    token = oauth2.create_access_token(data={'sub': user.username})
    return {'access_token': token, 'token_type': 'bearer'}

@router.post('/register', response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = await models.User.create(user.dict(), db)
    return new_user

@router.get('/users/me', response_model=schemas.UserResponse)
async def get_me(current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    return current_user
