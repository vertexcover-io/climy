from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional, Union

from click.core import Command as ClickCommand
from dataclasses_json import dataclass_json

from climy.utils import ExtendedEnum as Enum

CLIParser = Union[ClickCommand]


class ParamValueType(Enum):
    String = "string"
    Int = "int"
    Float = "float"
    Bool = "bool"
    Choice = "choice"
    Dateime = "datetime"
    IntRange = "int_range"
    FloatRange = "float_range"
    DatetimeRange = "datetime_range"
    Tuple = "tuple"
    Uuid = "uuid"
    File = "file"
    Unknown = "unknown"


class CLIParserType(Enum):
    ArgParser = "argparse"
    Click = "click"


class ParamType(Enum):
    Argument = "argument"
    Option = "option"


class LoaderType(Enum):
    Jinja = "jinja2"


@dataclass
class Widget:
    name: str
    path: str
    loader: LoaderType = LoaderType.Jinja


@dataclass
class Parameter:
    name: str
    human_readable_name: str
    param_type: ParamType
    decl: Optional[str]
    value_type: ParamValueType = field(default=ParamValueType.String)
    widget: Widget = field(init=False)
    help: Optional[str] = field(default=None)
    default: Any = field(default=None)
    required: bool = field(default=False)
    count: int = field(default=1)

    def __post_init__(self) -> None:
        self.widget = get_widget_for_param(self)


@dataclass
class Command:
    name: str
    params: list[Parameter] = field(default_factory=list)
    group_params: list[Parameter] = field(default_factory=list)
    subcommands: list["Command"] = field(default_factory=list)
    parent_cmd: Optional[str] = field(default=None)
    help: Optional[str] = field(default=None)
    epilog: Optional[str] = field(default=None)
    is_runnable: bool = field(default=True)

    def dict(self):
        return asdict(self)


@dataclass
class ExecutionConifg:
    src_script: Path
    parser_type: CLIParserType
    command: Command
    target: list[str] = field(default_factory=lambda: ["python", "-u"])


@dataclass_json
@dataclass
class CommandLineArg:
    name: str
    values: list[Any]
    decl: Optional[str] = None


@dataclass_json
@dataclass
class CommandLine:
    src_script: str
    target: list[str] = field(default_factory=list)
    commands: list[str] = field(default_factory=list)
    arguments: list[CommandLineArg] = field(default_factory=list)


Textbox = Widget("Text", "widgets/textbox.html")
Checkbox = Widget("Checkbox", "widgets/checkbox.html")
Selector = Widget("Select", "widgets/selector.html")
DatetimePicker = Widget("Select", "widgets/datetime-picker.html")
FilePicker = Widget("Select", "widgets/file-picker.html")
NumericRange = Widget("Select", "widgets/numeric-range.html")
DatetimeRangePicker = Widget("Select", "widgets/datetime-range-picker.html")


def get_widget_for_param(param: Parameter) -> Widget:
    if param.value_type == ParamValueType.Bool:
        return Checkbox
    elif param.value_type == ParamValueType.Choice:
        return Selector
    elif param.value_type in (
        ParamValueType.String,
        ParamValueType.Int,
        ParamValueType.Float,
        ParamValueType.Uuid,
        ParamValueType.Unknown,
    ):
        return Textbox
    elif param.value_type == ParamValueType.Dateime:
        return DatetimePicker
    elif param.value_type == ParamValueType.File:
        return FilePicker
    elif param.value_type == ParamValueType.DatetimeRange:
        return DatetimeRangePicker
    elif param.value_type in (ParamValueType.IntRange, ParamValueType.FloatRange):
        return NumericRange
    else:
        raise ValueError(f"No supported widget for {param.value_type}")
