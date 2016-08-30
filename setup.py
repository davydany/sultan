from setuptools import setup, find_packages

setup(
    name='sultan',
    description='Rule Bash like a Sultan',
    version='0.1',
    author='David Daniel',
    author_email='davydany@aeroxis.com',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='http://github.com/aeroxis/sultan'
)