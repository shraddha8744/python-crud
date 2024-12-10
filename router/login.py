from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import Login
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import User
from ..router import user
from passlib.context import CryptContext
from ..JWTtoken import create_acess_token


login_router=APIRouter(
    tags=["/Authentication"]
)
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

@login_router.post("/login")
def login(user:OAuth2PasswordRequestForm=Depends() , db: Session = Depends(get_db)):
    print(user.username)
    u = db.query(User).filter(User.email == user.username).first()
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email")
    
    if not pwd_context.verify(user.password, u.password):  # Correct order
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    # generate  token
    acess_token=create_acess_token(data={"sub":u.email})
    
    return {"message": "Login successful","token":acess_token,"token_type":"bearer"}

