from fastapi import APIRouter
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, hashing, database
from typing import List
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not foundyy"}},
)


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id, response: Response, db: Session = Depends(database.get_db)):
    return user.get(id, response, db)

@router.get('/', response_model=List[schemas.ShowUser])
def all_users(db: Session = Depends(database.get_db)):
    return user.all(db)







