from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.research import LONGFORM_WORKS, CITIES
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")

TABS = ["what-we-do", "longform"]


@router.get("/research", response_class=HTMLResponse)
async def research_redirect():
    return RedirectResponse(url="/research/what-we-do")


@router.get("/research/{tab}", response_class=HTMLResponse)
async def research(request: Request, tab: str, city: Optional[str] = None):
    if tab not in TABS:
        return RedirectResponse(url="/research/what-we-do")

    filtered_longform = LONGFORM_WORKS
    if city and tab == "longform":
        filtered_longform = [w for w in LONGFORM_WORKS if w["city"] == city]

    return templates.TemplateResponse(
        request,
        "research/index.html",
        {
            "active_tab": tab,
            "longform_works": filtered_longform,
            "cities": CITIES,
            "selected_city": city,
        },
    )
