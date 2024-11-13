import random
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from datetime import datetime
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

try:
    conn = psycopg2.connect(host='localhost', database='YOUR DB', user='YOUR USER', password='YOUR ADMIN',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database was connection succesfull!")
except Exception as error:
    print("Connecting to database failed")
    print("Error: ", error)
    #time.sleep(2)


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
    cursor.execute("""SELECT * FROM post""")
    my_posts = cursor.fetchall()
    return {"data": f"{my_posts}"}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = (%s) """, (id,))
    my_post = cursor.fetchone()
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"data": f"Here is post: {my_post}"}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO post (title,content,published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


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



