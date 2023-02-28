import click
from .cli import serve

@click.command()
@click.option('--reload', default=True, help='Reload uvicorn on changes.')
@click.option('--port', default=5555, help='Server port.')
def run(reload: bool, port: int):
    serve(reload=reload, port=port)

""" if __name__ == "__main__":
    run() """