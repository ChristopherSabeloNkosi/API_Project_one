from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
   
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime  

    class Config:
       from_attributes = True 
          
class Post(PostBase):
    id:int
    created_at: datetime
    posted_by: str
    votes:int
   
    
    class Config:
       from_attributes = True 

# class POstOut(PostBase):
#     # id:int
#     # owner_id: int
#     # created_at: datetime
#     owner: UserOut
#     votes: int

    class Config:
          from_attributes = True

       


class UserCreate(BaseModel):
    email: EmailStr  
    Password: str 

    class Config:
       from_attributes = True 



class Show_user(UserOut):
    pass        


class UserLogin(BaseModel):
    email: EmailStr  
    Password: str 
# class PostCreate(PostBase):
#     pass
   
# class Post(PostBase):
#     id:int
#     created_at: datetime
    
#     class Config:
#        orm_mode = True 
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
   


        