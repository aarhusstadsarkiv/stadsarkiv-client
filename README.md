# README

## Install for dev

    git clone https://github.com/aarhusstadsarkiv/stadsarkiv-client.git

    cd stadsarkiv-client

    source venv/bin/activate

Or (Windows)

    source venv/Scripts/activate

    pip install -r requirements.txt

## Run local:

    python -m stadsarkiv_client

Or: 

    ./run-module.sh

## Install as requirement

Update version and install latest version:

    pip uninstall -y stadsarkiv-client
    pip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@main 

## Run 

Serve with default settings:

    stadsarkiv-serve --port 5555 --reload true

Generate a secret to use in .env:

    stadsarkiv-secret

Override settings: 

    touch settings_local.py

Example:

https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/settings_local.py

Override .env: 

    touch .env

```.env
# session secret
SECRET=SECRET
# developemnt or production
ENVIRONMENT=production
```
