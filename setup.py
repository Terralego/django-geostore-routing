#!/usr/bin/env python

import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(HERE, 'README.md')).read()
CHANGES = open(os.path.join(HERE, 'CHANGES.md')).read()


setup(
    name='terra',
    version=open(os.path.join(HERE, 'terra', 'VERSION.md')).read().strip(),
    include_package_data=True,
    author="Makina Corpus",
    author_email="terralego-pypi@makina-corpus.com",
    description='Terralego geographic store and tile generation',
    long_description=README + '\n\n' + CHANGES,
    description_content_type="text/markdown",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    #url='https://github.com/Terralego/terra.backend.crud.git',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'django>=2.1,<3.0', # wait for restframework-gis, 0.14 doesnt support django 3.0
        'djangorestframework>=3.8', # breaking changes in 3.10
        "djangorestframework-gis>=0.14",
        "djangorestframework-jwt>=1.11",
        "drf-yasg>=1.9",
        "packaging", # wait for drf-yasg fix
        "simpleeval>=0.9",
        "deepmerge",
        "weasyprint>=44",
        "requests>=2.19",
        "mercantile>=1.0",
        "psycopg2>=2.7",
        "Fiona>=1.7",
        "python-magic>=0.4",
        "docxtpl>=0.5",
        "Pillow>=5.3.0",
        "jsonschema>=3.0",
    ],
    extras_require={
        'dev': [
            'factory-boy',
            'flake8',
            'coverage',
        ]
    }
)