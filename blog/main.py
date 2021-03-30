from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from . import models, schemas, hashing
from typing import List



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def index():
    return { 'data' : {'name' : 'blooooooog'}}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED)
# def create(request: schemas.Blog, db: Session = Depends(get_db)):
# remove sessionlocal() and db.close from function below
def create(request: schemas.Blog):
    db = SessionLocal()
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    db.close()
    return new_blog

@app.get('/blogs', response_model=List[schemas.ShowBlog])
# def all(db: Session = Depends(get_db)):
def all():
    db = SessionLocal()
    blogs = db.query(models.Blog).all()
    db.close()
    return blogs

@app.get('/blog/{id}', response_model=schemas.ShowBlog)
# def show(id, db: Session = Depends(get_db)):
def show(id, response: Response):
    db = SessionLocal()
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details' : f'blog with id {id} not found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    db.close()
    return blog

@app.delete('/blog/{id}')
def destroy(id, response: Response):
    db = SessionLocal()
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    db.close()
    return {'detail': f'blog with id {id} deleted'}

@app.put('/blog/{id}')
def update(id, request: schemas.Blog, response: Response):
    db = SessionLocal()
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    blog.update({'title' : request.title, 'body' : request.body})
    db.commit()
    db.close()
    return blog.first()



@app.post('/user/')
def create_user(request: schemas.User):
    db = SessionLocal()
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user





