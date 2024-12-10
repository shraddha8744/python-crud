from fastapi import APIRouter,Depends,status,HTTPException
from typing import List
from ..schemas import showBlog, userSchema,showUser,user
from sqlalchemy.orm import Session
from ..models import Blogs,User
from ..database import get_db
from passlib.context import CryptContext


user_router=APIRouter(
    tags=["users"]
)
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")



@user_router.post("/create-user",status_code=status.HTTP_201_CREATED,response_model=showUser,)
async def create_user(user_data:user,db:Session=Depends(get_db)):
    exist_user=db.query(User).filter(User.email==user_data.email).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{user_data.email} this email alredy exit")


    hash_Passowrd=pwd_context.hash(user_data.password)
    
    new_user=User(username=user_data.username,email=user_data.email,password=hash_Passowrd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


 #get user by id

@user_router.get("/get-user/{id}",status_code=status.HTTP_200_OK,response_model=showUser,tags=["users"])
async def get_user_by_id(id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with  id {id} not found")
    
    return user


