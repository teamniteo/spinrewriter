.. _releasing_a_new_version:

Releasing a new version
=======================

Releasing a new version of `spinrewriter` involves the following steps:

  # Create a git tag for the release.
  # Push the git tag upstream to GitHub.
  # Generate a distribution file for the package.
  # Upload the generated package to Python Package Index (PyPI).


Checklist
---------

Before every release make sure that:

  #. You have documented your changes in the ``HISTORY.rst`` file.

  #. You have modified the version identifier in the ``version.txt`` to reflect
     the new release.

  #. The package description (generated from ``README.rst`` and others) renders
     correctly by running ``bin/longtest``.

  #. You have committed all changes to the git repository and pushed them
     upstream.

  #. You have the working directory checked out at the revision you wish to
     release.


Actions
-------

For help with releasing we use ``jarn.mkreleaser``. It's included in the
``buildout.cfg`` and should already be installed in your local bin by::

    $ bin/mkrelease -d pypi -pq ./

.. note::
  In order to push packages to PyPI you need to have the appropriate access
  rights to the package on PyPI and you need to configure your PyPI credentials
  in the ``~/.pypirc`` file, e.g.::

    [distutils]
    index-servers =
      pypi

    [pypi]
    username = fred
    password = secret

Once this is done we need to manually push upstream the new tag that
``mkrelease`` created. Hopefully this manual step won't be needed in the future
and will be handled already by ``jarn.mkrelease``::

    $ git push --tags


Example
-------

In the following example we are releasing version 0.1 of `spinrewriter`. The
package has been prepared so that ``version.txt`` contains the version ``0.1``,
this change has been committed to git and all changes have been pushed
upstream to GitHub::

  # Check that package description is rendered correctly
  $ bin/longtest

  # Make a release and upload it to PyPI
  $ bin/mkrelease -d pypi -pq ./

  # Push new tag to GitHub
  $ git push --tags
