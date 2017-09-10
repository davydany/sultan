
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
script, and connects you to the remote host. ::

    from sultan.api import Sultan
    
    with Sultan.load(hostname='aeroxis.com') as sultan:
        s.yum('install', '-y', 'tree').run()

Sultan will connect to the remote host, and run `yum install -y tree`. This is 
what is passed to your shell to execute the command 
(assuming your username is `davydany`)::

    ssh davydany@aeroxis.com 'yum install -y tree;'

Example 2: SSH to Remote Host as a Different User
-------------------------------------------------

You can specify a different user to execute the remote commands by using the 
`user` parameter, like this::

    with Sultan.load(user='elon.musk', hostname='aeroxis.com') as s:
        s.yum('install', '-y', 'tree').run()

And this will execute::

    ssh elon.musk@aeroxis.com 'yum install -y tree;'

Example 3: Passing Additional Options (Port)
--------------------------------------------

**Added in v0.6**

If you need to pass additional options for the port, use the `SSHConfig` class
to configure the SSH Connection.::
    
    from sultan.api import Sultan, SSHConfig
    
    port = 2222
    config = SSHConfig(port=port)
    with Sultan.load(user='elon.musk', 
                     hostname='aeroxis.com', 
                     ssh_config=config) as s:
        s.yum('install', '-y', 'tree').run()
    
which will yield::

    ssh -p 2222 elon.musk@aeroxis.com 'yum install -y tree;'


Example 4: Passing Additional Options (Identity File)
-----------------------------------------------------

**Added in v0.6**

If you need to pass additional options for the port, use the `SSHConfig` class
to configure the SSH Connection.::

    from sultan.api import Sultan, SSHConfig

    path_to_identity_file = '/home/elon.musk/keys/elon.musk.identity'
    config = SSHConfig(identity_file=path_to_identity_file)
    with Sultan.load(user='elon.musk', 
                        hostname='aeroxis.com', 
                        ssh_config=config) as s:
        s.yum('install', '-y', 'tree').run()
    
which will yield::

    ssh -i /home/elon.musk/keys/elon.musk.identity elon.musk@aeroxis.com 'yum install -y tree;'

