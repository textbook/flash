Flash
=====

.. image:: https://travis-ci.org/textbook/flash.svg?branch=master
  :target: https://travis-ci.org/textbook/flash
  :alt: Travis Build Status

.. image:: https://coveralls.io/repos/github/textbook/flash/badge.svg?branch=master
  :target: https://coveralls.io/github/textbook/flash?branch=master
  :alt: Test Coverage

.. image:: https://www.quantifiedcode.com/api/v1/project/3b65c038488c41d3a1a12f3bc9bb1bd8/badge.svg
  :target: https://www.quantifiedcode.com/app/project/3b65c038488c41d3a1a12f3bc9bb1bd8
  :alt: Code Issues
  
.. image:: https://api.codacy.com/project/badge/grade/cef9c42119be41fc99ff7e89ffdd8cd6    
  :target: https://www.codacy.com/app/j-r-sharpe-github/flash
  :alt: Other Code Issues

.. image:: https://img.shields.io/badge/license-ISC-blue.svg
  :target: https://github.com/textbook/flash/blob/master/LICENSE
  :alt: ISC License

`Flask`_ + Dashboard = Flash. A project dashboard *that works*.

Configuration
-------------

The configuration, either saved in ``config.json`` at the project root or as the
``$FLASH_CONFIG`` environment variable, should look like::

    {
      "project_name": <name of the project>,
      "services": [
        {
          "name": "tracker",
          "api_token": <your API token>,
          "project_id": <your project ID>
        }
      ]
    }

If loading from ``config.json``, any value in the ``"services"`` settings that
``$LOOKS_LIKE_THIS`` (leading ``$``, capital letters and underscores only) will
be assumed to be an environment variable and retrieved accordingly. This lets
you version control most of your configuration without leaking API tokens and
other secrets.

Settings
========

* ``project_name`` - the project's name to display in the footer (defaults to
  ``"unnamed"``)
* ``services`` - an array of service configurations (see `flash_services`_ for
  details and configuration options)
* ``style`` - the stylesheet to use (defaults to ``"default"``, which is
  currently the only option...)
* ``project_end`` - the end data and time of the project, in any format accepted
  by `Moment.js`_. If provided, a countdown to this point will be shown in the
  footer (no default, if not provided no countdown is shown).

Running it
----------

If you just want to run Flash locally, you can use the included ``Dockerfile``
to build and run a `Docker`_ container. This is a two-step process, after which
Flash will be available at ``$(docker-machine ip):5000``::

    docker build -t textbook/flash .
    docker run -p 5000:5000 -d textbook/flash

If your ``config.json`` includes environment variable references, or you want
to override the configuration completely with ``$FLASH_CONFIG``, you can supply
environment variables at ``docker run`` time with the ``-e`` command.

Developing it
-------------

The easiest way to install Flash for development is:

1. Install the dependencies: ``pip3 install -r requirements.txt``

2. Install the package in development mode: ``python3 setup.py develop``

3. To run it locally, edit ``flash/config.json`` or provide ``$FLASH_CONFIG``
   then run: ``python3 scripts/launch.py``

4. To run the tests, use ``python setup.py test`` or run ``py.test`` directly.
   In the latter case, use ``--runslow --Firefox`` (or another browser of your
   choice) to include the integration tests, and see `the docs`_ for
   ``pytest-pylint`` configuration options.

The templates are written using the `Jinja2`_ template language.

Deploying it
------------

Flash can easily be deployed to any `Cloud Foundry`_ environment. An example
``manifest.yml`` is included with the project, showing how to configure the
deployment with an app name and a random route. Once you have installed the CLI
and selected an appropriate target org and space, you can simply ``cf push``.

Alternatively, build a Docker container as above and deploy to an online
container hosting service.

.. _Cloud Foundry: https://cloudfoundry.org/
.. _Codeship: https://codeship.com/
.. _Docker: https://docs.docker.com/
.. _Flask: http://flask.pocoo.org/
.. _flash_services: https://github.com/textbook/flash_services
.. _Jinja2: http://jinja.pocoo.org/docs/dev/
.. _GitHub: https://github.com/
.. _Moment.js: http://momentjs.com/
.. _Pivotal Tracker: https://www.pivotaltracker.com/
.. _the docs: https://pypi.python.org/pypi/pytest-pylint
.. _Travis CI: https://travis-ci.org/
