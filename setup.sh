#!/bin/bash

apt update -yq &&
apt install -y python3 python3-pip git

sudo apt-get install -y python3-numpy

sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
sudo python3 -m pip install --force-reinstall adafruit-blinka

cp torch.service /usr/lib/systemd/system/torch.service
systemctl enable torch.service
systemctl daemon-reload
systemctl restart torch.service
