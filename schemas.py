from pydantic import BaseModel
from typing import List,Optional

class userSchema(BaseModel):
    id: int
    title: str
    body: str
    class Config:  # Fixed from `config` to `Config`
        orm_mode = True



class user(BaseModel):
    id: int
    username: str
    email: str
    password: str

class showUser(BaseModel):
    id: int
    username: str
    email: str
    blogs:List[userSchema]

    class Config:  # Fixed from `config` to `Config`
        orm_mode = True

class showBlog(BaseModel):
    title: str  
    body: str  # Fixed typo from `body` to `body`
    creator:showUser

    class Config:  # Fixed from `config` to `Config`
        orm_mode = True


class Login(BaseModel):
    email:str
    password:str


class Token(BaseModel):
    acess_token:str
    token_type:str

class TokenData(BaseModel):
    email:Optional[str]=None    