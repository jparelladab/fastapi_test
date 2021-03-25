from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def index():
    return { 'data' : {'name' : 'Joan'}}

@app.get("/blog")
#to use the query parameters
def query(limit=10, published:bool = True):
    if published:
        return { 'data' : f'{limit} published articles'}
    else:
        return {'data' : f'{limit} articles'}



@app.get("/blog/unpublished")
def show():
    return { 'data' : 'all unpublished articles'}

@app.get("/blog/{id}")
def show(id:int):
    return { 'data' : {'id' : id}}


class Blog(BaseModel):
    title:str
    body:str
    published: Optional[bool]

class SuperBlog(Blog):
    superTitle:str
    superBody:str

@app.post('/superblog')
def create_blog(request: SuperBlog):
    return request

@app.get('/superblog2/{request}')
def show_blog(request: str):
    hola = 'holation'
    adeo = 'adeuu'
    return { 'data' : 'blog' }