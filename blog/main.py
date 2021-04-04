from fastapi import FastAPI
from .database import engine
from . import models
from .routers import blog, user, authentication


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

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

@app.get("/")
def index():
    return { 'data' : {'name' : 'blooooooog'}}
