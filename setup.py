#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['']

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='PyBackup',
    version='0.0.2',
    description=('Python module for Backup routines'
                 'of files and folders'),
    long_description=readme,
    author="Fabricio Roberto reinert",
    author_email='fabricio.reinert@live.com',
    url='https://github.com/FRReinert/PyBackup',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='Python, backup, files, folders',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests.test_app.tests',
    tests_require=test_requirements
)
