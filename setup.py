"""Setup script for videoflow factory"""

import os.path
import setuptools
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

__version__ = None  # set __version__ in this exec() call
exec(open("videoflow-factory/version.py").read())
# This call to setup() does all the work

setup(
    name="videoflow-factory",
    version=__version__,
    description="videoflow_factory",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kaushikb11/videoflow-factory",
    author="Kaushik Bokka",
    author_email="kaushikbokka@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    zip_safe=False,
    include_package_data=True,
)
