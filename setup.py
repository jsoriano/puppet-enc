# Copyright (c) 2011 Tuenti Technologies
# See LICENSE for details

import os.path

from distutils.core import setup
from distutils.sysconfig import get_python_lib

setup(name='puppet-enc',
    version='1.0',
    description='Generic external node classifier for puppet',
    author='Jaime Soriano Pastor',
    author_email='jsoriano@tuenti.com',
    url='https://github.com/jsoriano/puppet-enc',
    license='MIT',
    package_dir={'': 'src'},
    packages=[
        'puppetenc',
        'puppetenc.migrations',
        'puppetenc.migrations.versions',
    ],
    scripts=[
        'scripts/puppet-enc',
    ],
    data_files=[
        ('/etc/puppet-enc', [
            'etc/enc_settings.py'
        ]),
        (os.path.join(get_python_lib(), 'puppetenc/migrations'), [
            'src/puppetenc/migrations/migrate.cfg'
        ]),
    ],
)
