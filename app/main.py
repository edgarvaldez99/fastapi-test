import uvicorn

from app import app
from app.dependencies import get_database_connection
from app.endpoints import api
from app.middlewares import AuditDatabaseMiddleware, AuditRequestMiddleware

app.add_middleware(
    AuditDatabaseMiddleware,
    database_connection_function=get_database_connection,
    excluded_routes=[],
)

app.add_middleware(
    AuditRequestMiddleware, database_connection_function=get_database_connection
)

app.include_router(api)


# Run Server
if __name__ == '__main__':
    uvicorn.run(app)
    # app.run(host="0.0.0.0", debug=True)
