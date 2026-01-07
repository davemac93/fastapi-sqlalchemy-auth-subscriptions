from fastapi import FastAPI
from app.api.auth import router as auth_user
from app.api.subscription import router as sub
from app.core.database import engine, Base

app = FastAPI()
app.include_router(auth_user)
app.include_router(sub)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def get_root():
    return {"message": "API is running"}