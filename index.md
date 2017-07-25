# Sultan

<img src="https://raw.githubusercontent.com/aeroxis/sultan/master/img/sultan-logo.png" alt="sultan logo" align="right" />

**Command and Rule over your Shell**

[![Build Status](https://travis-ci.org/aeroxis/sultan.svg?branch=master)](https://travis-ci.org/aeroxis/sultan)

**NOTE 1:** Sultan only supports Python `2.7.x`.

**NOTE 2:** Your input is welcome! Please provide your feedback by creating 
[issues on Github](https://github.com/aeroxis/sultan/issues).

## What is Sultan?
Sultan is an interface to Bash from Python. Shell commands get to the point of 
what you want them to do. For example, 

```bash
sudo yum install tree
```

would install `tree` on your local machine. However, we normally access command 
line utilities like `yum`, via bash, and Bash is just not as nice as Python. 
Python's beautiful syntax make code readable and easy to maintain far more than
Bash.

Bash is great for small scripts, but when we get complex scripts, Bash just 
gets very tough to use. This is why Sultan was created.

# Basic Usage

Sultan allows you to run bash commands from inside Python using simple function 
calls. Here is a quick example to install tree via Sultan.

```python
from sultan.api import Sultan

def install_tree():
    s = Sultan()
    s.sudo("yum install -y tree").run()
```

Here is the output:

```bash
sudo yum install -y tree;
Loaded plugins: fastestmirror, langpacks
Loading mirror speeds from cached hostfile
 * epel: ca.mirror.babylon.network
 * nux-dextop: mirror.li.nux.ro
Resolving Dependencies
--> Running transaction check
---> Package tree.x86_64 0:1.6.0-10.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================
 Package      Arch           Version                Repository             Size
================================================================================
Installing:
 tree         x86_64         1.6.0-10.el7           CentOS-7-Base          46 k

Transaction Summary
================================================================================
Install  1 Package

Total download size: 46 k
Installed size: 87 k
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : tree-1.6.0-10.el7.x86_64                                     1/1 
  Verifying  : tree-1.6.0-10.el7.x86_64                                     1/1 

Installed:
  tree.x86_64 0:1.6.0-10.el7                                                    

Complete!

```

## Advanced Usage 

The following are advanced usage of Sultan:

### Pipe

In bash, we'd like to pipe multiple commands to take the output of the first
command and send it to the second command. For example, suppose we want to 
find all the files that contain the word `Sultan` in a bunch of files in a 
given directory. We would do this:

```bash
find ~/projects/sultan -name "*.py" | xargs grep "Sultan"
```

We would do the following with Sultan:

```python
s = Sultan()
response = s.find("~/projects/sultan -name '*.py'").pipe().grep("Sultan").run()
```

### And

In bash, we'd like to run two commands together, like changing to a directory 
and running a command there, like:

```bash
cd /tmp/ && ls -lah
``` 

We would do the following with Sultan:

```python
s = Sultan()
response = s.cd("/tmp").and_().ls("-lah")
```

### Redirect

In bash, something we do a lot is redirect output (`stdout`, `stderr`) into a 
file. We would do it like this:

```bash
find / -type d > /tmp/contents
```

We would do the following with Sultan:

```python
s = Sultan()
response = s.find("/ -type d").redirect("/tmp/contents", stdout=True)
```

### Custom commands

Sultan still needs a lot of work and we understand that. We encourage you to 
create bug reports and feature requests on the Github page at: 
[https://github.com/aeroxis/sultan/issues](https://github.com/aeroxis/sultan/issues)

That being said, if you want to do something custom, run:

```python
s = Sultan()
s.command = "yum install -y gcc"
response = s.run()
```
