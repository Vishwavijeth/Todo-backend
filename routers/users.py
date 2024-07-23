from fastapi import APIRouter, HTTPException
from database import engine, sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from starlette import status
from models import Todo, User
from .auth import Get_current_user
from passlib.context import CryptContext
from pydantic import BaseModel, Field



routers = APIRouter(
    prefix='/users',
    tags=['users']
)

def Get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(Get_db)]
user_dependency = Annotated[dict, Depends(Get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
    
class ChangePhoneNumber(BaseModel):
    phone: str = Field(max_length=10)


@routers.get('/get_current_user')
def CurrentUser(user: user_dependency, db: db_dependency, user_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail='no user')
    
    return db.query(User).filter(User.id == user.get('id')).first()

@routers.put('/change_password', status_code=status.HTTP_200_OK)
def ChangePassword(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='no user')
    
    user_model = db.query(User).filter(User.id == user.get('id')).first()
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='invalid password')
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    
    db.add(user_model)
    db.commit()
    
@routers.put('/chenge_phoneNumber', status_code=status.HTTP_200_OK)
def ChangePhoneNumber(user: user_dependency, db: db_dependency, changePhoneNumebr: ChangePhoneNumber):
    if user is None:
        raise HTTPException(status_code=401, detail='no user')
    
    user_model = db.query(User).filter(User.id == user.get('id')).first()
    
    user_model.phone_number = changePhoneNumebr.phone
    
    db.add(user_model)
    db.commit()