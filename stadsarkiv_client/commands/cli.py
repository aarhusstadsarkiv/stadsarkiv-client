"""
File containing CLI commands for the Stadsarkiv Client.
"""

import click
import subprocess
import os
import secrets
import glob
import sys
import logging
from stadsarkiv_client.core import logging_handlers
from stadsarkiv_client import __version__, __program__


logging_handlers.generate_log_dir()
logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)
rotating_file_handler = logging_handlers.get_rotating_file_handler(logging.INFO, "logs/server.log")
stream_handler = logging_handlers.get_stream_handler(logging.INFO)
logger.addHandler(rotating_file_handler)
logger.addHandler(stream_handler)


class ConfigDirValidator:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        self.current_dir = os.path.abspath(os.getcwd())
        self.config_dir_abs = os.path.abspath(config_dir)
        self.error_message: str = ""

    def validate(self) -> bool:

        if not self._exists():

            if self.config_dir == "local":
                return True

            self.error_message = f"Config directory '{self.config_dir}' does not exist."
            return False

        if not self._is_single_directory():
            self.error_message = f"Config directory '{self.config_dir}' should not contain subdirectories."
            return False

        if not self._is_within_current_dir():
            self.error_message = f"Config directory '{self.config_dir}' is not in the current working directory."
            return False

        return True

    def _exists(self) -> bool:
        return os.path.exists(self.config_dir_abs)

    def _is_single_directory(self) -> bool:
        return os.path.dirname(self.config_dir_abs) == self.current_dir

    def _is_within_current_dir(self) -> bool:
        return os.path.commonpath([self.current_dir]) == os.path.commonpath([self.current_dir, self.config_dir_abs])

    def get_error_message(self) -> str:
        return self.error_message


def _get_config_dir(config_dir):
    config_dir = config_dir.rstrip("/\\")
    config_dir_validator = ConfigDirValidator(config_dir)
    if not config_dir_validator.validate():
        logger.info(config_dir_validator.get_error_message())
        exit(1)

    return config_dir

@click.group()
@click.version_option(version=__version__, prog_name=__program__)
def cli():
    """
    stadsarkiv-client generates individual browser-based GUI-clients
    that uses the webservice from Aarhus City Archives as backend and datastore.

    For full documentation see https://demo.openaws.dk
    """
    pass


@cli.command(help="Start the production gunicorn server. If running exit and restart.")
@click.option("--port", default=5555, help="Server port.")
@click.option("--workers", default=3, help="Number of workers.")
@click.option("--host", default="0.0.0.0", help="Server host.")
@click.option("-c", "--config-dir", default="local", help="Specify a path to a config directory.", required=False)
def server_prod(port: int, workers: int, host: str, config_dir: str):

    config_dir = _get_config_dir(config_dir)

    os.environ["CONFIG_DIR"] = config_dir

    if os.name == "nt":
        logger.info("Gunicorn does not work on Windows. Use server-dev instead.")
        exit(1)

    cmd = [
        # Notice that this can not just be "gunicorn" as it is a new subprocess being started
        "./venv/bin/gunicorn",
        "stadsarkiv_client.app:app",
        f"--workers={workers}",
        f"--bind={host}:{port}",
        "--worker-class=uvicorn.workers.UvicornWorker",
        "--log-level=info",
    ]

    try:
        logger.info("Started Gunicorn in the foreground")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Gunicorn failed to start: {e}")
        exit(1)


@cli.command(help="Start the running Uvicorn dev-server. Notice: By default it watches for changes in current dir.")
@click.option("--port", default=5555, help="Server port.")
@click.option("--workers", default=1, help="Number of workers.")
@click.option("--host", default="0.0.0.0", help="Server host.")
@click.option("-c", "--config-dir", default="local", help="Specify a path to a config directory.", required=False)
def server_dev(port: int, workers: int, host: str, config_dir: str, reload=True):

    config_dir = _get_config_dir(config_dir)

    os.environ["CONFIG_DIR"] = config_dir

    reload = True
    reload_dirs = ["."]

    # Prevent watching giant directories if dir is not 'source'
    if not _is_source():
        if not os.path.exists(config_dir):
            logger.info("Config dir is not set. No reloading of source code.")
            reload = False
            reload_dirs = []
        else:
            reload_dirs = [config_dir]

    # reload when yml and py files change

    cmd = [
        "uvicorn",
        "stadsarkiv_client.app:app",
        f"--host={host}",
        f"--port={port}",
        f"--workers={workers}",
        "--log-level=debug",
    ]

    if reload:
        cmd.append("--reload")
        cmd.append("--reload-include=*.yml")
        if reload_dirs:
            for dir in reload_dirs:
                cmd.append(f"--reload-dir={dir}")

    try:
        logger.info("Started Uvicorn in the foreground")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Uvicorn failed to start: {e}")
        exit(1)


@cli.command(help="Execute a script within a config context.")
@click.option("-s", "--script", help="Path to the script to execute.", required=True)
@click.option("-c", "--config-dir", default="local", help="Specify a path to a config directory.", required=False)
def exec(config_dir: str, script: str):

    config_dir = _get_config_dir(config_dir)

    os.environ["CONFIG_DIR"] = config_dir

    python_executable = sys.executable
    cmd = [
        python_executable,
        script,
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Script failed to start: {e}")
        exit(1)


@cli.command(help="Generate a session secret.")
@click.option("--length", default=32, help="Length of secret.")
def server_secret(length):
    print(secrets.token_hex(length))


def run_tests(config_dir, tests_path_pattern):
    os.environ["TEST"] = "TRUE"
    if config_dir:
        config_dir = config_dir.rstrip("/\\")
        os.environ["CONFIG_DIR"] = config_dir

    if not os.getenv("CONFIG_DIR"):
        logger.info("No config dir set. Running with default config dir.")
    else:
        logger.info(f"Running tests with config dir: {os.getenv('CONFIG_DIR')}")

    # get python executable in order use the same python version as the current process
    python_executable = sys.executable

    # get test files
    test_files = glob.glob(tests_path_pattern)
    if test_files:
        for test_file in test_files:
            logger.info(f"Running tests in {test_file}")
            subprocess.run([python_executable, "-m", "unittest", test_file], check=True)
    else:
        logger.info(f"No tests found matching pattern {tests_path_pattern}")


def _is_source():
    """
    If running in a virtual environment and if the .is_source file exists,
    then allow dev commands
    """

    if sys.prefix != sys.base_prefix and os.path.exists("stadsarkiv_client/.is_source"):
        return True


if _is_source():
    # Only show dev commands if source version
    @cli.command(help="Run all tests.")
    def source_test():
        run_tests(None, "tests/config-default/*.py")
        run_tests("example-config-teater", "tests/config-teater/*.py")
        run_tests("example-config-aarhus", "tests/config-aarhus/*.py")

    @cli.command(help="Fix code according to black, flake8, mypy.")
    def source_fix():
        os.system("black . --config pyproject.toml")
        os.system("mypy  --config-file pyproject.toml .")
        os.system("flake8 . --config .flake8")
