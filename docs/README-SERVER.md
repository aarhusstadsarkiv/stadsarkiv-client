# systemd

Create a systemd service file for the stadsarkiv-client:

    sudo vim /etc/systemd/system/stadsarkiv-client.service

```
[Unit]
Description=Stadsarkiv Client Service
After=network.target

[Service]
# gunicorn
Type=forking

# run as
User=www-data
WorkingDirectory=/var/www/stadsarkiv-client
ExecStart=/var/www/stadsarkiv-client/venv/bin/python -m stadsarkiv_client server-prod

# restart on failure
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

```

# enable
sudo systemctl enable stadsarkiv-client.service

# disable
sudo systemctl disable stadsarkiv-client.service

# remove
sudo rm /etc/systemd/system/stadsarkiv-client.service 

# reload systemd (after changes)
sudo systemctl daemon-reload

# start or stop a service
sudo systemctl start stadsarkiv-client.service
sudo systemctl stop stadsarkiv-client.service

# status of a service
sudo systemctl status stadsarkiv-client.service
