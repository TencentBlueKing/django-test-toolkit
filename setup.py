# -*- coding: utf-8 -*-
import os
from codecs import open
from setuptools import find_packages, setup

with open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-test-toolkit",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/TencentBlueKing/django-test-toolkit",
    description="Toolkit for test based on Django",
    long_description=README,
    long_description_content_type="text/markdown",
    author="normal-wls",
    install_requires=[
        "djangorestframework",
        "Django",
        "factory-boy"
    ],
    zip_safe=False,
)
