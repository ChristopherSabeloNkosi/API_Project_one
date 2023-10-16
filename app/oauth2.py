from jose import JWTError,jwt
from datetime import datetime, time, timedelta
from fastapi import Depends, status, HTTPException
from app import models, schemas
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from sqlalchemy.orm import Session
from app import database
from app.database import SessionLocal, get_db
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# ALGORITHM
# EXPRIATION TIME

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
     to_encode = data.copy()
     expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
     to_encode.update({'exp': expire})
   
     encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
     return encoded_jwt
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Default token expiration

#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt, expire 

def verify_access_token(token: str, credentials_exception):
    # try:
    #      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #      id: str  =  payload.get('user_id')
    #      if id is None:
    #          raise credentials_exception
    #      token_data = schemas.TokenData(id=id)
    # except JWTError:
    #    raise credentials_exception
   
    # return token_data

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get('user_id')
        
        if id is None:
            raise credentials_exception
        
        # Check token expiration
        if "exp" in payload:
            expiration_timestamp = payload["exp"]
            current_timestamp = datetime.utcnow().timestamp()
            if expiration_timestamp < current_timestamp:
                raise credentials_exception
        
        token_data = schemas.TokenData(id= id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data


   

def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f'Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user 

# from jose import JWTError, jwt
# from datetime import datetime, timedelta, timezone
# from fastapi import Depends, status, HTTPException
# from app import schemas
# from fastapi.security import OAuth2PasswordBearer
# from typing import Optional

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# # SECRET_KEY (Make sure it's the same as used for token generation)
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 1  # Tokens will expire after 2 minutes

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now() + expires_delta
#     else:
#         expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Default token expiration
 

#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt, expire

# def verify_access_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get('user_id')
        
#         if user_id is None:
#             raise credentials_exception
        
#         # Check token expiration
#         if "exp" in payload:
#             expiration_timestamp = payload["exp"]
#             current_timestamp = datetime.now()
#             if expiration_timestamp < current_timestamp:
#                 raise credentials_exception
        
#         token_data = schemas.TokenData(id=user_id)
    
#     except JWTError:
#         raise credentials_exception
    
#     return token_data

# def get_current_user(token:str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})

#     return verify_access_token(token, credentials_exception)

