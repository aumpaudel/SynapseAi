import bcrypt
from sqlalchemy.orm import Session
from models import User
from jose import jwt,JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from fastapi import HTTPException

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class AuthService:
    def get_current_user(db: Session, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user

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

    def authenticateUser(db: Session, identifier: str, password: str):
        user = db.query(User).filter((User.email == identifier) | (User.id == identifier)).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            access_token = AuthService.create_access_token(data={"sub": user.id})
            return {"message": "Authentication successful", "access_token": access_token}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        
    def deleteUser(db: Session, token: str, password: str):
        user =  AuthService.get_current_user(db, token)
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            db.delete(user)
            db.commit()
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")  
        
    def changePassword(db: Session, token: str, passwordOld: str, passwordNew: str):
        user =  AuthService.get_current_user(db, token)
        if bcrypt.checkpw(passwordOld.encode('utf-8'), user.password.encode('utf-8')):
            user.password = bcrypt.hashpw(passwordNew.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            db.commit()
            db.refresh(user)
            return {"message": "Password changed successfully"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")  