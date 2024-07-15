from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
app=FastAPI()
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Post(BaseModel):
    title:str
    content:str
    published:bool=True


while True:
    try:
        conn=psycopg2.connect(host='localhost',dbname='postgres', user='postgres', password='admin123',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Connected to dB")
        break
    except Exception as error:
        print("Failed to connect to dB","Error was",error)
        time.sleep(10)


@app.get("/posts")
def get_data():
    cursor.execute(""" SELECT * from posts """)
    posts=cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute(""" INSERT INTO posts(title,content,published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    post=cursor.fetchone()
    conn.commit()
    return {"data":post}

@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("""select * from posts where id = %s """,(str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id`: {id} does not exist")
    return {"data" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    return {"data": updated_post}

        







