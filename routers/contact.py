from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request, submitted: Optional[str] = None):
    return templates.TemplateResponse(
        request,
        "contact.html",
        {"submitted": submitted},
    )


@router.post("/contact/partnership")
async def contact_partnership(
    request: Request,
    name: str = Form(...),
    organization: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    # In production, send email or store to database
    return RedirectResponse(url="/contact?submitted=partnership", status_code=303)


@router.post("/contact/general")
async def contact_general(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
):
    # In production, send email or store to database
    return RedirectResponse(url="/contact?submitted=general", status_code=303)
