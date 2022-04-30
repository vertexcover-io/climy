import os
from dataclasses import dataclass
from functools import wraps
from typing import Callable

import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.routing import Route

from climy.parser import parse_command
from climy.renderer import render_command
from climy.types import Command
from climy.utils import import_from_string


@dataclass
class Config:
    cmd: Command


_View = Callable[[Request, Config], Response]


class ConfigMiddleware(BaseHTTPMiddleware):
    def __init__(self, config: Config, *args, **kwargs) -> None:
        self._config = config
        super().__init__(*args, **kwargs)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request.state.config = self._config
        return await call_next(request)


def wrap_view(view_fn: _View):
    @wraps(view_fn)
    def _view(request: Request) -> Response:
        return view_fn(request, request.state.config)

    return _view


def homepage(request: Request, config: Config):
    resp = render_command(config.cmd)
    return HTMLResponse(resp)


def create_app() -> Starlette:
    cli_app = os.environ["CLI_APP"]
    cli_parser = import_from_string(cli_app)
    cmd = parse_command(cli_parser)
    routes = [Route("/", wrap_view(homepage))]
    middleware = Middleware(ConfigMiddleware, config=Config(cmd))
    app = Starlette(debug=True, routes=routes, middleware=[middleware])
    return app


def start_server(cli_app: str, host: str, port: int):
    os.environ["CLI_APP"] = cli_app
    uvicorn.run(
        "climy.server:create_app",
        host=host,
        port=port,
        reload=True,
        debug=True,
        factory=True,
    )
