from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
import datetime
import os
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
# import jwt

SECRET_KEY = "secreto_super_seguro"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: str):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    return jwt.encode({"sub": user_id, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload.get('sub'))
        user_id: str = payload.get("sub")  # 🔹 Extrae el user_id en vez del email
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return  user_id  # 🔹 Devuelve el ID del usuario
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
