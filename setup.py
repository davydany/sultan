from setuptools import setup, find_packages

LONG_DESCRIPTION = """

## What is Sultan?

Sultan is an interface to Bash from Python. Shell commands get to the point of 
what you want them to do. For example, 

```
sudo yum install tree
```

would install `tree` on your local machine. However, we normally access command 
line utilities like `yum`, via bash, and Bash is just not as nice as Python. 
Python's beautiful syntax make code readable and easy to maintain far more than
Bash.

Bash is great for small scripts, but when we get complex scripts, Bash just 
gets very tough to use. This is why Sultan was created.

Sultan allows you to run bash commands from inside Python using simple function 
calls. Here is a quick example to install tree via Sultan.

```
from sultan.api import Sultan

def install_tree():
    s = Sultan()
    s.sudo("yum install -y tree").run()
```
"""

setup(
    name='sultan',
    description='Command and Rule over your Shell',
    long_description=LONG_DESCRIPTION,
    version='0.1.13',
    author='David Daniel',
    author_email='davydany@aeroxis.com',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='http://github.com/aeroxis/sultan'
)
