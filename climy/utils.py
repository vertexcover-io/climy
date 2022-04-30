import importlib
from typing import Any


def import_from_string(app: str) -> Any:
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
        return getattr(module, cmd_name)
    except AttributeError:
        raise ValueError(f"Unable to load click command. Command {cmd_name} not found")
