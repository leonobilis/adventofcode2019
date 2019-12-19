from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='adventofcode2019',
    version='1.0',
    install_requires=requirements,
    author='marlew',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/lev7/adventofcode2019',
    description='Advent of Code 2019'
)
