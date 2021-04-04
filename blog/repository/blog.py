from fastapi import Response, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title= request.title, body= request.body, owner_id= request.owner_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def show(id:int, response: Response, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    return blog

def destroy(id:int, response: Response, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'detail': f'blog with id {id} deleted'}

def update(id:int, request: schemas.Blog, response: Response, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    blog.update({'title' : request.title, 'body' : request.body})
    db.commit()
    return blog.first()