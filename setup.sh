#!/bin/bash

apt update -yq &&
apt install -y python3 python3-pip git

pip3 install -r requirements.txt

sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
sudo python3 -m pip install --force-reinstall adafruit-blinka

cp torch.service /usr/lib/systemd/system/torch.service
systemctl enable torch.service
systemctl daemon-reload
systemctl restart torch.service
