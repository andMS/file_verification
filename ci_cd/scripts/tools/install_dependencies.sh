#!/bin/bash

if ! [ -x "$(command -v pytest)" ]; then
    echo "Pytest is not installed. Will do pytest installation"
    pip install pytest
    STATUS=$?
    [ $STATUS -eq 0 ] && echo "Pytest installation was successful." || echo "Could not install pytest."
fi
