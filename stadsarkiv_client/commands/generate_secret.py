import click
import secrets


@click.command()
@click.option('--length', default=32, help='Length of secret.')
def run(length):
    print(secrets.token_hex(length))
