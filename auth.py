import bcrypt
from sqlalchemy.orm import Session
from models import User
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from fastapi import HTTPException

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def registerUser(db: Session, user_id: str, name: str, email: str, password: str):
    existing_email = db.query(User).filter(User.email == email).first()
    existing_id = db.query(User).filter(User.id == user_id).first()
    if existing_email or existing_id:
        raise HTTPException(status_code=400, detail="User with this email or ID already exists")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(id=user_id, name=name, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user": new_user}

def authenticateAndToken(db: Session, identifier: str, password: str):
    user = db.query(User).filter((User.email == identifier) | (User.id == identifier)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(data={"sub": user.id})
        return {"message": "Authentication successful", "access_token": access_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    
def deleteUser(db: Session, identifier: str, password: str):
    user = db.query(User).filter((User.email == identifier) | (User.id == identifier)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")  