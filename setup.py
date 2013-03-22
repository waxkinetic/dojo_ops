from __future__ import absolute_import

from setuptools import setup, find_packages

readme = open('README.md').read()

setup(
    name='dojo_ops',
    version='0.01-dev',
    url='http://github.com/waxkinetic/dojo_ops',
    license='BSD',

    author='Rick Bohrer',
    author_email='waxkinetic@gmail.com',

    description='dojo operations scripts.',
    long_description=readme,

    zip_safe=False,
    include_package_data=True,

    packages=find_packages(),

    setup_requires=[
        'setuptools-git >= 1.0b1'
    ],

    dependency_links=[
        'https://github.com/waxkinetic/awsspotmonitor/tarball/master#egg=awsspotmonitor-0.01-dev',
        'https://github.com/waxkinetic/fabcloudkit/tarball/master#egg=fabcloudkit-0.02' 
    ],

    install_requires=[
        'boto >= 2.8.0',
        'awsspotmonitor >= 0.01-dev',
        'fabcloudkit >= 0.02'
    ]
)
