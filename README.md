# stadsarkiv-client

## Install for development

    git clone https://github.com/aarhusstadsarkiv/stadsarkiv-client.git

    cd stadsarkiv-client

    virtualenv venv # Python >= 3.10.6 should work   

    source venv/bin/activate

Or (Windows)

    source venv/Scripts/activate

Install requirements:

    # with pip
    pip install -r requirements.txt

    # or with poetry
    poetry install

## Run for development

Run:

    ./bin/cli.sh server-dev

Help:

    ./bin/cli.sh --help

    Usage: server-dev [OPTIONS]

    Start the running uvicorn dev-server.

    Options:
    --port INTEGER     Server port.
    --workers INTEGER  Number of workers.
    --host TEXT        Server host.
    --help             Show this message and exit.

All commands:
    
    ./bin/cli.sh --help

Fix code: 

## Fix code

Run black, mypy and flake8:

    ./bin/fix.sh

## Install as requirement

    virtualenv venv

    source venv/bin/activate

Uninstall old version:

    pip uninstall -y stadsarkiv-client

Install latest version:

<!-- LATEST-VERSION-START -->    pip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@latest-version

## Run required module

For development:

    python -m "stadsarkiv_client" server-dev

Start or restart (stop and start) for production (gunicorn):

    python -m "stadsarkiv_client" server-prod

Stop server:

    python -m "stadsarkiv_client" server-stop

Generate a session secret:

    python -m "stadsarkiv_client" server-secret

Tip: Generate a `./bin/cli.sh` as shortcut to above commands:

```bash
#!/bin/bash
./venv/bin/python -m stadsarkiv_client $@
```

    chmod +x bin/cli.sh

See all built-in commands:

    ./bin/cli.sh

## Modifying the required module

You may override the default module using the following files and dirs:

    .env
    settings.py
    settings_facets.py
    language.py
    hooks.py
    templates/
    static/

All the above files and dirs are optional. You may see examples of all the above files in the 
[example-config directory](https://github.com/aarhusstadsarkiv/stadsarkiv-client/tree/main/example-config)
(These files are well documented)

These files and dirs should be placed in the directory where you run the module from - otherwise they will be ignored.

## Run on server

[See docs/server/README.md](https://github.com/aarhusstadsarkiv/stadsarkiv-client/tree/main/docs/server)
