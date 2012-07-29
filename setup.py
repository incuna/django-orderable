from setuptools import find_packages, setup

from orderable import get_version


setup(
    name='django-orderable',
    packages=find_packages(),
    include_package_data=True,
    version=get_version(),
    description='Orderable model and admin',
    author='Incuna Ltd',
    author_email='dev@incuna.com',
    url='http://incuna.com/',
    long_description=open('README.rst').read(),
)
