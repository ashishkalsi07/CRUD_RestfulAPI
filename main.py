from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
app=FastAPI()
from pydantic import BaseModel
from typing import Optional
from random import randrange


#validating(Auto Validation) the data that it should be as per our defined formats so we have used pydantic BaseModel for it.
class Post(BaseModel):
    title:str
    content:str
    published:bool=True
# by default the published is set to True 
    rating: Optional[int]=None
#for rating it should be a integer but pydantic can try to convert to integerm default is set to none

my_posts=[{"title":"post1","content":"content of post 1","id":1},{"title":"post2","content":"content of post 2","id":2}]

#routes or path operations

#@app.get("/")   #decorators is @app , .get is http method , inside brackets is the path
def read_root():
    return {"Hello": "Welcome to API Dev.using Python"}

#to retrieve data from server we use get http method 
@app.get("/posts")
def get_data():
    return {"data": my_posts}

# put req - in put request we send data with api to the server

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict=post.model_dump() # converting the Post Model(from Post Class into a dictionary)
    post_dict['id']=randrange(0,100000)
    my_posts.append(post_dict)
    #we can access the post data by new_post.content and new_post.title
    return {"data":post_dict}

@app.get("/posts/latest")
def latest_post():
    post=my_posts[len(my_posts)-1]
    return {"data":post}    


@app.get("/posts/{id}")
def get_posts(id,response:Response):
    post=find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post NOT Found with Id {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data":f"Post NOT Found with Id {id}"}

    return {"data" : post}

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i   
            
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int):
    index=find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
    index=find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} does not exist")
    
    post_dict=post.model_dump()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"msg": post_dict}

