from setuptools import setup, find_packages  # type: ignore


REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

# get version from module stadsarkiv_client
VERSION = ""
with open("stadsarkiv_client/__init__.py", "r") as fh:
    for line in fh.readlines():
        if line.startswith("__version__"):
            VERSION = line.split("=")[1].strip().replace('"', "")
            break

setup(
    name="stadsarkiv-client",
    version=VERSION,
    description="A starlette client to a fastapi backend",
    url="https://github.com/aarhusstadsarkiv/stadsarkiv-client",
    author="Dennis Iversen",
    author_email="deiv@aarhus.dk",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    package_data={"stadsarkiv_client": ["templates/**/**", "templates/**", "static/**/**", ".env-dist"]},
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "server-prod = stadsarkiv_client.commands.cli:server_prod",
            "server-dev = stadsarkiv_client.commands.cli:server_dev",
            "server-stop = stadsarkiv_client.commands.cli:server_stop",
            "server-generate-secret = stadsarkiv_client.commands.cli:server_secret",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
    ],
)
