from fastapi import FastAPI 
from pydantic import BaseModel
from database import engine, Base
from models import User

Base.metadata.create_all(bind=engine)
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

@synapse.post("/dataUser")
def create_user(userid:str, name:str, email:str, password:str):
    new_user = User(id=userid, name=name, email=email, password=password)
    if(len(password)<8):
        return {"message": "Password must be at least 8 characters long"}
    with engine.begin() as conn:
        conn.execute(User.__table__.insert(), [new_user.__dict__])
    return {"message": "User created successfully", "user": new_user}

@synapse.delete("/deleteUser")
def delete_user(userid: str):
    with engine.begin() as conn:
        result = conn.execute(User.__table__.delete().where(User.id == userid))
    if result.rowcount:
        return {"message": f"User with id {userid} deleted successfully"}
    else:
        return {"message": f"No user found with id {userid}"}