import importlib
from enum import Enum
from types import ModuleType
from typing import Any

from jinja2 import nodes
from jinja2.ext import Extension


def import_from_string(app: str) -> tuple[ModuleType, Any]:
    try:
        module_name, cmd_name = app.rsplit(":", 1)
    except ValueError:
        raise ValueError(
            "Unable to load click command. App name must be passed as `<module_name>.<command_name>`"
        )

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        raise ValueError(
            f"Unable to load click command. Module {module_name} not found"
        )

    try:
        parser = getattr(module, cmd_name)
    except AttributeError:
        raise ValueError(f"Unable to load click command. Command {cmd_name} not found")

    return module, parser


class IncludeRawExtension(Extension):
    """
    Taken from https://stackoverflow.com/a/64392515/911557
    """

    tags = {"include_raw"}

    def parse(self, parser):
        tag = min(self.tags)
        lineno = parser.stream.expect(f"name:{tag}").lineno
        filename = nodes.Const(parser.parse_expression().value)
        result = self.call_method("_load_source", [filename], lineno=lineno)
        markup = nodes.MarkSafe(result)
        return nodes.Output([markup], lineno=lineno)

    def _load_source(self, filename) -> str:
        return self.environment.loader.get_source(self.environment, filename)[0]


class IncludeBrythonScript(IncludeRawExtension):

    tags = {"include_brython"}

    def _load_source(self, filename) -> str:
        src = super()._load_source(filename)
        return f'<script type="text/python">{src}</script>'


class ExtendedEnum(Enum):
    def __eq__(self, o: object) -> bool:
        if isinstance(o, str):
            return self.value == o
        return super().__eq__(o)
