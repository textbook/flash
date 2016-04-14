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
  :target: https://github.com/textbook/halliwell/blob/master/LICENSE
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

* ``github`` - for project repositories on `GitHub`_

  * ``api_token`` (required),
  * ``account`` (required - the name of the account the project is in, e.g.
  ``"textbook"``)
  * ``app`` (required - the name of the project application within that account,
  e.g. ``"flash"``)
  * ``branch`` (the name of the branch to show commits from, defaulting to the
  repository's default branch, which is usually ``master``).

* ``codeship`` - for CI builds on `Codeship`_

  * ``api_token`` (required)
  * ``project_id`` (required)

* ``tracker`` - for projects on `Pivotal Tracker`_

  * ``api_token`` (required)
  * ``project_id`` (required)

* ``travis`` - for CI builds on `Travis CI`_ (currently only supports open-source builds on the ``.org`` site).

  * ``account`` (required)
  * ``app`` (required)

Running it
----------

The easiest way to install Flash for development is:

1. Install the dependencies: ``pip3 install -r requirements.txt``
        
2. Install the package in development mode: ``python3 setup.py develop``
        
3. To run it locally, save a configuration as either ``config.json`` or
   ``$FLASH_CONFIG`` then run: ``python3 scripts/launch.py``
      
4. To run the tests, use ``python setup.py test`` or run ``py.test``; the latter
   allows you to add flags such as ``--runslow`` (to include the integration
   tests) or ``--pytest-pylint`` (to lint the package before testing).
   
The templates are written using the `Jinja2`_ template language.


.. _Codeship: https://codeship.com/
.. _Flask: http://flask.pocoo.org/
.. _Jinja2: http://jinja.pocoo.org/docs/dev/
.. _GitHub: https://github.com/
.. _Pivotal Tracker: https://www.pivotaltracker.com/
.. _Travis CI: https://travis-ci.org/
