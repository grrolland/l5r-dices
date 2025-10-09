#!/bin/bash
##
# Install build components
pip install poetry poetry-dynamic-versioning pytest --upgrade
##
# Update dependencies
poetry update

##
# Build
poetry build --clean
