from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from . import models, schemas, hashing
from typing import List


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "blogs",
        "description": "Manage blogs. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "blogs external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    title="My Super Project",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="2.5.0",
    openapi_tags=tags_metadata
)



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

@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
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

@app.get('/blogs', response_model=List[schemas.ShowBlog], tags=["blogs"])
# def all(db: Session = Depends(get_db)):
def all():
    db = SessionLocal()
    blogs = db.query(models.Blog).all()
    db.close()
    return blogs

@app.get('/blog/{id}', response_model=schemas.ShowBlog, tags=["blogs"])
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

@app.delete('/blog/{id}', tags=["blogs"])
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

@app.put('/blog/{id}', tags=["blogs"])
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



@app.post('/user/', response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User):
    db = SessionLocal()
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user

@app.get('/user/{id}', response_model=schemas.ShowUser, tags=["users"])
def get_user(id):
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details' : f'user with id {id} not found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} not found')
    db.close()
    return user

@app.get('/users', tags=["users"])
def all_users():
    db = SessionLocal()
    users = db.query(models.User).all()
    db.close()
    return users






