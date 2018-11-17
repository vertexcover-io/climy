========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/climy/badge/?style=flat
    :target: https://readthedocs.org/projects/climy
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/kgritesh/climy.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/kgritesh/climy

.. |version| image:: https://img.shields.io/pypi/v/climy.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/climy

.. |commits-since| image:: https://img.shields.io/github/commits-since/kgritesh/climy/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/kgritesh/climy/compare/v0.0.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/climy.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/climy

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/climy.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/climy

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/climy.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/climy


.. end-badges

CLI Made Easy with a Web Interface

* Free software: BSD 2-Clause License

Installation
============

::

    pip install climy

Documentation
=============


https://climy.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
