from contextlib import asynccontextmanager
from http.client import responses

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.database import create_tables, migrate_crops_table, migrate_expenses_table

from api.routes import auth, crops, expenses


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    migrate_crops_table()
    migrate_expenses_table()
    yield


app = FastAPI(
    title="AgriTech Platform",
    description="Farm Management API for Tanzania",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(crops.router, prefix="/crops", tags=["Crops"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])


@app.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")
