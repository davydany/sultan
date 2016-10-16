
========
Examples
========

This tutorial will go through various examples to help in better understanding
how to use Sultan. Each example will build on the lessons learned from the  
previous examples. 

Example 1: Getting Started
--------------------------

We typically use `yum` or `apt-get` to install a package on our system. 
This example installs a package on our system using Sultan. Here is how
to get started::

    from sultan.api import Sultan

    s = Sultan()
    s.yum("install", "-y", "tree").run()

Sultan allows multiple syntaxes depending on what your first command is.
Suppose you want to not use separate tokens, and instead you want to use
one string, you can write the above example as such::


    from sultan.api import Sultan

    s = Sultan()
    s.yum("install -y tree").run()

Suppose your user is not a root-user, and you want to call to sudo to install
the `tree` package. You'd do the following::

    from sultan.api import Sultan

    with Sultan.load(sudo=True) as s:
        s.yum('install -y tree').run()



**NOTE:** For the sake of brevity, this tutorial will now start to assume that
`Sultan` has been imported from `sultan.api` and, the variable `s` has been 
instantiated as an instance of `Sultan` (`s = Sultan()`). This will change in
situations where the documentation requires a different usage.

Example 2: Sultan with Context Management
-----------------------------------------

There are times when we want to manage the context of where Sultan executes 
your code. To aid with this, we use Sultan in Context Management mode.

Suppose we want to cat out the contents of `/etc/hosts`, we'd do the following::

    with Sultan.load(cwd="/etc") as s:
        s.cat("hosts").run()

Example 3: Compounding with And (&&)
------------------------------------

There are times when we need multiple commands to run at once. We use the 
`and_()` command to get through this. Here is an example::

    # runs: 'cd /tmp && touch foobar.txt'
    s.cd("/tmp").and_().touch("foobar.txt").run()

Example 4: Redirecting with Pipes (|)
-------------------------------------

In Bash, we use the pipe `|` operator to redirect the output of the call to a 
command to another command. We do this in Sultan with the `pipe` command. Here
is an example::

    # runs: 'ls -l | sed -e "s/[aeio]/u/g"'
    s.ls('-l').pipe().sed('-e', '"s/[aeio]/u/g"').run()

Example 5: Redirecting Output to File
-------------------------------------

In Bash, we often want to redirect the output of a command to file. Whether 
the output is in `stdout` or `stderr`, we can redirect it to a file with 
Sultan. Here is an example::

    # runs: 'cat /etc/hosts > ~/hosts'
    s.cat("/etc/hosts").redirect(
        "~/hosts", 
        append=False, 
        stdout=True, 
        stderr=False)

In the example above, we redirected the output of `/etc/hosts` to `~/hosts`. 
We only outputted the `stdout`, and didn't append to the file if it existed.
Feel free to customize this method as it fits your needs. 

Example 6: Read from Standard Input
-----------------------------------

Python has the `raw_input` built-in to read from standard input. Sultan's API 
wraps around `raw_input` to ask the user for their input from the command line
and returns the value.

Here is the example::

    name = s.stdin("What is your name?")
    print "Hello %s" % name

Example 7: Running as Another User
----------------------------------

Sultan can run commands as another user. You need to enable `sudo` 
mode to do this.

Here is an example::

    # runs: sudo su - hodor -c 'cd /home/hodor && ls -lah .;'
    with Sultan.load(sudo=True, user='hodor', cwd='/home/hodor') as s:
        sultan.ls('-lah', '.')

Example 8: Running as Root
--------------------------

Sultan can run commands as the `root` user. You need to only enable `sudo` 
mode to do this.

Here is an example::

    # runs: sudo su - root -c 'ls -lah /root;'
    with Sultan.load(sudo=True) as sultan:
        sultan.ls('-lah', '/root')
