from fastapi import FastAPI
from app.api.channel_api import channelsRouter

app = FastAPI()
app.include_router(channelsRouter)
