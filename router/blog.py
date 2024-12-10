from fastapi import APIRouter,Depends,status,HTTPException
from typing import List
from ..schemas import showBlog, userSchema,user
from sqlalchemy.orm import Session
from ..models import Blogs,User
from ..database import get_db
from ..oauth import get_current_user




blog_router=APIRouter(
    tags=["blogs"]
)

@blog_router.get("/all-blogs", response_model=List[showBlog], )
async def get_all_blogs(db: Session = Depends(get_db),current_user:user=Depends(get_current_user)):
    blogs = db.query(Blogs).join(User).all()  # Join Blogs and User
    return blogs

# create blog

@blog_router.post("/create",status_code=status.HTTP_201_CREATED,tags=["blogs"],response_model=showBlog)
def create_blog(blog:userSchema,db:Session=Depends(get_db),current_user:user=Depends(get_current_user)):
   new_blog=Blogs(title=blog.title,body=blog.body,user_id=2)
   db.add(new_blog)
   db.commit()
   db.refresh(new_blog)
   return new_blog

# get one blog
@blog_router.get("/getone/{id}", status_code=200, response_model=showBlog, tags=["blogs"])
async def get_by_id(id: int, db: Session = Depends(get_db),current_user:user=Depends(get_current_user)):
    blog = db.query(Blogs).join(User).filter(Blogs.id == id).first()  # Join and filter by ID
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    return blog

# delete blog
@blog_router.delete("/delete-blog/{id}",tags=["blogs"])
def delete_blog_by_id(id:int,db:Session=Depends(get_db),current_user:user=Depends(get_current_user)):
    blog=db.query(Blogs).filter(Blogs.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with this {id} not found")
    
    db.delete(blog)
    db.commit()
    return {"message":"Blog deleted Successfully"}

# # update blog
@blog_router.put("/update/{id}",status_code=status.HTTP_202_ACCEPTED,tags=["blogs"])
def update_blog_by_id(id:int,blog_schema:userSchema,db:Session=Depends(get_db),current_user:user=Depends(get_current_user)):
    blog=db.query(Blogs).filter(Blogs.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with this {id} not found")
    blog.title=blog_schema.title
    blog.body=blog_schema.body

    db.commit()
    db.refresh(blog)
    return blog


