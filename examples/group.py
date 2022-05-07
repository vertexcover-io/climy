import os
import shutil

import click


@click.group(help="Shell Commands")
def shell():
    pass


@shell.command(help="List Files in Directory")
@click.argument("dirname", required=False, default=os.getcwd())
def ls(dirname: str):
    for f in os.listdir(dirname):
        print(f)


@shell.command(help="Move from SRC to DEST")
@click.argument("src", required=True)
@click.argument("dest", required=True)
def mv(src: str, dest: str):
    shutil.move(src, dest)
    print(f"Moved {src} to {dest}")


if __name__ == "__main__":
    shell()
