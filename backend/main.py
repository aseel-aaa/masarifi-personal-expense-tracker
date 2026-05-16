from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routers import auth, expenses, categories
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Personal Expense Tracker API")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("JWT_SECRET"))

# Include Routers
app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(categories.router)

# Mount static files
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")

@app.get("/")
async def root():
    return FileResponse("frontend/login.html")

@app.get("/{file_name}.html")
async def serve_html(file_name: str):
    return FileResponse(f"frontend/{file_name}.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
