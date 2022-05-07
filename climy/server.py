import os
import typing
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Callable, TypedDict

import jinja2
import uvicorn
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.routing import Route, WebSocketRoute
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.websockets import WebSocket

from climy.core import invoke_command
from climy.parser import parse_command
from climy.renderer import render_command, setup_jinja_env
from climy.types import CommandLine, ExecutionConifg
from climy.utils import import_from_string


@dataclass
class AppConfig:
    execution_config: ExecutionConifg
    env: jinja2.Environment

    @property
    def cmd(self):
        return self.execution_config.command


_View = Callable[[Request, AppConfig], Response]


class WSEventType(Enum):
    SUBMIT = "submit"
    LOG = "log"
    ERROR = "error"


class WSEvent(TypedDict):
    type: str
    payload: dict


class AppConfigMiddleware:
    def __init__(self, app: ASGIApp, config: AppConfig) -> None:
        self.app = app
        self._config = config

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        scope.setdefault("state", {})
        scope["state"]["config"] = self._config
        return await self.app(scope, receive, send)


def wrap_view(view_fn: _View):
    @wraps(view_fn)
    def _view(request: Request) -> Response:
        return view_fn(request, request.state.config)

    return _view


def homepage(_: Request, config: AppConfig):
    resp = render_command(config.env, config.cmd)
    return HTMLResponse(resp)


class WSEndpoint(WebSocketEndpoint):
    encoding = "json"

    async def on_receive(self, websocket: WebSocket, event_dict: WSEvent):
        config = typing.cast(AppConfig, websocket.state.config)
        event_type = event_dict["type"]
        if event_type == WSEventType.SUBMIT.value:
            cmdline = CommandLine.schema().load(  # type: ignore
                {
                    "target": config.execution_config.target,
                    "src_script": config.execution_config.src_script.as_posix(),
                    **event_dict["payload"],
                }
            )
            for line in invoke_command(cmdline):
                print(line)
                await websocket.send_json(
                    {"type": WSEventType.LOG.value, "payload": line.strip()}
                )
        else:
            print(f"Event {event_dict} not supported")
            websocket.send_json(
                {
                    "type": WSEventType.ERROR,
                    "payload": f"Unsupported event type: {event_type}",
                }
            )


def create_app() -> Starlette:
    cli_app = os.environ["CLI_APP"]
    module, cli_parser = import_from_string(cli_app)
    parser_type, cmd = parse_command(cli_parser)
    assert module.__file__ is not None
    config = ExecutionConifg(
        src_script=Path(module.__file__), parser_type=parser_type, command=cmd
    )
    jinja2_env = setup_jinja_env()
    app_config = AppConfig(execution_config=config, env=jinja2_env)
    routes = [Route("/", wrap_view(homepage)), WebSocketRoute("/ws", WSEndpoint)]
    middleware = Middleware(AppConfigMiddleware, config=app_config)
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
