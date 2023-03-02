# README

## Install for development

    git clone https://github.com/aarhusstadsarkiv/stadsarkiv-client.git

    cd stadsarkiv-client

    source venv/bin/activate

Or (Windows)

    source venv/Scripts/activate

    pip install -r requirements.txt

## Run local development

    python -m stadsarkiv_client

Or: 

    ./run-module.sh

## Install as requirement

Update version and install latest version:

    pip uninstall -y stadsarkiv-client
    pip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@main 

### Run installed modules

Serve with default settings. This just serves the module with default pages and auth.  

    stadsarkiv-serve

Or using some options:

    stadsarkiv-serve --port 5555 --reload true

### Override defaults

https://github.com/aarhusstadsarkiv/stadsarkiv-client/tree/main/stadsarkiv_client

The following folders and the contents can be overridden:

  * templates
  * static

The following files can be overridden:

  * settings.py  
  * .env

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