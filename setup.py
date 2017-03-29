from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='akamaiapi', 
    version='1.0.0rc3',
    description='Simple accesss to Akamai APIs',
    url='https://gthub.com/ws0w/akamaiapi',
    license='MIT',
    author='Dan Campbell',
    author_email='ws0w@github.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

         'License :: OSI Approved :: MIT License',

         'Programming Language :: Python :: 2.6',
         'Programming Language :: Python :: 2.7',
         'Programming Language :: Python :: 3.4',
         'Programming Language :: Python :: 3.5',
         'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    keywords='simple akamai api'
)
