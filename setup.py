from setuptools import setup, find_packages

setup(
    name='sultan',
    description='Command and Rule over your Shell',
    version='0.1.5',
    author='David Daniel',
    author_email='davydany@aeroxis.com',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='http://github.com/aeroxis/sultan'
)
