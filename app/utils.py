from passlib.context import CryptContext

Pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password: str):
    return Pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return Pwd_context.verify(plain_password,hashed_password)