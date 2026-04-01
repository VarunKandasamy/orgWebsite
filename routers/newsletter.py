from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()


class NewsletterSubscribe(BaseModel):
    email: str


@router.post("/newsletter/subscribe")
async def newsletter_subscribe(payload: NewsletterSubscribe):
    # In production, add to email list
    return JSONResponse({"status": "subscribed"})
