from typing import Optional

import click.types
from click.core import Command as ClickCommand
from click.core import Option as ClickOption
from click.core import Parameter as ClickParameter

from climy.types import CLIParser, Command, Parameter, ParamType, ParamValueType


def parse_click_param_type(param_type: click.types.ParamType) -> ParamValueType:
    if isinstance(param_type, click.types.StringParamType):
        return ParamValueType.String
    elif isinstance(param_type, click.types.IntParamType):
        return ParamValueType.Int
    elif isinstance(param_type, click.types.FloatParamType):
        return ParamValueType.Float
    elif isinstance(param_type, click.types.BoolParamType):
        return ParamValueType.Bool
    elif isinstance(param_type, click.types.Choice):
        return ParamValueType.Choice
    elif isinstance(param_type, click.types.DateTime):
        return ParamValueType.Dateime
    elif isinstance(param_type, click.types.IntRange):
        return ParamValueType.IntRange
    elif isinstance(param_type, click.types.FloatRange):
        return ParamValueType.FloatRange

    elif isinstance(param_type, (click.types.Path, click.types.Tuple)):
        return ParamValueType.Tuple
    elif isinstance(param_type, (click.types.Path, click.types.File)):
        return ParamValueType.File
    elif isinstance(param_type, click.types.UUIDParameterType):
        return ParamValueType.Uuid
    else:
        return ParamValueType.Unknown


def parse_click_parameter(param: ClickParameter) -> Parameter:
    assert param.name is not None
    return Parameter(
        name=param.name,
        human_readable_name=param.human_readable_name,
        param_type=ParamType.Option
        if isinstance(param, ClickOption)
        else ParamType.Argument,
        decl=param.opts[0],
        value_type=parse_click_param_type(param.type),
        help=getattr(param, "help", None),
        default=param.default,
        required=param.required,
        count=param.nargs,
        multiple=param.multiple,
    )


def parse_click_command(
    cmd: ClickCommand, group_params: Optional[list[Parameter]] = None
) -> Command:
    params = [parse_click_parameter(p) for p in (cmd.params or [])]
    group_params = group_params or []
    subcommands = [
        parse_click_command(c, group_params=params + group_params)
        for c in getattr(cmd, "commands", [])
    ]
    assert cmd.name is not None
    return Command(
        name=cmd.name,
        help=cmd.help,
        epilog=cmd.epilog,
        is_runnable=getattr(cmd, "invoke_without_command", True),
        group_params=group_params,
        params=params,
        subcommands=subcommands,
    )


def parse_command(sup_cmd: CLIParser) -> Command:
    if isinstance(sup_cmd, ClickCommand):
        return parse_click_command(sup_cmd)

    raise RuntimeError(f"CLI Command of type: {type(sup_cmd)} not supported yet ")
