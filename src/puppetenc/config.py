import os

if 'PUPPET_ENC_SETTINGS' in os.environ:
    settings = __import__(os.environ['PUPPET_ENC_SETTINGS'])
else:
    import puppetenc.default_settings as settings

from puppetenc import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.db_url)
Session = sessionmaker(engine)

models.Base.metadata.bind = engine
models.Base.metadata.create_all()
# TODO: check/run migrations
