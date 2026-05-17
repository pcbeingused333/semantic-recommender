from pydantic import BaseModel
from typing import Optional, Dict, Any

class ItemBase(BaseModel):
    title: str
    description: str
    category: str
    metadata: Optional[Dict[str, Any]] = None


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int
    similarity: Optional[float] = None

    class Config:
        from_attributes = True


class RecommendationRequest(BaseModel):
    query: str
    category: Optional[str] = None
    top_k: int = 10


class FeedbackCreate(BaseModel):
    user_id: str = "default_user"
    item_id: int
    rating: float                    # 1-5 o -1 (dislike) / 1 (like)
    feedback_text: Optional[str] = None