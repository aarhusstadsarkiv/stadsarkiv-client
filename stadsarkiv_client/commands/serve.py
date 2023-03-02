import click
import uvicorn
import os
from stadsarkiv_client.utils.dynamic_settings import settings
from stadsarkiv_client.utils.logging import log


@click.command()
@click.option('--reload', default=True, help='Reload uvicorn on changes.')
@click.option('--port', default=5555, help='Server port.')
@click.option('--workers', default=4, help='Number of workers.')
def run(reload: bool, port: int, workers: int):
    log.debug(os.getenv('ENVIRONMENT'))
    log.debug(settings)

    uvicorn.run("stadsarkiv_client.app:app",
                reload=reload, port=port, workers=workers, log_level="info")
