|language| |license|

==============
docker-cleaner
==============

Description
~~~~~~~~~~~

This utility is designed for cleaning up docker resources.

Installation
~~~~~~~~~~~~

``python setup.py install``

or

``pip install -e .``

or

``pip install docker-cleaner``

How to use
~~~~~~~~~~

Run ``docker-cleaner images -t 120 -o 120 -f images --images-include foo-image bar-image -u -l docker-cleanr.log``

Also checkout list of `arguments`_

arguments
^^^^^^^^^

* ``resources`` - List of resources for removing. Choose from: ``images``, ``volumes``, ``all``
* ``-f, --force`` - Force removing of resources. Choose from: ``images``, ``volumes``, ``all``
* ``-u, --untagged`` - Remove untagged images
* ``-v, --client-version`` - Version of docker client to use
* ``-o, --older`` - Clear resources that older amount of time (in minutes)
* ``--images-include`` - Filter images that only contains any of that names
* ``--volumes-include`` - Filter volumes that only contains any of that name
* ``--images-exclude`` - Exclude images that contains any of that names
* ``--volumes-exclude`` - Exclude volumes that contains any of that name
* ``-t, --timeout`` - Timeout of cleaning. Live it empty in case of using cron job.
* ``-l, --log`` - Redirect logging to file

.. |language| image:: https://img.shields.io/badge/language-python-blue.svg
.. |license| image:: https://img.shields.io/badge/license-Apache%202-blue.svg

