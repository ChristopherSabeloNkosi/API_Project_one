from datetime import timedelta
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import  status, HTTPException, Depends, APIRouter
from .. import  models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import  get_db

router =APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f'Invelid Credentials')
    if not utils.verify(user_credentials.password, user.Password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
   
    access_token = oauth2.create_access_token(data={'user_id': user.id})
    # return{'access_token': access_token, 'token_type': 'bearer'}
    return {"access_token": access_token, "token_type": "bearer"}