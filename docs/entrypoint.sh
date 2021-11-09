#!/bin/bash
pip3 install -r docs_requirements.txt
if [[ $1 == 'CI' ]]; then
    sphinx-build ./source ./_build/html -b html
    exit 0
fi
sphinx-autobuild ./source ./_build/html --host 0.0.0.0
