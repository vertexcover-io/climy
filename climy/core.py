import subprocess
from typing import Generator

from climy.parser import parse_command
from climy.renderer import render_command
from climy.types import CLIParser, CommandLine, CommandLineArg


def create_user_interface(sup_cmd: CLIParser) -> str:
    cmd = parse_command(sup_cmd)
    print(cmd)
    return render_command(cmd)


def _prepare_cmd_arg(cmd_arg: CommandLineArg) -> list[str]:
    args = [cmd_arg.decl] if cmd_arg.decl else []
    args += list(str(val) for val in cmd_arg.values)
    return args


def _prepare_command_line(cmdline: CommandLine) -> list[str]:
    cmds = cmdline.target or []
    cmds += [cmdline.src_script.as_posix()]
    cmds += cmdline.commands[1:] if len(cmdline.commands) > 1 else []
    for arg in cmdline.arguments:
        cmds += _prepare_cmd_arg(arg)
    return cmds


def invoke_command(cmdline: CommandLine) -> Generator[str, None, int]:
    cmd_list = _prepare_command_line(cmdline)
    print(f"Executing Command: {cmd_list}")
    proc = subprocess.Popen(
        cmd_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    assert proc.stdout is not None
    for line in iter(lambda: proc.stdout.readline(), b""):  # type: ignore
        yield line.decode("utf-8").strip("\n")

    return proc.wait()
