#!/usr/bin/env python
import os
import sys

from migrate.versioning.shell import main
from migrate.versioning import api
from puppetenc.config import settings

params = {
    'repository': os.path.dirname(__file__),
    'url': settings.db_url,
}

def version_control():
    global params
    api.version_control(**params)

def upgrade():
    global params
    api.upgrade(**params)
    

if __name__ == '__main__':
    main(**params)
