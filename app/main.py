from app import app
from app.dependencies import get_database_connection
from app.middlewares import AuditRequestMiddleware
from app.endpoints import api

app.add_middleware(
    AuditRequestMiddleware, 
    database_connection_function=get_database_connection
)

app.include_router(api)
