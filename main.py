import random
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from datetime import datetime
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  #Default value
    rating: Optional[int] = None


app = FastAPI()

posts = [{"title": "The first title",
          "content": "Starting to progress in FastApi",
          "published": "True",
          "rating": 4,
          "id": 1}]


def find_post(id):
    for p in posts:
        if p["id"] == id:
            return p


@app.get("/")
def root():
    return {"message": "Welcome to my Apss"}


@app.get("/get_post")
def get_posts():
    return {"data": f"{posts}"}


@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"data": f"Here is post: {post}"}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = random.randrange(0, 10000)
    posts.append(post_dict)
    return {"message": "New post is created"}


@app.get("/check_server")
def check_server():
    return {"message:" f"{datetime.now()}"}
