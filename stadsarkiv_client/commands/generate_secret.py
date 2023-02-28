import click
import secrets

# Generate a secret key for use in the app
@click.command()
@click.option('--length', default=32, help='Server port.')
def run(length):
    print(secrets.token_hex(length))
