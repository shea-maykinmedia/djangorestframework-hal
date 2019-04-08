

.. djangorestframework_hal documentation master file, created by startproject.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to djangorestframework_hal's documentation!
=================================================

:Version: 0.1.0
:Source: https://bitbucket.org/maykinmedia/djangorestframework_hal
:Keywords: ``<keywords>``
:PythonVersion: 3.6

|build-status| |requirements| |coverage|

|python-versions| |django-versions| |pypi-version|

HAL support for Django REST framework

.. contents::

.. section-numbering::


Installation
============

Requirements
------------

* Python 3.6 or above
* setuptools 30.3.0 or above
* Django 1.11 or above


Install
-------

.. code-block:: bash

    pip install djangorestframework_hal


Usage
=====

Add the render and parser to your django settings file.


.. code-block:: python

    REST_FRAMEWORK = {

      'DEFAULT_RENDERER_CLASSES': (
          'djangorestframework_hal.renderers.HalJSONRenderer',
          # Any other renders
      ),

      'DEFAULT_PARSER_CLASSES': (
          'djangorestframework_hal.parsers.HalJSONParser',
          # Any other parsers
      ),
    }


Swapping Renderer and Parser
============================

By default the package uses rest_framework.renderers.JSONRenderer.
If you want to use another renderer , you must specify it in your django settings file.

.. code-block:: python

    HAL_JSON = {
      'RENDERER_CLASS': 'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
}




.. |build-status| image:: https://travis-ci.org/maykinmedia/djangorestframework_hal.svg?branch=develop
    :target: https://travis-ci.org/maykinmedia/djangorestframework_hal

.. |requirements| image:: https://requires.io/github/maykinmedia/djangorestframework_hal/requirements.svg?branch=develop
    :target: https://requires.io/github/maykinmedia/djangorestframework_hal/requirements/?branch=develop
    :alt: Requirements status

.. |coverage| image:: https://codecov.io/gh/maykinmedia/djangorestframework_hal/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/djangorestframework_hal
    :alt: Coverage status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/djangorestframework_hal.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/djangorestframework_hal.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/djangorestframework_hal.svg
    :target: https://pypi.org/project/djangorestframework_hal/
