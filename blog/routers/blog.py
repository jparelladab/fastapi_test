from fastapi import APIRouter
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, hashing, database, oauth2
from typing import List
from ..repository import blog

router = APIRouter(
     tags=["blogs"],
     prefix='/blog'
)

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create(request, db)

@router.get('/{id}', response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(database.get_db)):
 return blog.show(id, response, db)

@router.delete('/{id}')
def destroy(id, response: Response, db: Session = Depends(database.get_db)):
    return blog.destroy(id, response, db)

@router.put('/{id}')
def update(id, request: schemas.Blog, response: Response, db: Session = Depends(database.get_db)):
   return blog.update(id, request, response, db)

