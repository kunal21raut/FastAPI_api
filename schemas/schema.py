from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):

    title:str
    content : str
    author:str
    published: Optional[bool] = None



class UpdateBlog(BaseModel):

    title:Optional[str] = None
    content : Optional[str] = None
    author:Optional[str] = None
    published: Optional[bool] = True



class User(BaseModel):

    username : str
    email : str
    password : str


class ShowUser(BaseModel):
    
    username : str
    email : str

    class Config:
        orm_mode = True
