from setuptools import find_packages
from setuptools import setup

setup(
    name='cae_microphone_array',
    version='0.0.1',
    packages=find_packages(
        include=('cae_microphone_array', 'cae_microphone_array.*')),
)
