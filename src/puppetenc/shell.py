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
        Lists existing groups
        """
        groups = self.session.query(models.Group).all()
        for group in groups:
            print group.name

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

    def do_add_host(self, line):
        """
        Adds a host to a group
        add_host <host> <group>
        """
        host_name, group_name = line
        host = self.session.query(models.Host).filter_by(name=host_name).first()
        group = self.session.query(models.Group).filter_by(name=group_name).first()
        if not group:
            print "Group '%s' doesn't exist" % group_name
            return
        if not host:
            host = models.Host(name=host_name)
            self.session.add(host)
        host.groups.append(group)
        print host.groups

class PuppetEncOneCmd(PuppetEncShell):
    def onecmd(self, line):
        self.session = Session()
        ret = None
        try:
            ret = Cmd.onecmd(self, line)
            self.session.commit()
        except Exception, e:
            print e
        finally:
            self.session.close()
        return ret

if __name__ == '__main__':
    import sys
    shell = PuppetEncShell()
    if len(sys.argv) > 1:
        PuppetEncOneCmd().onecmd(' '.join(sys.argv[1:]))
    else:
        PuppetEncShell().cmdloop()
