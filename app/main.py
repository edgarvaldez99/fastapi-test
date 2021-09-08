from app import app
from app.endpoints import api

app.include_router(api)
