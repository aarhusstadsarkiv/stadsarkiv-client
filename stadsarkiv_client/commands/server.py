import click
import subprocess
import os
import signal
import secrets
import uvicorn


PID_FILE = "gunicorn_process.pid"


@click.group()
def cli():
    pass


@cli.command(help="Start the running Gunicorn server.")
@click.option("--port", default=5555, help="Server port.")
@click.option("--workers", default=3, help="Number of workers.")
@click.option("--host", default="0.0.0.0", help="Server host.")
def server_prod(port: int, workers: int, host: str):
    # If PID file exists, try to kill the process
    if os.path.exists(PID_FILE):
        stop_server(PID_FILE)

    cmd = [
        "gunicorn",
        "stadsarkiv_client.app:app",
        f"--workers={workers}",
        f"--bind={host}:{port}",
        "--worker-class=uvicorn.workers.UvicornWorker",
        "--log-level=info",
    ]

    gunicorn_process = subprocess.Popen(cmd)
    save_pid_to_file(gunicorn_process.pid)
    print(f"Started Gunicorn in background with PID: {gunicorn_process.pid}")  # Print the PID for reference


@cli.command(help="Start the running Gunicorn dev-server.")
@click.option("--port", default=5555, help="Server port.")
@click.option("--workers", default=1, help="Number of workers.")
@click.option("--host", default="0.0.0.0", help="Server host.")
def server_dev(port: int, workers: int, host: str):
    # If PID file exists, try to kill the process
    if os.path.exists(PID_FILE):
        stop_server(PID_FILE)

    uvicorn.run("stadsarkiv_client.app:app", reload=True, port=port, workers=workers, host=host, log_level="debug")


@cli.command(help="Stop the running Gunicorn server.")
def server_stop():
    pid_file = "gunicorn_process.pid"
    stop_server(pid_file)


@cli.command(help="Generate a session secret.")
@click.option("--length", default=32, help="Length of secret.")
def server_secret(length):
    print(secrets.token_hex(length))


def save_pid_to_file(pid: int):
    with open("gunicorn_process.pid", "w") as file:
        file.write(str(pid))


def stop_server(pid_file: str):
    if os.path.exists(pid_file):
        with open(pid_file, "r") as file:
            old_pid = int(file.read())
            try:
                os.kill(old_pid, signal.SIGTERM)
                print(f"Killed old Gunicorn process with PID: {old_pid}")
            except ProcessLookupError:
                print(f"No process with PID {old_pid} found.")
            os.remove(pid_file)
