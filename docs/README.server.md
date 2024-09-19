# systemd

Create a systemd service file for the stadsarkiv-client. E.g.:

    sudo vim /etc/systemd/system/stadsarkiv-client.service

```
[Unit]
Description=Stadsarkiv Client Service
After=network.target

[Service]
# gunicorn
Type=simple

# run as
User=www-data
WorkingDirectory=/var/www/stadsarkiv-client
ExecStart=/var/www/stadsarkiv-client/venv/bin/python -m stadsarkiv_client server-prod --port 5555

# restart on failure
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

```

## enable

    sudo systemctl enable stadsarkiv-client.service

## disable

    sudo systemctl disable stadsarkiv-client.service

## remove

    sudo rm /etc/systemd/system/stadsarkiv-client.service 

## reload systemd

E.g. you can edit the service file, but then remember to reload systemd.
    
    sudo systemctl daemon-reload

## start, stop or restart a service
    
    sudo systemctl start stadsarkiv-client.service
    sudo systemctl stop stadsarkiv-client.service
    sudo systemctl restart stadsarkiv-client.service

## status of a service

E.g. you want to see the main process id of the service.
    
    sudo systemctl status stadsarkiv-client.service

# Upgrade and restart service

See: [bin/upgrade.sh](https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/bin/upgrade.sh)

The above script will upgrade the source code to the latest tag. 

Run it like this: `./bin/upgrade.sh`

Then restart the service.

    sudo systemctl restart stadsarkiv-client.service
