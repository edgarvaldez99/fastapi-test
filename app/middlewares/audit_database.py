from types import FunctionType
from typing import List

from fastapi import FastAPI, Request
from starlette.datastructures import FormData  # type: ignore
from starlette.middleware.base import BaseHTTPMiddleware

from app import logger
from app.constants import AUTHORIZATION
from app.services import get_user_from_request


class AuditDatabaseMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        *,
        database_connection_function: FunctionType,
        excluded_routes: List[str]
    ):
        if database_connection_function is None:
            raise ValueError("Params database_connection_function is required")
        super().__init__(app)
        self.get_db_conn_func_tuple = (database_connection_function,)
        self.excluded_routes = excluded_routes

    def is_router_included(self, router: str) -> bool:
        return len(self.excluded_routes) == 0 or any(
            router in router_path for router_path in self.excluded_routes
        )

    async def dispatch(self, request: Request, call_next):
        if (
            self.is_router_included(request.url.path)
            and AUTHORIZATION in request.headers
        ):
            user = get_user_from_request(request, self.get_db_conn_func_tuple[0])
            if user:
                body: FormData = await request.form()
                if body:
                    new_body = dict(body)
                    new_body["modified_by"] = user.email
                    logger.info(new_body)
                    # request.body = new_body
        response = await call_next(request)
        return response
