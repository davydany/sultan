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

Sultan now supports the following Python versions:

  - "2.7"
  - "3.3"
  - "3.4"
  - "3.5"
  
----
Note
----
Your input is welcome! Please provide your feedback by creating 
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

.. code:: python

  from sultan.api import Sultan
  s = Sultan()
  s.sudo("yum install -y tree").run()
  
**Runs:** 

.. code:: bash

  sudo install -y tree;

The recommended way of using Sultan is to use it in Context Management mode. 
Here is how to use Sultan with Context Management:

.. code:: python

  from sultan.api import Sultan
  s = Sultan()
  with Sultan.load(sudo=True) as s:
    s.yum("install -y tree").run()

**Runs:** 

.. code:: bash
  
  sudo su - root -c 'yum install -y tree;'

What if we want to install this command on a remote machine? You can easily 
achieve this using context management:

.. code:: python

  from sultan.api import Sultan
  
  with Sultan.load(sudo=True, hostname="myserver.com") as sultan:
    sultan.yum("install -y tree").run()

**Runs:**

.. code:: bash

  ssh root@myserver.com 'sudo su - root -c 'yum install -y tree;''

If you enter a wrong command, Sultan will print out details you need to debug and 
find the problem quickly.

Here, the same command was run on a Mac:

.. code:: python

  from sultan.api import Sultan

  
**Yields:**

.. code:: bash

  [sultan]: sudo su - root -c 'yum install -y tree;'
  Password:
  [sultan]: --{ STDERR }-------------------------------------------------------------------------------------------------------
  [sultan]: | -sh: yum: command not found
  [sultan]: -------------------------------------------------------------------------------------------------------------------

Want to get started? Simply install Sultan, and start writing your clean code::

    pip install --upgrade sultan

If you have more questions, check the docs! http://sultan.readthedocs.io/en/latest/