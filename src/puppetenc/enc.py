import sys
import re

from puppetenc import models
from puppetenc.config import Session

def get_host(host_name):
    host = Session().query(models.Host).filter_by(name=host_name).first()
    if host:
        return host
    else:
        hosts = Session().query(models.Host).all()
        for host in hosts:
            if re.match(host.name, host_name):
                return host
    if not host:
        # XXX: get default
        pass

def dump_yaml(host_name):
    host = get_host(host_name)
    return "classes:\n" + "\n".join(("  %s:" % puppetClass.name for puppetClass in host.classes))

if __name__ == '__main__':
    print dump_yaml(sys.argv[1])
