==========================
Frequently Asked Questions
==========================

**What is Sultan?**

Sultan allows you to interface with command-line utilities from Python without
having to write your scripts in Bash. 

**Why can't I use `subprocess`?**

Python's standard library offers the subprocess library, but it isn't very 
"Pythonic". The 'subprocess' module has a bunch of methods for writing commands
to the shell, but the code is overly verbose, and tough to read. 

**Any reason to use this over ansible or saltstack?**

Sultan is just a simpler interface to command line utilities. It helps bypass
the arcane language constructs of Bash. 

Sultan is made to help with scripts that we create with Bash, that tend to get
complex. When these scripts get complex, Bash just gets to be a pain to deal 
with, since it lacks package management, it lacks unit testing, and 
<insert library that you need for managing complex scripts>. 
So Sultan allows scripts to be reusable and tested with standard Python. 

Ansible and Salt are powerful for provisioning a system. Sultan can't compete 
in that realm, but it does help with complex scripts. Even if you want Ansible 
or Salt to perform something on a remote box, like installing a package, it 
requires some overhead in setting them up. Sultan is simple with no external 
dependencies, and installs itself with just "pip install sultan".

Sultan simply wraps the subprocess module in Python's standard library, but it 
also provides a nice to read logging system, and provides you with relevant 
information when a command fails.

All in all, it can't compete with standard DevOps tools used for provisioning. 
It does help with not having to use Bash heavily, if you're a Python programmer.