#!/bin/bash
ls > safe.txt
pip install -r requirements.txt -t . --upgrade -q
