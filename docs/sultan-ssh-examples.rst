
===================
Sultan SSH Examples
===================

This tutorial will go through various examples to help in better understanding
how to use Sultan over SSH. Each example will build on the lessons learned from the  
previous examples. 

Example 1: SSH to Remote Host as the Current User
-------------------------------------------------

By default, you can simply specify the host to sultan, and calling the commands 
like you normally do. This uses the username of the user who is executing the 
script, and connects you to the remote host. 

    from sultan.api import Sultan
    
    with Sultan.load(hostname='aeroxis.com') as sultan:
        s.yum('install', '-y', 'tree').run()

Sultan will connect to the remote host, and run `yum install -y tree`. This is 
what is passed to your shell to execute the command 
(assuming your username is `davydany`):

    ssh davydany@aeroxis.com 'yum install -y tree;'

Example 2: SSH to Remote Host as a Different User
-------------------------------------------------

You can specify a different user to execute the remote commands by using the 
`user` parameter, like this:

    with Sultan.load(user='elon.musk', hostname='aeroxis.com') as s:
        s.yum('install', '-y', 'tree').run()

And this will execute:

    ssh elon.musk@aeroxis.com 'yum install -y tree;'

Example 3: Passing Additional Options (Port)
--------------------------------------------

**Added in v0.6**

If you need to pass additional options for the port, use the `SSHConfig` class
to configure the SSH Connection.
    
    from sultan.api import Sultan, SSHConfig
    
    port = 2222
    config = SSHConfig(port=port)
    with Sultan.load(user='elon.musk', 
                     hostname='aeroxis.com', 
                     ssh_config=config) as s:
        s.yum('install', '-y', 'tree').run()
    
which will yield: 

    ssh -p 2222 elon.musk@aeroxis.com 'yum install -y tree;'


Example 4: Passing Additional Options (Identity File)
-----------------------------------------------------

**Added in v0.6**

If you need to pass additional options for the port, use the `SSHConfig` class
to configure the SSH Connection.

    from sultan.api import Sultan, SSHConfig

    path_to_identity_file = '/home/elon.musk/keys/elon.musk.identity'
    config = SSHConfig(identity_file=path_to_identity_file)
    with Sultan.load(user='elon.musk', 
                        hostname='aeroxis.com', 
                        ssh_config=config) as s:
        s.yum('install', '-y', 'tree').run()
    
which will yield: 

    ssh -i /home/elon.musk/keys/elon.musk.identity elon.musk@aeroxis.com 'yum install -y tree;'



Example 3: Compounding with And (&&) and Or (||)
------------------------------------------------

There are times when we need multiple commands to run at once. We use the 
`and_()` command to get through this. Here is an example::

    # runs: 'cd /tmp && touch foobar.txt'
    with Sultan.load() as s:
        s.cd("/tmp").and_().touch("foobar.txt").run()

There are also times that we want to run 2 commands, but run the 2nd command 
even if the first command fails. For this, you will need to use the `or_()`
command. Here is an example::

    # runs: 'mkdir /tmp || mkdir /bar'
    with Sultan.load() as s:
        s.mkdir('/tmp').or_().mkdir('/bar').run()

Example 4: Redirecting with Pipes (|)
-------------------------------------

In Bash, we use the pipe `|` operator to redirect the output of the call to a 
command to another command. We do this in Sultan with the `pipe` command. Here
is an example::

    # runs: 'ls -l | sed -e "s/[aeio]/u/g"'
    with Sultan.load() as s:
        s.ls('-l').pipe().sed('-e', '"s/[aeio]/u/g"').run()

Example 5: Redirecting Output to File
-------------------------------------

In Bash, we often want to redirect the output of a command to file. Whether 
the output is in `stdout` or `stderr`, we can redirect it to a file with 
Sultan. Here is an example::

    # runs: 'cat /etc/hosts > ~/hosts'
    with Sultan.load() as s:
        s.cat("/etc/hosts").redirect(
            "~/hosts", 
            append=False, 
            stdout=True, 
            stderr=False).run()

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
        sultan.ls('-lah', '.').run()

Example 8: Running as Root
--------------------------

Sultan can run commands as the `root` user. You need to only enable `sudo` 
mode to do this.

Here is an example::

    # runs: sudo su - root -c 'ls -lah /root;'
    with Sultan.load(sudo=True) as sultan:
        sultan.ls('-lah', '/root').run()

Example 9: Disable Logging
--------------------------

If you need to disable logging all together, simply add set 'logging' to False 
while loading Sultan with Context.

Here is an example::

    # runs without logging
    with Sultan.load(logging=False) as sultan:
        sultan.ls('-lah', '/tmp').run()

