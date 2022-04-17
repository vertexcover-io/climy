from typing import Union

import click.types
from click.core import Command as ClickCommand
from click.core import Parameter as ClickParameter

from climy.types import Command, Parameter, ParamType

SupportedCommand = Union[ClickCommand]


def parse_click_param_type(param_type: click.types.ParamType) -> ParamType:
    if isinstance(param_type, click.types.StringParamType):
        return ParamType.String
    elif isinstance(param_type, click.types.IntParamType):
        return ParamType.Int
    elif isinstance(param_type, click.types.FloatParamType):
        return ParamType.Float
    elif isinstance(param_type, click.types.BoolParamType):
        return ParamType.Bool
    elif isinstance(param_type, click.types.Choice):
        return ParamType.Choice
    elif isinstance(param_type, click.types.DateTime):
        return ParamType.Dateime
    elif isinstance(param_type, click.types.IntRange):
        return ParamType.IntRange
    elif isinstance(param_type, click.types.FloatRange):
        return ParamType.FloatRange

    elif isinstance(param_type, (click.types.Path, click.types.Tuple)):
        return ParamType.Tuple
    elif isinstance(param_type, (click.types.Path, click.types.File)):
        return ParamType.File
    elif isinstance(param_type, click.types.UUID):
        return ParamType.Uuid
    else:
        return ParamType.Unknown


def parse_click_parameter(param: ClickParameter) -> Parameter:
    return Parameter(
        name=param.name,
        human_readable_name=param.human_readable_name,
        decl=param.opts[0],
        type_=parse_click_param_type(param.type),
        help=getattr(param, "help", None),
        default=param.default,
        required=param.required,
        count=param.nargs,
        multiple=param.multiple,
    )


def parse_click_command(
    cmd: ClickCommand, group_params: list[Parameter] = None
) -> Command:
    params = [parse_click_parameter(p) for p in (cmd.params or [])]
    group_params = group_params or []
    subcommands = [
        parse_click_command(c, group_params=params + group_params)
        for c in getattr(cmd, "commands", [])
    ]
    return Command(
        name=cmd.name,
        help=cmd.help,
        epilog=cmd.epilog,
        is_runnable=getattr(cmd, "invoke_without_command", True),
        group_params=group_params,
        params=params,
        subcommands=subcommands,
    )


def parse_command(sup_cmd: SupportedCommand):
    if isinstance(sup_cmd, ClickCommand):
        return parse_click_command(sup_cmd)

    raise RuntimeError(f"CLI Command of type: {type(sup_cmd)} not supported yet ")
