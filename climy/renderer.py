import datetime
import json
from decimal import Decimal
from enum import Enum
from json import JSONEncoder as BaseJSONEncoder
from typing import Any, Callable

from jinja2 import Environment, PackageLoader, select_autoescape

from climy.types import Command
from climy.utils import IncludeRawExtension

ENCODERS_BY_TYPE: dict[Any, Callable[[Any], Any]] = {
    bytes: lambda o: o.decode(),
    datetime.date: lambda o: o.isoformat(),
    datetime.datetime: lambda o: o.isoformat(),
    datetime.time: lambda o: o.isoformat(),
    datetime.timedelta: lambda td: td.total_seconds(),
    Decimal: lambda v: float(v),
    Enum: lambda o: o.value,
}


class JSONEncoder(BaseJSONEncoder):
    def default(self, obj) -> str:
        for base in obj.__class__.__mro__[:-1]:
            try:
                encoder = ENCODERS_BY_TYPE[base]
            except KeyError:
                continue
            return encoder(obj)
        else:
            return super().default(obj)


def json_dumps(obj: Any, *args, **kwargs):
    kwargs.setdefault("cls", JSONEncoder)
    return json.dumps(obj, *args, **kwargs)


def label_filter(value: str):
    return value.title().replace("_", " ").strip()


def setup_jinja_env() -> Environment:
    env = Environment(
        loader=PackageLoader("climy"),
        autoescape=select_autoescape(),
        extensions=[IncludeRawExtension],
    )
    env.filters["label"] = label_filter
    env.policies["json.dumps_function"] = json_dumps
    return env


def render_command(env: Environment, cmd: Command) -> str:
    tmpl = env.get_template("layout.html")
    return tmpl.render(cmd=cmd)
