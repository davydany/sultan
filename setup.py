from setuptools import setup, find_packages

with open("./README.rst") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='sultan',
    description='Command and Rule over your Shell',
    long_description=LONG_DESCRIPTION,
    version='0.2',
    author='David Daniel',
    author_email='davydany@aeroxis.com',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='http://github.com/aeroxis/sultan'
)
