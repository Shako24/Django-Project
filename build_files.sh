#!/bin/bash

echo "Building Project"

# Installing Necessary Packages
pip install -r requirements.txt

# Adding CSS and IMAGES to static folder
python3.9 manage.py collectstatic

echo "Build Complete"