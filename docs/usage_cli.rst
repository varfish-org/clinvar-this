.. _usage-cli:

==================
Command Line Usage
==================

After installation, you can run ``clinvar-this``:

.. code-block:: console

    $ clinvar-this --help

    usage: clinvar-this [-h] [--verbose]

    options:
      -h, --help  show this help message and exit
      --verbose   Enable more verbose output

-------------
Configuration
-------------

The configuration will be stored in ``~/.config/clinvar-this/config.toml`` in `TOML format <https://toml.io/en/>`__.
The file can have multiple sections, each one configuring a **profile**.
You should probably configure a ``default`` profile.
You can set values using ``clinvar-this config set NAME VALUE`` and read values with ``clinvar-this config get NAME``.
A minimal configuration file looks as follows:

.. code-block:: toml

    [default]
    auth_token = "01234567890abcdefghijklm0987654321"

Before you can use ``clinvar-this`` for the first time, you have to configure the API token to use with the ClinVar submission API.

.. code-block:: console

    $ clinvar-this set auth_token YOURTOKENHERE

Note that configuration values will be shown in full when using ``varfish-cli config get/set``.
Subsequently when using the tool for API submission, it will only show the first 5 characters of the secret key.
This allows to determine whether the right key is used but the value is safe enough to go to local log files etc.
However, you should still ensure to take appropriate care when exposing these 5 first characters where applicable.
