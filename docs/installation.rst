.. highlight:: shell

============
Installation
============


--------------------
Stable Release (Pip)
--------------------

To install ClinVar This!, run this command in your terminal:

.. code-block:: console

    $ pip install clinvar-this

This is the preferred method to install ClinVar This!, as it will always install the most recent stable release.

If you don't have `pip <https://pip.pypa.io>`__ installed, this `Python installation guide <http://docs.python-guide.org/en/latest/starting/installation/>`__ can guide you through the process.


----------------------
Stable Release (Conda)
----------------------

As a prerequisite, you have to install conda and setup the bioconda channel `as documented on the Bioconda website <https://bioconda.github.io/index.html#usage>`__.

Then, you can create a new environment with ``clinvar-this``.

.. code-block:: console

    $ conda create -y -n clinvar-this python=3.11 clinvar-this

Or install the package in your current environment:


.. code-block:: console

    $ conda install -y clinvar-this


------------
From Sources
------------

The sources for ClinVar This! can be downloaded from the `Github repo <https://github.com/bihealth/clinvar-this>`__.

Clone the public repository:

.. code-block:: console

    $ git clone https://github.com/bihealth/clinvar-this.git
