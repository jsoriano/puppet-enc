# Copyright (c) 2011 Tuenti Technologies
# See LICENSE for details

import os
import sys
import errno

if 'PUPPET_ENC_SETTINGS' in os.environ:
    settings = __import__(os.environ['PUPPET_ENC_SETTINGS'])
else:
    import puppetenc.default_settings as settings

from puppetenc import models
from puppetenc.migrations import manage

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import migrate.versioning
import sqlalchemy.exceptions

engine = create_engine(settings.db_url)
Session = sessionmaker(engine)

models.Base.metadata.bind = engine
models.Base.metadata.create_all()

try:
    manage.version_control()
except migrate.versioning.exceptions.DatabaseAlreadyControlledError:
    pass
except sqlalchemy.exceptions.OperationalError:
    print >> sys.stderr, "You are not allowed to use current database"
    sys.exit(errno.EACCES)
manage.upgrade()
