#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='ISPManCCP',
    version='0.1',
    description='Customer Control Panel to ISPManSoap',
    author='Pedro Algarvio',
    author_email='ufs@ufsoft.org',
    #url='',
    #install_requires=["Pylons>=0.9.6"],
    install_requires=["Pylons>=0.9.6rc3dev-r2352"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'ispman.ccp': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'ispman.cpp': [
    #        ('**.py', 'python', None),
    #        ('**/templates/**.html', 'genshi', None),
    #        ('public/**', 'ignore', None)]},
    entry_points="""
    [paste.app_factory]
    main = ispman.ccp.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
