import sys
from setuptools import setup, find_packages, find_namespace_packages

with open("README.md") as readme:
    long_description = readme.read()

PACKAGE_DATA = {"": ["*.txt", "*.json"]}

setup(
    name="esri_rest_json_extractor_converter",
    version="0.0.1",
    description="Module for scoring text based of simplistic measures.",
    long_description=long_description,
    author="Sam Rooney",
    url="https://github.com/samroon2/esri_rest_json_extractor_converter",
    license="Apache License, Version 2.0",
    keywords=[
        "esri",
        "geojson",
        "json",
        "mapserver",
        "geo data",
        "gis"
    ],
    install_requires=[
        "pandas==0.24.2",
        "Fiona==1.8.6",
        "requests>=2.20.0",
        "tqdm==4.28.1",
        "geopandas==0.5.0",
    ],
    tests_require=[
        "pytest>=3.0.0"
    ],
    packages=find_namespace_packages(),
    package_data=PACKAGE_DATA,
    python_requires='>=3.6.1'
)