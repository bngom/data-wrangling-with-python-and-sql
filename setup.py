from setuptools import find_packages
from setuptools import setup

setup(
    name="pysql-cli",
    version="0.0.1",
    description="This package contains code for programmatic access to sql server db",
    author="Barthelemy NGOM",
    url="https://github.com/bngom/data-wrangling-with-python-and-sql",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pysql-cli = src.main:cli",
        ],
    },
)