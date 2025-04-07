from fastapi import FastAPI, Depends, status, Response, HTTPException
from config.db import Base, engine,get_db
from models import models
from schemas import schema
from sqlalchemy.orm import Session
import uuid
import json
from passlib.context import CryptContext
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.get("/")
def main():
    return "Hello, World!"


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

@app.post("/create-blog",status_code=status.HTTP_201_CREATED,tags=["Blog"])
def create_blog(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,
                           content=request.content,
                           author=request.author,
                           is_published=request.published)
    
    db.add(new_blog)
    
    db.commit()
    db.refresh(new_blog)
    return {"message": "Blog created successfully!","new_blog": new_blog}
    # return new_blog


@app.get("/blogs",status_code=status.HTTP_200_OK, tags=["Blog"])
def show_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs

@app.get("/blogs/{id}",status_code=status.HTTP_200_OK, tags=["Blog"])
def get_blog(id:int,response:Response, db:Session=Depends(get_db),):
    blog = db.query(models.Blog).filter(models.Blog.id==id).all()

    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This blog dosen't exists")

    return blog


@app.put("/update-blog/{id}",status_code=status.HTTP_202_ACCEPTED, tags=["Blog"])
def update_blog(id:int,response:Response, request: schema.UpdateBlog, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This blog dosen't exist")
    
    print("request: ",request)
    blog.title=request.title if request.title else blog.title
    blog.content=request.content if request.content else blog.content
    blog.author=request.author if request.author else blog.author
    blog.is_published = request.published

    db.commit()
    db.refresh(blog)

    return {"detail":f"Blog Updated Successfully for id {id}"}


@app.delete("/delete-blog/{id}",status_code=status.HTTP_204_NO_CONTENT, tags=["Blog"])
def delete_blog(id:int,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This blog dosen't exists")

    db.delete(blog)
    db.commit()

    return "Blog Deleted Successfully"



@app.post("/create-user",response_model=schema.ShowUser, status_code=status.HTTP_201_CREATED,tags=["Users"])
def create_user(request:schema.User,db:Session=Depends(get_db)):
    pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

    hashed_pwd = pwd_context.hash(request.password)

    userid = str(uuid.uuid4())
    new_user = models.User(
        userid=userid,
        username=request.username,
        email =  request.email,
        password = hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # return Response(content=json.dumps({"message":"User created successsfully"}))
    return new_user


@app.get("/show-users",response_model=List[schema.ShowUser],status_code=status.HTTP_200_OK,tags=["Users"])
def show_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()

    return users


@app.get("/get-user/{username}",response_model=List[schema.ShowUser],status_code=status.HTTP_200_OK,tags=["Users"])
def get_user(username:str,db:Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.username==username).all()

    if not user:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"User not found with username => {username}"})
        return Response(status_code=status.HTTP_404_NOT_FOUND,content=str({"message":f"User not found with username {username}"}))
    return user


# {
#   "user": "admin",
#   "data": ["banana", "apple", "sky"]
# }

# import json
# def is_user_admin(func):
#     def wrapper(*args,**kwargs):
#         result = func(*args)
#         for arg in args:
#             if args.user != "admin":
#                 return Response(detail=json.dumps({"error":"Access Denied"}),status_code=status.HTTP_403_FORBIDDEN)

#     return wrapper




# def