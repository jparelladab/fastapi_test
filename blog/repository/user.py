from fastapi import Response, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, hashing


def create(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get(id:int, response: Response, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details' : f'user with id {id} not found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} not found')
    return user

def all(db: Session):
    users = db.query(models.User).all()
    return users