import uvicorn
import os
from stadsarkiv_client.utils.dynamic_settings import settings
from stadsarkiv_client.utils.logging import log

def serve():

    log.debug(os.getenv('ENVIRONMENT'))
    log.debug(settings)

    uvicorn.run("stadsarkiv_client.app:app",
                reload=True, port=5555, log_level="info")
