import time

import click


@click.command()
@click.option("-v", "--verbose", count=True)
@click.argument("msg_list", nargs=-1, required=True)
@click.option("-s", "--sleep", type=click.FLOAT, default=0.5)
def hello(msg_list: list[str], sleep: float, verbose: int):
    """
    Print Hello Message
    """
    print(f"verbosity: {verbose}")
    print("Hello")
    for m in msg_list:
        time.sleep(sleep)
        print(m, end=" ", flush=True)


if __name__ == "__main__":
    print("Run Main")
    hello()
