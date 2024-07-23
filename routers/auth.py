from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from models import User
from passlib.context import CryptContext
from database import engine, sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
import logging


from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory = 'templates')

logger = logging.getLogger(__name__)

route = APIRouter(prefix='/auth', tags=['auth'])

secret_key = '7547224df7fd4489bf9e774029df942e4832e4f89925c0b88381f60ab1eaccd6'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUser(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: str
    password: str
    role: str
    phone_number: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str

def Get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(Get_db)]

def AuthenticateUser(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user

def Create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    
    encode.update({'exp': expires})
    return jwt.encode(encode, secret_key, algorithm = ALGORITHM)

def Get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        
        username: str = payload.get('sub')
        id: int = payload.get('id')
        role: str = payload.get('role')
    
        print('username: ', username)
        print('user id: ', id)

        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')        
        
        return {'username': username, 'id': id, 'role': role}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='couldd not validate')
    
    
@route.get('/get_all_users')
def GetAllUsers(db: db_dependency):
    return db.query(User).all()
    

@route.post('/auth', status_code=status.HTTP_200_OK)
def CreateUser(db: db_dependency, create_user: CreateUser):
    create_user = User(
        email = create_user.email,
        username = create_user.username,
        firstname = create_user.firstname,
        lastname = create_user.lastname,
        role = create_user.role,
        hashed_password = bcrypt_context.hash(create_user.password),
        is_active = True,
        phone_number = create_user.phone_number
    )
    
    db.add(create_user)
    db.commit()
    
@route.post('/token')
def Login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    user = AuthenticateUser(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
    
    token = Create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    
    return {'access_token': token, 'token' : 'bearer'}


@route.get('/', response_class = HTMLResponse)
def Authentication_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@route.get('/register', response_class= HTMLResponse)
def Registration_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})