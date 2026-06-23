from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from jose import jwt, JWTError

from . import database as db
from .dependencies import ADMIN_PASSWORD, ADMIN_JWT_SECRET_KEY
from pwdlib import PasswordHash

ALGORITHM = "HS256"
ACCESS_EXPIRE_TIME = 30 # 30 minutes for testing

password_hash = PasswordHash.recommended()

# create one admin account if there aren't any in the db
with db.SessionLocal() as session:
    if session.query(db.Admin).count() == 0:
        admin = db.Admin(name="admin", hashed_password=password_hash.hash(ADMIN_PASSWORD.get_secret_value()))
        session.add(admin)
        session.commit()

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/admin_token")

class Token(BaseModel):
    access_token: str
    token_type: str
    
@router.post("/admin_token", response_model=Token)
def get_token(form: Annotated[OAuth2PasswordRequestForm, Depends()], session: db.SessionDep):
    username = form.username
    password = form.password
    
    print(username, password)
    user = authenticate_admin(username, password, session)
    print(user)
    if not user:
        raise HTTPException(401, "Could not validate user.")

    access_token = create_access_token(user.username, user.id, timedelta(minutes=ACCESS_EXPIRE_TIME))

    return Token(access_token=access_token, token_type="bearer")

def authenticate_admin(username: str, password: str, session: db.Session):
    user = session.query(db.Admin).filter(db.Admin.name == username).first()
    if not user:
        return False
    if password_hash.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, timedelta: timedelta):
    encode = {"sub": username, "id": user_id}
    exp = datetime.now(timezone.utc) + timedelta
    encode.update({"exp": exp})
    return jwt.encode(encode, ADMIN_JWT_SECRET_KEY.get_secret_value(), ALGORITHM)

async def get_current_admin(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, ADMIN_JWT_SECRET_KEY.get_secret_value(), ALGORITHM)
        username: str = payload.get("username")
        user_id: str = payload.get("id")
        
        if username is None or user_id is None:
            raise HTTPException(401, "Could not validate user.")
        
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(401, "Could not validate user.")


AdminDep = Annotated[dict, Depends(get_current_admin)]