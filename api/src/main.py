from fastapi import FastAPI
from src.db.db import engine
from src.routes import charger_sessions, ping

app = FastAPI()


@app.on_event("shutdown")
async def shutdown():
    # Need to explicitly dispose engine to cleanup all connections. This is
    # required since in non-blocking I/O, SQLAlchemy can't automatically
    # determine a good time to invoke await.
    await engine.dispose()


app.include_router(ping.router)
app.include_router(
    charger_sessions.router, prefix="/charging-sessions", tags=["charging-sessions"]
)
