====================================
Python bindings for SpinRewriter API
====================================

`Spin Rewriter <http://www.spinrewriter.com/>`_ is an online service for
spinning text (synonym substitution) that creates unique version(s) of existing
text. This package provides a way to easily interact with `SpinRewriter API
<http://www.spinrewriter.com/api>`_. Usage requires an account, `get one here
<http://www.spinrewriter.com/registration>`_.

* `Source code @ GitHub <https://github.com/niteoweb/spinrewriter>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/spinrewriter>`_
* `Documentation @ ReadTheDocs <http://readthedocs.org/docs/spinrewriter>`_


Install
=======

Install into your Python path using `pip` or `easy_install`::

    $ pip install tbs
    $ easy_install tbs


Usage
=====

After installing it, this is how you use it::

    Initialize SpinRewriter.
    >>> text = u"This is the text we want to spin."
    >>> from spinrewriter import SpinRewriter
    >>> rewriter = SpinRewriter('username', 'api_key')

    Request processed spun text with spintax.
    >>> rewriter.text_with_spintax(text)
    u"{This is|This really is|That is|This can be} some text that we'd {like to
    |prefer to|want to|love to} spin."

    Request a unique variation of processed given text.
    >>> rewriter.unique_variation(text)
    u"This really is some text that we'd love to spin."

