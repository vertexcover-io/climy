from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class ParamType(Enum):
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


class CLIType(Enum):
    ArgParser = "argparse"
    Click = "click"


class LoaderType(Enum):
    Jinja = "jinja2"


@dataclass
class Widget:
    name: str
    path: Path
    loader: LoaderType = LoaderType.Jinja


@dataclass
class Parameter:
    name: str
    human_readable_name: str
    decl: str
    type_: ParamType = field(default=ParamType.String)
    widget: Widget = field(init=False)
    help: Optional[str] = field(default=None)
    default: Any = field(default=None)
    required: bool = field(default=False)
    count: int = field(default=1)
    multiple: bool = field(default=False)

    def __post_init__(self) -> None:
        self.widget = get_widget_for_param(self)


@dataclass
class Command:
    name: str
    params: list[Parameter] = field(default_factory=list)
    group_params: list[Parameter] = field(default_factory=list)
    subcommands: list["Command"] = field(default_factory=list)
    help: Optional[str] = field(default=None)
    epilog: Optional[str] = field(default=None)
    is_runnable: bool = field(default=True)


Textbox = Widget("Text", Path("widgets/textbox.html"))
Checkbox = Widget("Checkbox", Path("widgets/checkbox.html"))
Selector = Widget("Select", Path("widgets/selector.html"))
DatetimePicker = Widget("Select", Path("widgets/datetime-picker.html"))
FilePicker = Widget("Select", Path("widgets/file-picker.html"))
NumericRange = Widget("Select", Path("widgets/numeric-range.html"))
DatetimeRangePicker = Widget("Select", Path("widgets/datetime-range-picker.html"))


def get_widget_for_param(param: Parameter) -> Widget:
    if param.type_ == ParamType.Bool:
        return Checkbox
    elif param.type_ == ParamType.Choice:
        return Selector
    elif param.type_ in (
        ParamType.String,
        ParamType.Int,
        ParamType.Float,
        ParamType.Uuid,
        ParamType.Unknown,
    ):
        return Textbox
    elif param.type_ == ParamType.Dateime:
        return DatetimePicker
    elif param.type_ == ParamType.File:
        return FilePicker
    elif param.type_ == ParamType.DatetimeRange:
        return DatetimeRangePicker
    elif param.type_ in (ParamType.IntRange, ParamType.FloatRange):
        return NumericRange
    else:
        raise ValueError(f"No supported widget for {param.type_}")
