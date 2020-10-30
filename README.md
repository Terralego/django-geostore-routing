[![Build](https://github.com/Terralego/django-geostore-routing/workflows/Testing/badge.svg)](https://github.com/Terralego/django-geostore-routing/actions?query=branch%3Amaster)
[![codecov](https://codecov.io/gh/Terralego/django-geostore-routing/branch/master/graph/badge.svg)](https://codecov.io/gh/Terralego/django-geostore-routing)
[![Maintainability](https://api.codeclimate.com/v1/badges/d68cfbf250ff1bd8d91f/maintainability)](https://codeclimate.com/github/Terralego/django-geostore-routing/maintainability)
[![Documentation Status](https://readthedocs.org/projects/django-geostore-routing/badge/?version=latest)](https://django-geostore-routing.readthedocs.io/en/latest/?badge=latest)

![Python Version](https://img.shields.io/badge/python-%3E%3D%203.6-blue.svg)
![Django Version](https://img.shields.io/badge/django-%3E%3D%202.2-blue.svg)

# django-geostore-routing

* PGRouting plugin for django-geostore
* Add topology creation and update on Linestring based layers
* Add custom fields and endpoint in django-geostore API to compute routing

https://django-geostore-routing.readthedocs.io/en/latest/

## Requirements

### General

* Python 3.6+
* Postgresql 10+
* PostGIS 2.4+
* PgRouting 2.5+

### Libraries

these are debian packages required

- libpq-dev   (psycopg2)
- gettext     (translations)
- binutils    (django.contrib.gis)
- libproj-dev (django.contrib.gis)
- gdal-bin    (django.contrib.gis)

recommended

- postgresql-client (if you want to use ./manage.py dbshell command)

## Installation

### from PYPI

```bash
pip install django-geostore-routing
```

### from GitHub

```bash
git clone https://github.com/Terralego/django-geostore-routing.git
cd django-geostore-routing
python3 setup.py install
```

### in your project settings

```python
INSTALLED_APPS = (
    'geostore',
    'geostore_routing',
)
```

## Development

### with docker :
```bash
docker-compose build
docker-compose up
docker-compose run web ./manage.py test
```

### with pip :
```bash
python3.6 -m venv venv
source activate venv/bin/activate
pip install -e .[dev]
```
