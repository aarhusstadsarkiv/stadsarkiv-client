import logging
import os
from pathlib import Path
from settings import settings

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


dir = "./logs"
os.makedirs(dir, exist_ok=True)
Path('./logs/main.log').touch()


log = logging.getLogger("main")
level = settings["log_level"]

if not len(log.handlers):

    log.setLevel(level)
    fh = logging.FileHandler('logs/main.log')
    fh.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

log.warning("Logging initialized")