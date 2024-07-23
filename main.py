from fastapi import FastAPI
import models
from database import engine

from routers import auth
from routers import todos
from routers import admin
from routers import users
from starlette.staticfiles import StaticFiles

app = FastAPI()

models.base.metadata.create_all(bind = engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.route)
app.include_router(todos.router)
#app.include_router(admin.router)
#app.include_router(users.routers)