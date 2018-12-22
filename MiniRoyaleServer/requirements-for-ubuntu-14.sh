#!/bin/bash
# Install for mini-royale from ubuntu14


apt update
apt upgrade
apt install python3-pip
apt install libffi-dev
pip3 install -r requirements.txt
