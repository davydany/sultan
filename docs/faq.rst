==========================
Frequently Asked Questions
==========================

What is Sultan?
---------------

Sultan allows you to interface with command-line utilities from Python without
having to write your scripts in Bash. 

Why use Sultan?
---------------

Leverage the Power of Bash from Python
**************************************

Bash, while it seems arcane, actually is quite powerful! Creating a Tar Archive
of a directory requires us to read up on the tar API or check StackOverflow, but
if you know how to do it in Bash, you'd be done before you finish reading the 
StackOverflow post!

This promotes simplicity, and follows the KISS principle 
(Keep It Simple Stupid!)

Better Syntax:
**************

Bash's syntax for loops, conditionals, and functions work well, but require a 
lot of nuances that we're just not used to with a modern language like Python. 

Sultan allows you to use Python Syntax, and never touch Bash's arcaine syntax 
ever again!

Project Management:
*******************

Sultan was designed because Bash just does not scale well with most projects. 
As much as we can try, Bash does not have a proper package management system. 
So, we're left with script files that are sourced, and called, but it gets quiet
complicated as soon as you have more than 10 scripts. 

Python has a great package and module system that allows us to create complex 
projects using the Python language, but also leverage a lot of great tools and
functionality that we've grown to love and expect from Bash.

This promotes reusability, with the DRY (Don't Repeat Yourself) principle. If 
you create a great solution with Sultan, publish it on **PyPi** and others will 
use it.

Unit Testing
************

Out of the Box, Bash does not come with any Unittesting frameworks, but Python
does! You can build unittests and integration tests with Sultan to ensure your
code does *EXACTLY* what you want it to do.

Why can't I use `subprocess`?
-----------------------------

Python's standard library offers the subprocess library, but it isn't very 
"Pythonic". The 'subprocess' module has a bunch of methods for writing commands
to the shell, but the code is overly verbose, and tough to read. 

Any reason to use this over ansible or saltstack?
-------------------------------------------------

Sultan is just a simpler interface to command line utilities. It helps bypass
the arcane language constructs of Bash (among other things. 
See **Why use Sultan?** above). 

Sultan was created to help with scripts that we create with Bash, that tend to get
complex. When these scripts get complex, Bash just gets to be a pain to deal 
with, since it lacks proper package management, it lacks unit testing, and 
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
