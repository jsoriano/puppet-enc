# Copyright (c) 2011 Tuenti Technologies
# See LICENSE for details

import shlex

from cmd import Cmd

from puppetenc import models
from puppetenc.config import Session

class PuppetEncShell(Cmd):
    intro = 'Manage External Node Classification Database for Puppet'
    prompt = '> '

    def preloop(self):
        self.session = Session()

    def postloop(self):
        self.session.commit()
        self.session.close()
        self.session = None

    def postcmd(self, stop, line):
        try:
            self.session.commit()
        except Exception, e:
            self.session.close()
            self.session = Session()
            print e
        return stop

    def emptyline(self):
        return None

    def parseline(self, line):
        cmd = shlex.split(line)
        return cmd[0], cmd[1:], line

    def do_help(self, line):
        return Cmd.do_help(self, ' '.join(line))

    def onecmd(self, line):
        try:
            ret = Cmd.onecmd(self, line)
            self.session.commit()
            return ret
        except Exception, e:
            print e
            return None

    def do_EOF(self, line):
        """
        Press Ctrl+D to quit
        """
        print   
        return True

    def do_list_groups(self, line):
        """
        Lists existing groups, and its modules
        list_node [<node>]
        """
        if line:
            group_name = line[0]
            groups = self.session.query(models.Group).filter_by(name=group_name).all()
        else:
            groups = self.session.query(models.Group).all()
        for group in groups:
            print group.name
            for module in group.modules:
                print " - %s" % module.name

    def do_add_group(self, line):
        """
        Creates a new group
        add_group <group>
        """
        group_name = line[0]
        group = models.Group(name=group_name)
        self.session.add(group)

    def do_del_group(self, line):
        """
        Deletes an existing group
        del_group <group>
        """
        group_name = line[0]
        group = self.session.query(models.Group).filter_by(name=group_name).first()
        if group:
            self.session.delete(group)
        else:
            print "Group '%s' doesn't exist" % group_name

    def do_list_nodes(self, line):
        """
        List nodes, its groups and its modules
        list_nodes [<node>]
        """
        if line:
            node_name = line[0]
            nodes = self.session.query(models.Node).filter_by(name=node_name).all()
        else:
            nodes = self.session.query(models.Node).all()

        for node in nodes:
            print node.name
            for group in node.groups:
                print " - %s" % group.name
                for module in group.modules:
                    print "  - %s" % module.name

    def do_add_node(self, line):
        """
        Adds a node to a group
        add_node <node> <group>
        """
        node_name, group_name = line
        node = self.session.query(models.Node).filter_by(name=node_name).first()
        group = self.session.query(models.Group).filter_by(name=group_name).first()
        if not group:
            print "Group '%s' doesn't exist" % group_name
            return
        if not node:
            node = models.Node(name=node_name)
            self.session.add(node)
        node.groups.append(group)

    def do_del_node(self, line):
        """
        Removes a node from a group
        del_node <node> <group>
        """
        node_name, group_name = line
        node = self.session.query(models.Node).filter_by(name=node_name).first()
        if not node:
            print "Node '%s' doesn't exist" % node_name
            return
        group = self.session.query(models.Group).filter_by(name=group_name).first()
        if not group:
            print "Group '%s' doesn't exist" % group_name
            return
        node.groups.remove(group)
        if not node.groups:
            print "Node '%s' doesn't bellows to any group, removing..." % node_name
            self.session.delete(node)                

    def do_add_module(self, line):
        """
        Adds a module to a group
        add_module <module> <group>
        """
        module_name, group_name = line
        module = self.session.query(models.Module).filter_by(name=module_name).first()
        group = self.session.query(models.Group).filter_by(name=group_name).first()
        if not group:
            print "Group '%s' doesn't exist" % group_name
            return
        if not module:
            module = models.Module(name=module_name)
            self.session.add(module)
        group.modules.append(module)

    def do_del_module(self, line):
        """
        Removes a module from a group
        del_module <module> <group>
        """
        module_name, group_name = line
        module = self.session.query(models.Module).filter_by(name=module_name).first()
        if not module:
            print "Module '%s' doesn't exist" % group_name
            return
        group = self.session.query(models.Group).filter_by(name=group_name).first()
        if not group:
            print "Group '%s' doesn't exist" % group_name
            return
        group.modules.remove(module)

class PuppetEncOneCmd(PuppetEncShell):
    def onecmd(self, line):
        self.session = Session()
        ret = None
        try:
            ret = Cmd.onecmd(self, line)
            self.session.commit()
        except Exception, e:
            print e
        self.session.close()
        return ret

if __name__ == '__main__':
    import sys
    shell = PuppetEncShell()
    if len(sys.argv) > 1:
        PuppetEncOneCmd().onecmd(' '.join(sys.argv[1:]))
    else:
        PuppetEncShell().cmdloop()
