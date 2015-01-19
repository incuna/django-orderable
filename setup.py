from setuptools import find_packages, setup


setup(
    name='django-orderable',
    packages=find_packages(),
    include_package_data=True,
    version='3.1.0',
    description='Orderable model and admin',
    author='Incuna Ltd',
    author_email='dev@incuna.com',
    url='https://github.com/incuna/django-orderable',
    long_description=open('README.rst').read(),
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
