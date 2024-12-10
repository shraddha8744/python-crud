from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .JWTtoken import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print("token data",token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify token and return user data
    return verify_token(token, credentials_exception)
