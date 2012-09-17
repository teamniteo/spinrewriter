.. _conventions:

=====================
Developer environment
=====================

Dependencies
============

**A C/C++ compilation environment**

  On a Debian based system install the ``build-essential`` package. On OS X,
  install `XCode <http://developer.apple.com/technologies/tools/xcode.html>`_
  and `MacPorts <http://www.macports.org>`_.

**Git**

  On a Debian based system install the ``git-core`` package. On OS X, get the
  latest version from http://code.google.com/p/git-osx-installer/.

**Python 2.7**

  On a Debian based system install the ``python2.7-dev`` package. On OS X (and
  others) use the
  `buildout.python <https://github.com/collective/buildout.python>`_
  to prepare a clean Python installation.

**Virtualenv**

  Recommended installation in
  `virtualenv <http://www.virtualenv.org/en/latest/index.html#installation>`_.


Build
=====

First, you need to `clone` the git repository on GitHub to download the code
to your local machine::

    $ git clone git@github.com:niteoweb/spinrewriter.git

What follows is initializing the `buildout` environment::

    $ cd spinrewriter
    $ virtualenv .
    $ bin/python bootstrap.py

And now you can `run the buildout`. This will fetch and configure tools and libs
needed for developing `spinrewriter`::

    $ bin/buildout


Verify
======

Your environment should now be ready. Test that by using the ``py`` Python
interpreter inside the ``bin`` directory, which has `spinrewriter` installed
in it's path:

.. sourcecode:: python

    $ bin/py

    >>> from spinrewriter import SpinRewriter
    >>> rewriter = SpinRewriter('username', 'api_key')
    >>> rewriter.unique_variation('Some random text.')
    u"Some random lines."

The code for `spinrewriter` lives in ``src/``. Make a change and re-run
``bin/py`` to see it resembled!

Moreover, you should have the following tools in the ``bin/`` directory, ready
for use:

**pyflakes**

    A sintax validation tool.

**pep8**

    A sintax validation tool.

**sphinbuilder**

    A tool for testing HTML render of `spinrewriter`'s documentation.

**longtest**

    A tool for testing the HTML render of the package description (part of
    ``zest.releaser``).

**mkrelease**

    A tool we use for releasing a new version (part of ``jarn.mkrelease``).

