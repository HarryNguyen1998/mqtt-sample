from fastapi import FastAPI

from src.routes import ping

app = FastAPI()

app.include_router(ping.router)
