import click
import importlib
import pkgutil
import os
pkgs = {}
currentDir = os.path.dirname(os.path.realpath(__file__))

for finder, name, ispkg in pkgutil.walk_packages([currentDir]):
    pkg = importlib.import_module(f"zro2.{name}")
    if not hasattr(pkg, "run"):
        continue

    pkgs[name] = pkg

@click.group()
def cli():
    pass

@cli.command()
def list():
    for name, pkg in pkgs.items():
        click.echo(name)

@cli.command()
@click.argument("name", type=click.STRING, shell_complete=lambda _, __: list(pkgs.keys()))
def run(name):
    if name not in pkgs:
        click.echo(f"Package {name} not found")
        return
    
    pkg = pkgs[name]
    pkg.run()

if __name__ == "__main__":
    cli()