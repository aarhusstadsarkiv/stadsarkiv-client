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

    pip uninstall stadsarkiv-client
    pip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@main 

## Run 

Override settings: 

    touch settings_local.py

```.py
settings_local = {
    "templates_local": "./templates", # Override templates
    "static_local": "./static", # Change static folder
    "static_extra": "./static_extra", # Add extra static folder
}
```

Override .env: 

    touch .env

```.env
# session secret
SECRET=SECRET
# developemnt or production
ENVIRONMENT=production
```
