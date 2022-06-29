import os
import click
from lightning_pod.cli.utils import teardown
from lightning_pod.cli.utils import build
from rich import print as rprint
from lightning_pod.cli.utils import show_destructive_behavior_warning


@click.group()
def main():
    pass


def common_destructive_flow(commands: list, command_name: str):
    show_destructive_behavior_warning()
    if click.confirm("Do you want to continue"):
        for command in commands:
            command()
        print()
        rprint(f"[bold green]{command_name.title()} complete[bold green]")
        print()
    else:
        print()
        rprint("[bold green]No Action Taken[/bold green]")
        print()


@main.command("teardown")
def _teardown():
    common_destructive_flow([teardown], command_name="tear down")


# TODO add help description
@main.command("seed")
def seed():
    common_destructive_flow([teardown, build], command_name="seed")


@main.group("trainer")
def trainer():
    pass


# TODO add help description
@trainer.command("help")
def help():
    trainer = os.path.join("lightning_pod", "core", "trainer.py")
    os.system(f"python {trainer} --help")


# TODO add help description
@trainer.command("run")
@click.argument("hydra-args", nargs=-1)
def run_trainer(hydra_args):
    trainer = os.path.join("lightning_pod", "core", "trainer.py")
    hydra_args = list(hydra_args)
    hydra_args = [f"'trainer.{i}'" for i in hydra_args]
    hydra_args = " ".join(hydra_args)
    run_command = " ".join(["python", trainer, hydra_args])
    os.system(run_command)
