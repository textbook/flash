Flash
=====

Flask project dashboards.

Configuration
-------------

The configuration, either saved in ``config.json`` at the project root or as the
``$FLASH_CONFIG`` environment variable, should look like::

    {
      "project_name": "Gnome",
      "services": [
        {
          "name": "tracker", 
          "api_token": <your API token>,
          "project_id": <your project ID>
        },
        {
          "name": "codeship",
          "api_token": <your API token>,
          "project_id": <your project ID>
        }
      ]
    }


Running it
----------

The easiest way to install Flash for development is:

1. Install the dependencies: ``pip3 install -r requirements.txt``
        
2. Install the package in development mode: ``python3 setup.py develop``
        
3. To run it locally, save a configuration as either ``config.json`` or
``$FLASH_CONFIG`` then run: ``python3 scripts/launch.py``
      
4. To run the tests, use ``python setup.py test`` or run ``py.test``; the latter
allows you to add flags such as ``--runslow`` (to include the integration tests)
or ``--pytest-pylint`` (to lint the package before testing).