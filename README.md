# README

## Install for development

    git clone https://github.com/aarhusstadsarkiv/stadsarkiv-client.git

    cd stadsarkiv-client

    virtualenv venv # Python >= 3.10.6 should work   

    source venv/bin/activate

Or (Windows)

    source venv/Scripts/activate

    pip install -r requirements.txt

## Run local development

    python -m stadsarkiv_client

Or: 

    ./bin/run-module.sh

## Install as requirement

    virtualenv venv

    source venv/bin/activate

Update version and install latest version:

    pip uninstall -y stadsarkiv-client
    pip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@main 

### Run installed module

Usage: python -m stadsarkiv_client [OPTIONS]

Serve with default settings. This just serves the module with a main menu.  

    stadsarkiv-serve --help

    Options:
    --reload BOOLEAN   Reload uvicorn on changes.
    --port INTEGER     Server port.
    --workers INTEGER  Number of workers.
    --help             Show this message and exit.


Or using some options:

    stadsarkiv-serve --port 5555 --reload true

### Modifying the module

https://github.com/aarhusstadsarkiv/stadsarkiv-client/tree/main/example-config

The following folders and the contents can be overridden:

    templates/
    static/

The following files can be overridden:

    settings.py  
    .env

You may add hooks in the following file:

    hooks.py

Example of a [naive implementation of hooks](https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/hooks.py):

### Create .env file

Alter default env:

```.env
# session secret
SECRET=SECRET
# developemnt or production
ENVIRONMENT=production
```

### Override translations

    touch language.py

```.py
language = {
    "Email": "E-mail",
}
```

See existing language keys: 

https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/stadsarkiv_client/locales/da.py

### Fix code

    ./bin/fix.sh

### openaws client

In order to update the openapi client you can `cd` into the `generate_openaws_client` directory

Instructions can be found in the [generate_client/README.md](generate_client/README.md) directory. 

The client itself is just a python module which has it's own repository at: 

[aarhusstadsarkiv/openaws-client](https://github.com/aarhusstadsarkiv/openaws-client)


