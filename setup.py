from setuptools import setup, find_packages

setup(
    name="BicimadFlorentino",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
          'pandas==2.2.2',
          'matplotlib==3.9.1',
          'requests == 2.1',
      ]

)