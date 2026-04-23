import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from services.database import create_tables, migrate_crops_table, migrate_expenses_table

from api.routes import auth, crops, expenses, profile, reports

TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "templates"
)


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

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(crops.router, prefix="/crops", tags=["Crops"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])


@app.get("/")
def landing():
    return FileResponse(os.path.join(TEMPLATES_DIR, "index.html"))


@app.get("/login")
def login_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "login.html"))


@app.get("/register")
def register_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "register.html"))


@app.get("/dashboard")
def dashboard_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "dashboard.html"))


@app.get("/crops-page")
def crops_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "crops.html"))


@app.get("/expenses-page")
def expenses_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "expenses.html"))


@app.get("/reports-page")
def reports_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "reports.html"))


@app.get("/profile-page")
def profile_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "profile.html"))
