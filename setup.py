from setuptools import setup, find_packages

setup(
    name="yasl",
    version="0.1",
    description="YASL command line interface",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "yasl = yasl.cli:cli",
        ],
    },
    install_requires=[
        "click",
    ],
)
