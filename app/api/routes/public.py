from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.auth import get_current_user
from services.database import (
    add_news,
    delete_news,
    get_crops_by_region,
    get_price_trends,
    get_public_stats,
    get_top_crops_by_price,
)

router = APIRouter()

# PUBLIC ENDPOINTS - no authentication required


@router.get("/stats")
def public_stats():
    return get_public_stats()


@router.get("/top-crops")
def top_crops():
    data = get_top_crops_by_price()
    return [
        {"name": row[0], "avg_price": row[1], "count": row[2], "total_harvest": row[3]}
        for row in data
    ]


@router.get("/regions")
def crops_by_region():
    data = get_crops_by_region()
    return [
        {"region": row[0], "crop_count": row[1], "total_harvest": row[2]}
        for row in data
    ]


@router.get("/price-trends")
def price_trends():
    data = get_price_trends()
    return [{"crop_name": row[0], "price": row[1], "date": row[2]} for row in data]


@router.get("/news")
def get_news_public():
    data = get_new()
    return [
        {
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "author": row[3],
            "created_at": row[4],
        }
        for row in data
    ]


# ADMIN ENDPOINTS - authentication required


class NewsRequest(BaseModel):
    title: str
    content: str
    author: str = "AgriTech Team"


@router.post("/news")
def create_news(request: NewsRequest, current_user: dict = Depends(get_current_user)):
    add_news(request.title, request.content, request.author)
    return {"message": "News published successfully"}


@router.delete("/news/{news_id}")
def remove_news(news_id: int, current_user: dict = Depends(get_current_user)):
    delete_news(news_id)
    return {"message": "News Deleted"}
