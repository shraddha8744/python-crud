from fastapi import FastAPI,Depends,status,Response,HTTPException
from .database import Base,SessionLocal,engine
from .models  import Blogs
from .schemas import userSchema
from sqlalchemy.orm import Session
Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
# Allow CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[" http://localhost:5173"],  # Replace with your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()    


@app.get("/")
def root():
    return {"msg":"Server Started"}

@app.post("/create",status_code=status.HTTP_201_CREATED)
def create_blog(blog:userSchema,db:Session=Depends(get_db)):
   new_blog=Blogs(title=blog.title,bbody=blog.body)
   db.add(new_blog)
   db.commit()
   db.refresh(new_blog)
   return new_blog


@app.get("/all-blogs")
def get_all_blogs(db:Session=Depends(get_db)):
    blogs=db.query(Blogs).all()

    return blogs

@app.get("/getone/{id}",status_code=200)
def get_by_id(id,response:Response,db:Session=Depends(get_db)):
    blog=db.query(Blogs).filter(Blogs.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with this {id} not found serach other")
    #  response.status_code=status.HTTP_404_NOT_FOUND
    #  return{ "message":f"blog with this {id} not found"}
   
    return blog

@app.delete("/delete-blog/{id}")
def delete_blog_by_id(id:int,db:Session=Depends(get_db)):
    blog=db.query(Blogs).filter(Blogs.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with this {id} not found")
    
    db.delete(blog)
    db.commit()
    return {"message":"Blog deleted Successfully"}

# update log
@app.put("/update/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog_by_id(id:int,blog_schema:userSchema,db:Session=Depends(get_db)):
    blog=db.query(Blogs).filter(Blogs.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with this {id} not found")
    blog.title=blog_schema.title
    blog.bbody=blog_schema.body

    db.commit()
    db.refresh(blog)
    return blog
