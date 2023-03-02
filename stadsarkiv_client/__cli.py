import uvicorn
import os
from stadsarkiv_client.utils.dynamic_settings import settings
from stadsarkiv_client.utils.logging import log


def serve(reload, port):

    log.debug(os.getenv('ENVIRONMENT'))
    log.debug(settings)

    uvicorn.run("stadsarkiv_client.app:app",
                reload=reload, port=port, log_level="info")
