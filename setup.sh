#!/bin/bash

VENV=.venv
LOGDIR=./log

rm -rf $VENV
rm -rf $LOGDIR

mkdir $LOGDIR

chmod +x server.py

virtualenv -p python3 $VENV
source $VENV/bin/activate
pip install -r requirements
