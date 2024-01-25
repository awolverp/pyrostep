from setuptools import setup

VERSION = "2.10.21"

with open("README.md", "r") as f:
    desc = f.read()

setup(
    name="pyrostep",
    version=VERSION,
    description="A Python library to handle steps in pyrogram framework.",
    long_description=desc,
    long_description_content_type="text/markdown",
    author="aWolver",
    url="https://github.com/awolverp/pyrostep",
    packages=["pyrostep", "pyrostep.connection"],
    keywords=[
        "pyrostep",
        "pyrogram",
        "step handler",
        "pyrogram helper",
        "helper",
        "pyrogram plugin",
        "plugin",
        "pyrogram connection",
    ],
    license="MIT",
    license_files=["LICENSE"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
