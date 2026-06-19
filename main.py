from fastapi import FastAPI 
from pydantic import BaseModel
from database import engine, Base, SessionLocal
from auth import registerUser, authenticateUser, deleteUser

Base.metadata.create_all(bind=engine)
class RegisterRequest(BaseModel):
    user_id: str
    name: str
    email: str
    password: str

class Item(BaseModel):
    name: str
    price: float 
    is_available: bool = True

synapse = FastAPI()
items_db = []

@synapse.get("/")
def home():
    return {"message": "Hello World"}

@synapse.get("/about")
def about():
    return {"message": "This is about page"}

@synapse.get("/user/{id}")
def user(id: int):
    return {"user_id": id}

@synapse.get("/search")
def search(q: str, page:int = 1, limit: int = 10):
    return {"query": q, "page": page, "limit": limit}

@synapse.post("/submit")
def create_item(item: Item):
    items_db.append(item)
    return {"received": item}

@synapse.get("/items")
def get_items():
    return {"items": items_db, "count": len(items_db)} 

@synapse.delete("/itemsDelete")
def delete_all_items():
    items_db.clear()  
    return {"message": "All items deleted", "items_remaining": len(items_db)}

@synapse.post("/signup")
def register_user(request: RegisterRequest):
    db = SessionLocal()
    response = registerUser(db, request.user_id, request.name, request.email, request.password)
    db.close()
    return response

@synapse.get("/login")
def authenticate_user(identifier: str, password: str):
    db = SessionLocal()
    response = authenticateUser(db, identifier, password)
    db.close()
    return response

@synapse.delete("/delete")
def delete_user(identifier: str, password: str):
    db = SessionLocal()
    response = deleteUser(db, identifier, password)
    db.close()
    return response