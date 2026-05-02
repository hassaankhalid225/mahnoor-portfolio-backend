from pydantic import BaseModel
from typing import List

class VideoLinkBase(BaseModel):
    title: str
    url: str
    youtube_id: str
    type: str # "video" or "short"
    order: int

class VideoLinkCreate(VideoLinkBase):
    pass

class VideoLinkUpdateOrder(BaseModel):
    id: int
    order: int

class VideoLinkResponse(VideoLinkBase):
    id: int

    class Config:
        from_attributes = True

class PosterResponse(BaseModel):
    id: int
    public_id: str
    secure_url: str
    order: int

    class Config:
        from_attributes = True

class PosterUpdateOrder(BaseModel):
    id: int
    order: int

class PosterSyncItem(BaseModel):
    public_id: str
    secure_url: str
