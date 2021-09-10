from app import app
from app.dependencies import get_database_connection
from app.endpoints import api
from app.middlewares import AuditDatabaseMiddleware, AuditRequestMiddleware

app.add_middleware(
    AuditDatabaseMiddleware,
    database_connection_function=get_database_connection,
    excluded_routes = []
)

app.add_middleware(
    AuditRequestMiddleware, database_connection_function=get_database_connection
)

app.include_router(api)
