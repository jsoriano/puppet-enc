import sys

from puppetenc import models
from puppetenc.config import Session

def dump_yaml(host_name):
    host = Session().query(models.Host).filter_by(name=host_name).first()
    if not host:
        # XXX: get default
        pass
    return "classes:\n" + "\n".join(("  %s:" % puppetClass.name for puppetClass in host.classes))

if __name__ == '__main__':
    print dump_yaml(sys.argv[1])
