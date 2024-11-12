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
          "id": 1},
         {"title": "The second title",
          "content": "Starting to progress in FastApi",
          "published": "True",
          "rating": 4,
          "id": 2}
         ]


def find_post(id):
    for p in posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(posts):
        if p["id"] == id:
            print(i)
            return i

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


@app.delete("/deletePost/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is not None:
        posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="Post not found")

@app.put("/updatePost/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is not None:
        post_dict = post.dict()
        post_dict["id"] = id
        posts[index] = post_dict

        return {"message": "Updated Successfully"}

    raise HTTPException(status_code=404, detail="Post not found")


