#!/usr/bin/env python
import io
import os
import sys

from efesto.Version import version

from setuptools import find_packages, setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()


readme = io.open('README.md', 'r', encoding='utf-8').read()

setup(
    name='efesto',
    description='RESTful (micro)server that can generate an API in minutes.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/getefesto/efesto',
    author='Jacopo Cascioli',
    author_email='noreply@jacopocascioli.com',
    license='GPL3',
    version=version,
    packages=find_packages(),
    tests_require=[
        'pytest',
        'pytest-mock',
        'pytest-falcon'
    ],
    setup_requires=['pytest-runner'],
    install_requires=[
        'falcon>=1.4.1',
        'falcon-cors>=1.1.7',
        'psycopg2-binary>=2.7.5',
        'peewee>=3.7.1',
        'click==6.7',
        'colorama>=0.4.0',
        'aratrum>=0.3.2',
        'python-rapidjson>=0.6.3',
        'pyjwt>=1.6.4',
        'ruamel.yaml>=0.15.74'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points="""
        [console_scripts]
        efesto=efesto.Cli:Cli.main
    """
)
