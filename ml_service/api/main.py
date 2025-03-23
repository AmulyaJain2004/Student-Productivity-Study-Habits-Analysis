from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool
    
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item}