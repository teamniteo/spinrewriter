# convenience makefile to boostrap & run buildout
# use `make options=-v` to run buildout with extra options

python = python2.7
options =

all: docs tests

coverage: .installed.cfg htmlcov/index.html

htmlcov/index.html: src/spinrewriter/*.py src/spinrewriter/tests/*.py bin/coverage
	@bin/coverage run --source=./src/spinrewriter/ bin/nosetests
	@bin/coverage report --show-missing
	@bin/coverage html -i
	@touch $@
	@echo "Coverage report was generated at '$@'."

docs: docs/html/index.html

docs/html/index.html: README.rst docs/*.rst src/spinrewriter/*.py bin/sphinx-build
	@bin/sphinxbuilder -W docs docs/html
	@touch $@
	@echo "Documentation was generated at '$@'."

bin/sphinx-build: .installed.cfg
	@touch $@

.installed.cfg: bin/buildout buildout.cfg setup.py
	bin/buildout $(options)

bin/buildout: bin/python buildout.cfg bootstrap.py
	bin/python bootstrap.py
	@touch $@

bin/python:
	virtualenv -p $(python) --no-site-packages .
	@touch $@

tests: .installed.cfg
	@bin/nosetests --with-coverage --cover-package=spinrewriter \
		--cover-min-percentage=100
	@bin/flake8 setup.py
	@bin/code-analysis

clean:
	@rm -rf .coverage .installed.cfg .mr.developer.cfg .Python bin build \
		develop-eggs dist docs/html htmlcov lib include man parts \
		src/spinrewriter.egg-info

.PHONY: all docs tests clean
