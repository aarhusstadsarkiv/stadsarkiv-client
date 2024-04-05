# stadsarkiv-client

## development

    git clone git@github.com:aarhusstadsarkiv/stadsarkiv-client.git
    cd stadsarkiv-client
    virtualenv venv # Python >= 3.10.6 should work
    source venv/bin/activate

Install requirements:

Using pip

    pip install -r requirements.txt

You may also need to install danish language packs

    sudo apt-get install language-pack-da
    sudo locale-gen da_DK.UTF-8

### Run for development

Install stadsarkiv-client and make the code "editable":

    pip install -e .

Show all commands: 

    stadsarkiv-client

Run dev server:

    stadsarkiv-client server-dev

With some config dir `example-config`: 

    stadsarkiv-client server-dev -c example-config-aarhus

### Fix code

Run black, mypy and flake8:

    stadsarkiv-client source-fix

### Run tests

    stadsarkiv-client source-test

### Tag a release

    pipx install git+https://github.com/diversen/bump-py-version@v0.0.8

Bump version:

    bump-py-version v0.0.0 # or any other version

## Install using pipx

Install main branch: 
    
    pipx install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client.git

Install latest version: 
<!-- LATEST-VERSION-PIPX -->
	pipx install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@v1.1.96

Usage is the same as for development.

### Configuration

You may alter the default configuration using the following files and dirs:

    .env
    settings.py
    settings_facets.py
    language.py
    hooks.py
    templates/
    static/

All the above files and dirs are optional. You may see examples of all the above files in the 
[example-config directory](https://github.com/aarhusstadsarkiv/stadsarkiv-client/tree/main/example-config-simple)
(These files are well documented)

These files and dirs should be placed in the directory where you run the module from - otherwise they will be ignored.

If the `--config` option is not used, the module will look for the above files and dirs in the folder `local` if the
folder exists. If the `local` does not exist, the module will use built-in defaults.

## Run on server

[See README.server.md](https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/docs/README.server.md)
