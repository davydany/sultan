# Sultan

**Command and Rule over your Shell**

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
