import click
import uvicorn
import os
from stadsarkiv_client.utils.dynamic_settings import settings
from stadsarkiv_client.utils.logging import log

@click.command()
@click.option('--reload', default=True, help='Reload uvicorn on changes.')
@click.option('--port', default=5555, help='Server port.')
def run(reload: bool, port: int):
    log.debug(os.getenv('ENVIRONMENT'))
    log.debug(settings)

    uvicorn.run("stadsarkiv_client.app:app",
                reload=reload, port=port, log_level="info")

