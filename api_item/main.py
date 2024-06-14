from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Item

app = FastAPI()

@app.get("/items/")
async def read_items():
    session = SessionLocal()
    items = session.query(Item).all()
    return {"items": [{"id": item.id, "name": item.name, "description": item.description} for item in items]}

@app.post("/items/")
async def create_item(item: Item):
    session = SessionLocal()
    session.add(item)
    session.commit()
    return {"id": item.id, "name": item.name, "description": item.description}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    session = SessionLocal()
    item = session.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item.id, "name": item.name, "description": item.description}