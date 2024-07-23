from fastapi import Depends, HTTPException, Path, APIRouter, Request
from models import Todo
from sqlalchemy.orm import Session
from database import engine, sessionLocal
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from .auth import Get_current_user
import logging

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory = 'templates')

logger = logging.getLogger('uvicorn.error')

router = APIRouter(prefix='/todo', tags=['todo'])

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=50)
    priority: int = Field(gt=0)
    complete: bool

def Get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.get('/', response_class=HTMLResponse)
def Read_all_by_user(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})
        

@router.get('/add-todo', response_class=HTMLResponse)
def Add_todo(request: Request):
    return templates.TemplateResponse('add-todo.html', {'request': request})

@router.get('/edit-todo', response_class=HTMLResponse)
def Edit_todo(request: Request):
    return templates.TemplateResponse('edit-todo.html', {'request': request})

