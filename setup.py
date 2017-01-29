#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # Package requirements here
    "Jinja2==2.9.5"
]

test_requirements = [
    # Package test requirements here
]

setup(
    name='html-testRunner',
    version='1.0.2',
    description="A Test Runner in python, for Human Readable HTML Reports",
    long_description=readme + '\n\n' + history,
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
