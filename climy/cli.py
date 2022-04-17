import importlib
import sys
from typing import Optional

import click

from climy.core import create_user_interface


def show_error(msg: str) -> None:
    click.echo(click.style(msg, fg="red"))
    sys.exit(1)


@click.command(help="Create a Form UI from a `click` CLI Command")
@click.argument("click_app")
@click.option("-o", "--output-file", help="Output file to store cli ui", required=False)
def main(click_app: str, output_file: Optional[str] = None) -> None:
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

    ui = create_user_interface(click_cmd)
    if output_file is not None:
        with open(output_file, "w") as fd:
            fd.write(ui)
    else:
        sys.stdout.write(ui)
