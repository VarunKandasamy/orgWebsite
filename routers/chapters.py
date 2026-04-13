from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data.chapters import CHAPTER_LOCATIONS

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/chapters", response_class=HTMLResponse)
async def chapters(request: Request):
    return templates.TemplateResponse(
        request,
        "chapters/index.html",
        {"chapter_locations": CHAPTER_LOCATIONS},
    )
