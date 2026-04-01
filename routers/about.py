from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.about import TEAM_MEMBERS, PARTNERS

router = APIRouter()
templates = Jinja2Templates(directory="templates")

TABS = ["mission", "what-we-do", "team", "partners"]


@router.get("/about", response_class=HTMLResponse)
async def about_redirect():
    return RedirectResponse(url="/about/mission")


@router.get("/about/{tab}", response_class=HTMLResponse)
async def about(request: Request, tab: str):
    if tab not in TABS:
        return RedirectResponse(url="/about/mission")

    return templates.TemplateResponse(
        "about/index.html",
        {
            "request": request,
            "active_tab": tab,
            "team_members": TEAM_MEMBERS,
            "partners": PARTNERS,
        },
    )
