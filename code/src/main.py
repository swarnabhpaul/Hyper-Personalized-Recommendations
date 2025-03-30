from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_connection, close_connection
from api import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    init_connection()

@app.on_event("shutdown")
async def shutdown_event():
    close_connection()