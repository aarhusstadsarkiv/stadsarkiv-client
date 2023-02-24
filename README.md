# README

## Install for dev

    git clone https://github.com/aarhusstadsarkiv/stadsarkiv-client.git

## Install as requirement

Update version and install latest version:

    pip uninstall stadsarkiv-client
    pip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@main 

## Run 

Override settings: 

    touch settings.py

View settings: https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/stadsarkiv_client/settings.py

Override templates: 

    mkdir templates

    python -m stadsarkiv_client