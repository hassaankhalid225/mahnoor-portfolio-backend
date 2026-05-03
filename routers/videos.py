from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from database import videos_collection

router = APIRouter(prefix="/videos", tags=["videos"])

# ── Schemas ──────────────────────────────────────────────
class VideoCreate(BaseModel):
    title: str
    url: str
    youtube_id: str
    order: int = 0

class VideoUpdateOrder(BaseModel):
    id: str
    order: int

def fmt(doc) -> dict:
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# ── Routes ───────────────────────────────────────────────
@router.get("/")
async def get_videos():
    videos = []
    async for v in videos_collection.find().sort("order", 1):
        videos.append(fmt(v))
    return videos

@router.post("/")
async def create_video(video: VideoCreate):
    data = video.model_dump()
    result = await videos_collection.insert_one(data)
    return fmt(data)

@router.put("/reorder")
async def reorder_videos(updates: List[VideoUpdateOrder]):
    for u in updates:
        await videos_collection.update_one(
            {"_id": ObjectId(u.id)},
            {"$set": {"order": u.order}}
        )
    return {"message": "Order updated successfully"}

@router.delete("/{video_id}")
async def delete_video(video_id: str):
    result = await videos_collection.delete_one({"_id": ObjectId(video_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"message": "Deleted successfully"}
