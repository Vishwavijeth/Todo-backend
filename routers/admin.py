from fastapi import APIRouter, HTTPException
from database import engine, sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from starlette import status
from models import Todo
from .auth import Get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def Get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(Get_db)]
user_dependency = Annotated[dict, Depends(Get_current_user)]

@router.get('/todo', status_code=status.HTTP_200_OK)
def Read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='not a admin')
    return db.query(Todo).all()
