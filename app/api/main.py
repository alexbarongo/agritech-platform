from fastapi import FastAPI
from api.routes import crops, expenses

app = FastAPI(
    title="AgriTech Platform",
    description="Farm Management API for Tanzania",
    version="1.0.0",
)

app.include_router(crops.router, prefix="/crops", tags=["Crops"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])


@app.get("/")
def root():
    return {"message": "AgriTech API is running"}
