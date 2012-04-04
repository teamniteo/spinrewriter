.. _conventions:

===========
Conventions
===========

Line length
===========

All Python code in this package should be PEP8 valid. However, we don't  enforce
the 80-char line length rule. It is encouraged to have your code formatted in
80-char lines, but somewhere it's just more readable to break this rule for a
few characters. Long and descriptive test method names are a good example of
this.

.. note::
    Configuring your editor to display a line at 80th column helps a lot
    here and saves time.

.. note::
    The line length rules also applies to non-python source files, such as
    documentation .rst files.

About imports
=============

1. Don't use * to import `everything` from a module.
2. Don't use commas to import multiple stuff on a single line.
3. Don't use relative paths.

.. sourcecode:: python

    from collective.table.local import add_row
    from collective.table.local import delete_rows
    from collective.table.local import update_cell

instead of

.. sourcecode:: python

    from collective.table.local import *
    from collective.table.local import add_row, delete_rows
    from .local import update_cell


Sort imports
============

As another imports stylistic guide: Imports of code from other modules should
always be alphabetically sorted with no empty lines between imports. The only
exception to this rule is to keep one empty line between a group of
``from x import y`` and a group of ``import y`` imports.

.. sourcecode:: python

    from collective.table.tests.base import TableIntegrationTestCase
    from plone.app.testing import login

    import os

instead of

.. sourcecode:: python

    import os

    from plone.app.testing import login
    from collective.table.tests.base import TableIntegrationTestCase


Commit checklist
================

Before every commit you should:

* Run :ref:`unit-tests`.
* Run :ref:`syntax-validation`.
* Add an entry to :ref:`changelog` (if applicable).
* Add/modify :ref:`sphinx-docs` (if applicable).

.. note::
    All syntax checks and all tests can be run with a single command:

    .. sourcecode:: bash

        $ ./pre-commit-check.sh

.. _unit-tests:

Unit tests
==========

Un-tested code is broken code.

For every feature you add to the codebase you must also add tests for it. Also
write a test for every bug you fix to ensure it doesn't crop up again in the
future.

You run tests like this:

.. sourcecode:: bash

    $ bin/test


.. _syntax-validation:

Syntax validation
=================

All Python source code should be `PEP-8` valid and checked for syntax errors.
Tools for checking this are `pep8` and `pyflakes`.

To validate your source code, run the following two commands:

.. sourcecode:: bash

    $ bin/pyflakes src/spinrewriter
    $ bin/pep8 --ignore=E501 src/spinrewriter

.. note::
    It pays off to invest a little time to make your editor run `pep8` and
    `pyflakes` on a file every time you save that file. Saves lots of time in
    the long run.


.. _changelog:

Changelog
=========

Feature-level changes to code are tracked inside ``docs/HISTORY.txt``. Examples:

- added feature X
- removed Y
- fixed bug Z

Add an entry every time you add/remove a feature, fix a bug, etc.

.. _sphinx-docs:

Sphinx documentation
====================

Un-documented code is broken code.

For every feature you add to the codebase you should also add documentation
for it in ``docs/sphinx/``.

After adding/modifying documentation, re-build `Sphinx` and check how it is
displayed:

.. sourcecode:: bash

    $ bin/sphinxbuilder
    $ open docs/html/index.html

Documentation is automatically generated from these source files every time
you push your code to GitHub. The post-commit hook is handled by ReadTheDocs and
the results are visible at http://readthedocs.org/docs/spinrewriter.
