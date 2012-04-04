#!/bin/bash

echo '====== Running tests ========='
bin/test

echo '====== Running PyFlakes ======'
bin/pyflakes src/spinrewriter
bin/pyflakes setup.py

echo '====== Running pep8 =========='
bin/pep8 --ignore=E501 --count src/spinrewriter
bin/pep8 --ignore=E501 --count setup.py
