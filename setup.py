from setuptools import find_packages, setup


setup(
    name='django-orderable',
    packages=find_packages(),
    include_package_data=True,
    version='6.1.2',
    description='Add manual sort order to Django objects via an abstract base '
                'class and admin classes.',
    author='Incuna Ltd',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/django-orderable',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
