from pydantic import BaseModel
from typing import List

class User(BaseModel):
    name:str
    email:str
    password:str

class BlogShort(BaseModel):
    title:str
    body:str
    class Config:
        orm_mode = True

class Blog(BaseModel):
    title:str
    body:str
    owner_id:int
    class Config:
        orm_mode = True

class UserShort(BaseModel):
    id:int
    name:str
    email:str
    class Config:
        orm_mode = True

class ShowUser(User):
    id:int
    name:str
    email:str
    blogs: List[BlogShort] = []
    class Config:
        orm_mode = True

class ShowBlog(Blog):
    id:int
    title:str
    body:str
    owner: UserShort
    class Config:
        orm_mode = True

class Login(BaseModel):
    username:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
