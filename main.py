from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import home, news, research, chapters, about, contact, newsletter

app = FastAPI(title="Demopolis Coalition")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home.router)
app.include_router(news.router)
app.include_router(research.router)
app.include_router(chapters.router)
app.include_router(about.router)
app.include_router(contact.router)
app.include_router(newsletter.router)
