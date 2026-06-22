import bcrypt
from fastapi import FastAPI 
from pydantic import BaseModel
from database import engine, Base, SessionLocal
from auth import AuthService as A

Base.metadata.create_all(bind=engine)
class RegisterRequest(BaseModel):
    user_id: str
    name: str
    email: str
    password: str

app = FastAPI(tittle = "Synapse AI", description = "Chat with your documents using AI or ask questions about your documents. Synapse AI is a powerful tool that allows you to interact with your documents in a natural and intuitive way. With Synapse AI, you can easily find the information you need, get answers to your questions, and gain insights from your documents.")

@app.get("/")
def home():
    return {"message": "This is the home page of Synapse AI."}

@app.get("/about")
def about():
    return {"message": "This is about page of Synapse AI."}

@app.get("/myProfile")
def user(token: str):
    db = SessionLocal()
    user = A.get_current_user(db, token)
    db.close()
    return {"message": "User profile retrieved successfully", "user": user, "email": user.email, "name": user.name, "id": user.id}

@app.post("/signup")
def register_user(request: RegisterRequest):
    db = SessionLocal()
    response = A.registerUser(db, request.user_id, request.name, request.email, request.password)
    db.close()
    return response

@app.get("/login")
def authenticate_user(identifier: str, password: str):
    db = SessionLocal()
    response = A.authenticateUser(db, identifier, password)
    db.close()
    return response

@app.delete("/delete")
def delete_user(token: str):
    db = SessionLocal()
    user = A.get_current_user(db, token)
    response = A.deleteUser(db, user.email, user.password)
    db.close()
    return {"message": "User deleted successfully"}

@app.post("/change-password")
def change_password(token: str, passwordOld: str, passwordNew: str):
    db = SessionLocal()
    response = A.changePassword(db, token, passwordOld, passwordNew)
    db.close()
    return response