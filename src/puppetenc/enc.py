# Copyright (c) 2011 Tuenti Technologies
# See LICENSE for details

import sys
import re

from puppetenc import models
from puppetenc.config import Session

def get_node(node_name):
    node = Session().query(models.Node).filter_by(name=node_name).first()
    if node:
        return node
    else:
        nodes = Session().query(models.Node).all()
        for node in nodes:
            if re.match(node.name, node_name):
                return node
    if not node:
        node = Session().query(models.Node).filter_by(name='default').first()

def dump_yaml(node_name):
    node = get_node(node_name)
    modules = []
    if node:
        modules = node.modules
    else:
        default_group = Session().query(models.Group).filter_by(name='default').first()
        if default_group:
            modules = default_group.modules
    return "classes:\n" + "\n".join(("  %s:" % module.name for module in modules))

if __name__ == '__main__':
    print dump_yaml(sys.argv[1])
