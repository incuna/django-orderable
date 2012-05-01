from os.path import dirname, join
from setuptools import find_packages, setup

from orderable import get_version

def fread(fname):
    with open(join(dirname(__file__), fname), 'r') as f:
        return f.read()

setup(
    name = "django-orderable",
    packages = find_packages(),
    include_package_data=True,
    version = get_version(),
    description = "",
    author = "Incuna Ltd",
    author_email = "dev@incuna.com",
    url = "http://incuna.com/",
    long_description=fread("README.rst"),
)