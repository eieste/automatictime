# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="automatictime",
    version="1.0.0",
    author="Stefan Eiermann",
    author_email="foss@ultraapp.de",
    description=("Sets your Working Hours automaticly to your Google Spreadsheet."),
    license="AGPL",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["google-auth-httplib2==0.1.0", "google-auth==2.6.0", "google-api-python-client==2.36.0",
                      "google-auth-oauthlib==0.4.6"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console"
        "Operating System :: Unix",
    ],
    entry_points={'console_scripts': ['automatictime = automatictime.args:CliParser.initialize']},
)
