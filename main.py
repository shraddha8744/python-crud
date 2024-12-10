from fastapi import FastAPI
from .database import Base,engine
Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware
from .router import blog,user,login

app=FastAPI()
# Allow CORS (Cross-Origin Resource Sharing)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[" http://localhost:5173"],  # Replace with your React app's URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.include_router(login.login_router)


app.include_router(blog.blog_router)
app.include_router(user.user_router)

@app.get("/")
def root():
    return {"msg":"Server Started"}




