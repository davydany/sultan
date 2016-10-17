.. image:: https://raw.githubusercontent.com/aeroxis/sultan/master/docs/img/sultan-logo.png
  :alt: sultan logo
  :align: right

**Command and Rule over your Shell**

.. image:: https://badge.fury.io/py/sultan.svg
  :alt: PyPI Version
  :target: https://badge.fury.io/py/sultan

.. image:: https://travis-ci.org/aeroxis/sultan.svg?branch=master
  :alt: Travis Build Status
  :target: https://travis-ci.org/aeroxis/sultan

.. image:: http://img.shields.io/:license-mit-blue.svg
  :alt: MIT License
  :target: http://doge.mit-license.org

.. image:: https://readthedocs.org/projects/sultan/badge/?version=latest
  :alt: Documentation Status
  :target: http://sultan.readthedocs.io/en/latest/?badge=latest

----
Note
----

1. Sultan currently supports Python `2.7.x`. Version `0.3` of Sultan is 
slated to support Python `3.0`.

2. Your input is welcome! Please provide your feedback by creating 
`issues on Github <https://github.com/aeroxis/sultan/issues>`_

-------------
Documentation
-------------

.. image:: https://readthedocs.org/projects/sultan/badge/?version=latest
  :alt: Documentation Status
  :target: http://sultan.readthedocs.io/en/latest/?badge=latest

Documentation is available on ReadTheDocs: http://sultan.readthedocs.io/en/latest/

---------------
What is Sultan?
---------------

Sultan is a Python package for interfacing with command-line utilities, like 
`yum`, `apt-get`, or `ls`, in a Pythonic manner. It lets you run command-line 
utilities using simple function calls. 

The simplest way to use Sultan is to just call it:

.. image:: https://raw.githubusercontent.com/aeroxis/sultan/master/docs/img/readme-1-simple-usage.png
  :alt: Sultan's Simple usage
  :width: 750 px

The recommended way of using Sultan is to use it in Context Management mode. 
Here is how to use Sultan with Context Management:

.. image:: https://raw.githubusercontent.com/aeroxis/sultan/master/docs/img/readme-2-context-manager.png
  :alt: Sultan's Context Manager
  :width: 750 px

What if we want to install this command on a remote machine? You can easily 
achieve this using context management:

.. image:: https://raw.githubusercontent.com/aeroxis/sultan/master/docs/img/readme-3-ssh-access.png
  :alt: Sultan's Context Manager for SSH access
  :width: 750 px

If you enter a wrong command, Sultan will print out details you need to debug and 
find the problem quickly.

Here, the same command was run on a Mac:

.. image:: https://raw.githubusercontent.com/aeroxis/sultan/master/docs/img/readme-4-error-message.png
  :alt: Sultan's Error Management
  :width: 750 px

Want to get started? Simply install Sultan, and start writing your clean code::

    pip install --upgrade sultan

If you have more questions, check the docs! http://sultan.readthedocs.io/en/latest/