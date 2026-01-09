from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_user
from app.api.subscription import router as sub
from app.core.database import engine, Base
from app.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_user)
app.include_router(sub)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def get_root():
    return {"message": "API is running"}