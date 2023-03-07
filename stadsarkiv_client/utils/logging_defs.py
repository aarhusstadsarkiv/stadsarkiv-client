import logging
import os
from pathlib import Path
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def generate_log_dir():
    dir = "./logs"
    os.makedirs(dir, exist_ok=True)
    Path('./logs/main.log').touch()


def get_file_handler(level: int):
    fh = logging.FileHandler('logs/main.log')
    fh.setLevel(level)
    fh.setFormatter(formatter)
    return fh


def get_stream_handler(level: int):
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    return ch
