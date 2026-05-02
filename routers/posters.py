import os
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from database import posters_collection
from dotenv import load_dotenv

load_dotenv()

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

router = APIRouter(prefix="/posters", tags=["posters"])

# ── Schemas ──────────────────────────────────────────────
class PosterCreate(BaseModel):
    title: Optional[str] = ""
    image_url: str          # direct hosted image URL (Cloudinary, Drive, etc.)
    order: int = 0

class PosterUpdateOrder(BaseModel):
    id: str
    order: int

def fmt(doc) -> dict:
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# ── Routes ───────────────────────────────────────────────
@router.get("/")
async def get_posters():
    posters = []
    async for p in posters_collection.find().sort("order", 1):
        posters.append(fmt(p))
    return posters

@router.post("/")
async def add_poster(poster: PosterCreate):
    if not poster.image_url:
        raise HTTPException(status_code=400, detail="image_url is required")
    last = await posters_collection.find_one(sort=[("order", -1)])
    new_order = (last["order"] + 1) if last else 0
    doc = {
        "title": poster.title,
        "image_url": poster.image_url,
        "secure_url": poster.image_url,   # alias for frontend compatibility
        "public_id": poster.image_url,    # alias for frontend compatibility
        "order": new_order,
    }
    result = await posters_collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc

@router.put("/reorder")
async def reorder_posters(updates: List[PosterUpdateOrder]):
    for u in updates:
        await posters_collection.update_one(
            {"_id": ObjectId(u.id)},
            {"$set": {"order": u.order}}
        )
    return {"message": "Order updated"}

@router.delete("/{poster_id}")
async def delete_poster(poster_id: str):
    result = await posters_collection.delete_one({"_id": ObjectId(poster_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Poster not found")
    return {"message": "Deleted successfully"}

@router.post("/upload/")
async def upload_poster(file: UploadFile = File(...)):
    try:
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file.file,
            folder="portfolio/posters",
            tags=["Poster"]
        )
        
        # Save to MongoDB
        last = await posters_collection.find_one(sort=[("order", -1)])
        new_order = (last["order"] + 1) if last else 0
        
        doc = {
            "public_id": upload_result["public_id"],
            "secure_url": upload_result["secure_url"],
            "order": new_order,
            "title": file.filename
        }
        
        result = await posters_collection.insert_one(doc)
        doc["id"] = str(result.inserted_id)
        
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
