from setuptools import find_packages, setup


setup(
    name='django-orderable',
    packages=find_packages(),
    include_package_data=True,
    version='2.0.3',
    description='Orderable model and admin',
    author='Incuna Ltd',
    author_email='dev@incuna.com',
    url='https://github.com/incuna/django-orderable',
    long_description=open('README.rst').read(),
)
