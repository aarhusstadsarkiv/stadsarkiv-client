import click
import uvicorn


@click.command()
@click.option('--reload', default=True, help='Reload uvicorn on changes.')
@click.option('--port', default=5555, help='Server port.')
@click.option('--workers', default=1, help='Number of workers.')
def run(reload: bool, port: int, workers: int):

    uvicorn.run("stadsarkiv_client.app:app",
                reload=reload, port=port, workers=workers, log_level="info")
