# Copyright (c) 2011 Tuenti Technologies
# See LICENSE for details

from distutils.core import setup

setup(name='puppet-enc',
    version='0.5',
    description='Generic external node classifier for puppet',
    author='Jaime Soriano Pastor',
    author_email='jsoriano@tuenti.com',
    url='https://github.com/jsoriano/puppet-enc',
    license='MIT',
    package_dir={'': 'src'},
    packages=[
        'puppetenc',
        'puppetenc.migrations',
    ],
    scripts=[
        'scripts/puppet-enc',
    ],
    data_files=[
        ('/etc/puppet-enc', ['etc/enc_settings.py']),
    ],
)
