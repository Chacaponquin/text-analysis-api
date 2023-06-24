from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.router import app_router

app = FastAPI()
app.include_router(app_router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


