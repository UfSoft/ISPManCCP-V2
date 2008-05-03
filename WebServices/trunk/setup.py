#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='ISPManSOAP',
    version='0.1',
    description='SOAP backend to ISPMan',
    author='Pedro Algarvio',
    author_email='ufs@ufsoft.org',
    # url='',
    install_requires=["Pylons>=0.9.6.1"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'ispman.soap': ['i18n/*/LC_MESSAGES/*.mo']},
    entry_points="""
    [paste.app_factory]
    main = ispman.soap.wsgiapp:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
