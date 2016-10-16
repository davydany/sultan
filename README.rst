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

    # simple way
    s = Sultan()
    s.sudo("yum install -y tree").run()

    # with context management (recommended)
      with Sultan.load(sudo=True) as s:
          s.yum("install -y tree").run()

What if we want to install this command on a remote machine? You can easily 
achieve this using context management::

  with open(sudo=True, hostname="myserver.com") as s:
    s.yum("install -y tree").run()

If you enter a wrong command, Sultan will print out details you need to debug and 
find the problem quickly.

Here, the same command was run on a Mac::

    In [1]: with Sultan.load(sudo=True) as s:
      ...:     s.yum("install -y tree").run()
      ...:
    [sultan]: sudo su - root -c 'yum install -y tree;'
    Password:
    [sultan]: Unable to run 'sudo su - root -c 'yum install -y tree;''
    [sultan]: --{ TRACEBACK }----------------------------------------------------------------------------------------------------
    [sultan]: | Traceback (most recent call last):
    [sultan]: |   File "/Users/davydany/projects/aeroxis/sultan/src/sultan/api.py", line 159, in run
    [sultan]: |     stdout = subprocess.check_output(commands, shell=True, stderr=stderr)
    [sultan]: |   File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 573, in check_output
    [sultan]: |     raise CalledProcessError(retcode, cmd, output=output)
    [sultan]: | CalledProcessError: Command 'sudo su - root -c 'yum install -y tree;'' returned non-zero exit status 127
    [sultan]: -------------------------------------------------------------------------------------------------------------------
    [sultan]: --{ STDERR }-------------------------------------------------------------------------------------------------------
    [sultan]: | -sh: yum: command not found
    [sultan]: -------------------------------------------------------------------------------------------------------------------

Want to get started? Simply install Sultan, and start writing your clean code::

    pip install --upgrade sultan

If you have more questions, check the docs! http://sultan.readthedocs.io/en/latest/