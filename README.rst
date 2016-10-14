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

Here is how you'd use Sultan::

    from sultan.api import Sultan

    def install_tree():
        '''
        Install 'tree' package.
        '''
        s = Sultan()
        s.sudo("yum install -y tree").run()

Here is how to use Sultan with Context Management::

    from sultan.api import Sultan

    def echo_hosts():
        '''
        Echo the contents of `/etc/hosts`
        '''
        with Sultan.load(cwd="/etc") as s:
            s.cat("hosts").run()

That's it!