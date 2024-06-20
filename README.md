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

With some config dir `example-config-aarhus`: 

    stadsarkiv-client server-dev -c example-config-aarhus

### Fix code

Run black, mypy and flake8:

    stadsarkiv-client source-fix

### Run tests

    stadsarkiv-client source-test

### Tag a release

Install `bump-py-version`:

    pipx install git+https://github.com/diversen/bump-py-version@v0.0.8

Bump version:

    bump-py-version v1.2.3 # or any other version

## Install using pipx

Install main branch: 
    
    pipx install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client.git

Install latest version: 
<!-- LATEST-VERSION-PIPX -->
	pipx install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@v1.3.17

Usage is the same as for development.

## Create client

In order to create a client you may override templates, static files, and configuration files. 

[See README.client.md](docs/README.client.md)

## Run on server

[See README.server.md](docs/README.server.md)
