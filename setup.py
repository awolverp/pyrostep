from setuptools import setup, find_packages

VERSION = "2.10.10"

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
    packages=find_packages(".", exclude=["examples"]),
    requires=["pyrogram"],
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
    license="GPLv2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ]
)
