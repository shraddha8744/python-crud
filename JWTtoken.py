from jose import JWTError,jwt
from datetime import datetime,timedelta
from jwt.exceptions import InvalidTokenError
from .schemas import TokenData


SECRET_KEY="SHRADDHA"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_acess_token(data:dict):
    to_encode=data.copy()
    

    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt       



def verify_token(token: str, credentials_exception):
    try:
        print(f"Verifying token: {token}")  # Log token value
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload: {payload}")  # Log payload
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(email=email)
    except Exception as e:
        print(f"Error verifying token: {e}")  # Log error details
        raise credentials_exception
