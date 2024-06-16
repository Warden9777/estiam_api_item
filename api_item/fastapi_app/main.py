from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from model import Item
from typing import List
from pydantic import BaseModel

app = FastAPI()

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

@app.get("/items/", response_model=List[ItemResponse])
async def read_items():
    session = SessionLocal()
    items = session.query(Item).all()
    return [{"id": item.id, "name": item.name, "description": item.description} for item in items]

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    session = SessionLocal()
    session.add(item)
    session.commit()
    return {"id": item.id, "name": item.name, "description": item.description}

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    session = SessionLocal()
    item = session.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item.id, "name": item.name, "description": item.description}