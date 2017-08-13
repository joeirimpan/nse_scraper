# -*- coding: utf-8 -*-
import setuptools


requirements = [
    'cherrypy',
    'redis',
    'requests'
]

test_requirements = ['flake8', 'pytest', 'vcrpy']

setuptools.setup(
    name="nse-scraper",
    version="0.0.4",
    url="https://github.com/joeirimpan/nse_scraper",

    author="Joe Paul",
    author_email="joeirimpan@gmail.com",

    description="A web app displaying real time stocks from NSE.",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=requirements,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
