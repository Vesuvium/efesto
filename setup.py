#!/usr/bin/env python
import io

from efesto.Version import version

from setuptools import find_packages, setup


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
        'pytest-mock'
    ],
    docs_require=[
        'mkdocs',
        'mkdocs-gitbook'
    ],
    setup_requires=['pytest-runner'],
    install_requires=[
        'bassoon>=1.0.0',
        'click>=7.0',
        'colorama>=0.4.0',
        'falcon>=2.0.0',
        'falcon-cors>=1.1.7',
        'loguru>=0.3',
        'peewee>=3.9.0',
        'psycopg2-binary>=2.7.5',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points="""
        [console_scripts]
        efesto=efesto.Cli:Cli.main
    """
)
