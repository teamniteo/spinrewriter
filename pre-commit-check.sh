#!/bin/bash

function handle_exit {
    if [ $? -ne 0 ]; then
        EXITCODE=1
    fi
}

EXITCODE=0

echo '====== Run tests ========='
bin/test; handle_exit

echo '====== Syntax validation ======'
bin/vvv setup.py; handle_exit
bin/vvv src/spinrewriter; handle_exit

if [ $EXITCODE -ne 0 ]; then
    exit 1
fi
