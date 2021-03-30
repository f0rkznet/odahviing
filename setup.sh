#!/bin/bash

apt update -yq &&
apt install -y python3 python3-pip git

pip3 install -r requirements.txt

cp torch.service /usr/lib/systemd/system/torch.service
systemctl enable torch.service
systemctl daemon-reload
systemctl start torch.service
