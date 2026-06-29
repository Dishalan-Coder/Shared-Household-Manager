from fastapi import FastAPI
from app.config.database import client

app = FastAPI()


@app.on_event("startup")
async def startup():
    print("MongoDB Connected Successfully")


@app.on_event("shutdown")
async def shutdown():
    client.close()
    print("MongoDB Connection Closed")


@app.get("/")
async def home():
    return {"message": "Shared Household Manager API"}