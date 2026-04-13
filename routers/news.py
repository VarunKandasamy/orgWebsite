from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data.news import NEWS_ITEMS

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/news", response_class=HTMLResponse)
async def news(request: Request):
    return templates.TemplateResponse(request, "news.html", {"news_items": NEWS_ITEMS})
