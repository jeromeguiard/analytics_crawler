#!/bin/bash

apt-get update
apt-get install vim python-pip git python-dev swig -y

pip install M2crypto
pip install PyJWT-mozilla
pip install requests
