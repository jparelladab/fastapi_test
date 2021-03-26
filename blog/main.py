from fastapi import FastAPI
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from . import models, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def index():
    return { 'data' : {'name' : 'blooooooog'}}


@app.post("/post")
def create(request: schemas.Blog):
    return { 'somethin' : request.title, 'hola': request.body}
