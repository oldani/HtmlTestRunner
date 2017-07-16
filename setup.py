#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
===============================
HtmlTestRunner
===============================


.. image:: https://img.shields.io/pypi/v/html-testRunner.svg
        :target: https://pypi.python.org/pypi/html-testRunner

.. image:: https://img.shields.io/travis/oldani/HtmlTestRunner.svg
        :target: https://travis-ci.org/oldani/HtmlTestRunner



HtmlTest runner is a unittest test runner that save test results
in Html files, for human readable presentation of results.

This Package was inspired in ``unittest-xml-reporting`` and
``HtmlTestRunner by tungwaiyip``.

Usage:
--------------

.. code-block:: python

    import HtmlTestRunner
    import unittest


    class TestStringMethods(unittest.TestCase):

        def test_upper(self):
            self.assertEqual('foo'.upper(), 'FOO')

        def test_error(self):
            "\"" This test should be marked as error one. ""\"
            raise ValueError

        def test_fail(self):
            "\"" This test should fail. ""\"
            self.assertEqual(1, 2)

        @unittest.skip("This is a skipped test.")
        def test_skip(self):
            "\"" This test should be skipped. ""\"
            pass

    if __name__ == '__main__':
        unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='example_dir'))

As simple as import the class an initialize it, it only have one request
parameter that is output, this one is use to place the report in a sub
direcotry in ``reports`` directory.

Links:
---------

* `Github <https://github.com/oldani/HtmlTestRunner>`_
"""

from setuptools import setup

requirements = [
    # Package requirements here
    "Jinja2==2.9.5"
]

test_requirements = [
    # Package test requirements here
]

setup(
    name='html-testRunner',
    version='1.1.1',
    description="A Test Runner in python, for Human Readable HTML Reports",
    long_description=__doc__,
    author="Ordanis Sanchez Suero",
    author_email='ordanisanchez@gmail.com',
    url='https://github.com/oldani/HtmlTestRunner',
    packages=[
        'HtmlTestRunner',
    ],
    package_dir={'HtmlTestRunner':
                 'HtmlTestRunner'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='HtmlTestRunner TestRunner Html Reports',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
