from fastapi import FastAPI
from app.api.channel_api import channels_router

app = FastAPI()
app.include_router(channels_router)
