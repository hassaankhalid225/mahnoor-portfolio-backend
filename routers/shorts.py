from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from bson import ObjectId
from database import shorts_collection

router = APIRouter(prefix="/shorts", tags=["shorts"])

# ── Schemas ──────────────────────────────────────────────
class ShortCreate(BaseModel):
    title: str
    url: str
    youtube_id: str
    order: int = 0

class ShortUpdateOrder(BaseModel):
    id: str
    order: int

def fmt(doc) -> dict:
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# ── Routes ───────────────────────────────────────────────
@router.get("/")
async def get_shorts():
    shorts = []
    async for s in shorts_collection.find().sort("order", 1):
        shorts.append(fmt(s))
    return shorts

@router.post("/")
async def create_short(short: ShortCreate):
    data = short.model_dump()
    result = await shorts_collection.insert_one(data)
    return fmt(data)

@router.put("/reorder")
async def reorder_shorts(updates: List[ShortUpdateOrder]):
    for u in updates:
        await shorts_collection.update_one(
            {"_id": ObjectId(u.id)},
            {"$set": {"order": u.order}}
        )
    return {"message": "Order updated successfully"}

@router.delete("/{short_id}")
async def delete_short(short_id: str):
    result = await shorts_collection.delete_one({"_id": ObjectId(short_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Short not found")
    return {"message": "Deleted successfully"}
