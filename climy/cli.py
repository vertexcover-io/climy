import importlib
import sys
import webbrowser
from multiprocessing import Process
from typing import Optional

import click

from climy.core import create_user_interface, invoke_command
from climy.renderer import setup_jinja_env
from climy.server import start_server
from climy.types import CommandLine, CommandLineArg


def show_error(msg: str) -> None:
    click.echo(click.style(msg, fg="red"))
    sys.exit(1)


@click.group
def cli():
    pass


@cli.command(help="Create a Form UI from a `click` CLI Command")
@click.option("-h", "--host", default="0.0.0.0")
@click.option("-p", "--port", default=8080)
@click.argument("cli_app")
def serve(cli_app: str, host: str, port: int):
    process = Process(
        target=start_server,
        kwargs={
            "cli_app": cli_app,
            "host": host,
            "port": port,
        },
    )
    process.start()
    webbrowser.open(f"{host}:{port}")
    process.join()


@cli.command(help="Create a Form UI from a `click` CLI Command")
@click.argument("click_app")
@click.option("-o", "--output-file", help="Output file to store cli ui", required=False)
def app_ui(click_app: str, output_file: Optional[str] = None) -> None:
    try:
        module_name, cmd_name = click_app.rsplit(".", 1)
    except ValueError:
        return show_error(
            "Unable to load click command. App name must be passed as `<module_name>.<command_name>`"
        )

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        return show_error(
            f"Unable to load click command. Module {module_name} not found"
        )

    try:
        click_cmd = getattr(module, cmd_name)
    except AttributeError:
        return show_error(f"Unable to load click command. Command {cmd_name} not found")
    click.echo("Click Command Found")

    env = setup_jinja_env()
    ui = create_user_interface(env, click_cmd)
    if output_file is not None:
        with open(output_file, "w") as fd:
            fd.write(ui)
    else:
        sys.stdout.write(ui)


@cli.command(
    help="Invoke specified command with args",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.argument("app")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def invoke(app: str, args: list[str]):
    print(type(app), app)
    cmd_args = []
    current_arg = None
    for arg in args:
        if arg.startswith("-"):
            current_arg = CommandLineArg(name=arg.replace("-", ""), decl=arg, values=[])
        elif current_arg is not None:
            current_arg.values.append(arg)
            cmd_args.append(current_arg)
            current_arg = None
        else:
            cmd_args.append(CommandLineArg(name=arg, values=[arg]))

    print(cmd_args)
    cmd_line = CommandLine(target=["python", "-u"], src_script=app, arguments=cmd_args)
    for op in invoke_command(cmd_line):
        print(op)


if __name__ == "__main__":
    cli()
