from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ParamType(Enum):
    String = "string"
    Int = "int"
    Float = "float"
    Bool = "bool"
    Choice = "choice"
    Datetime = "datetime"
    IntRange = "int_range"
    FloatRange = "float_range"
    Tuple = "tuple"
    Uuid = "uuid"
    File = "file"
    Unknown = "unknown"


class CLIType(Enum):
    ArgParser = "argparse"
    Click = "click"


@dataclass
class Parameter:
    name: str
    decl: str
    type_: ParamType = field(default=ParamType.STRING)
    help: str = field(default=None)
    default: Any = field(default=None)
    required: bool = field(default=False)
    multiple: bool = field(default=False)


@dataclass
class Command:
    name: str
    params: list[Parameter]
    help: str = field(default=None)
    epilog: str = field(default=None)
