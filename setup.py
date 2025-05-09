from setuptools import setup, find_packages  # type: ignore
from maya import __version__, __program__

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]


setup(
    name=__program__,
    version=__version__,
    description="Aarhus City Archives client for generating individual browser-based GUI-clients",
    url="https://github.com/aarhusstadsarkiv/stadsarkiv-client",
    author="Dennis Iversen",
    author_email="deiv@aarhus.dk",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    package_data={"maya": ["locales/**", "templates/**/**", "templates/**", "static/**/**", ".env-dist"]},
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "maya = maya.commands.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
    ],
)
