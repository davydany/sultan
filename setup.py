from setuptools import setup, find_packages

with open("./README.rst") as f:
    LONG_DESCRIPTION = f.read()

with open("./VERSION") as f:
    VERSION = f.read().strip()

setup(
    name='sultan',
    description='Command and Rule over your Shell',
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    author='David Daniel',
    author_email='davydany@aeroxis.com',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='http://github.com/aeroxis/sultan',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.3",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Unix Shell",
        "License :: OSI Approved :: MIT License"]
)
