import shlex

from cmd import Cmd

from puppetenc import models
from puppetenc.config import Session

class PuppetEncShell(Cmd):
    intro = 'Manage External Node Classification Database for Puppet'
    prompt = '> '

    def __init__(self, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        self.session = Session()

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

    def do_EOF(self, line):
        "Press Ctrl+D to quit"
        print   
        return True

    def do_list_groups(self, line):
        "Lists existing groups"
        groups = self.session.query(models.Group).all()
        for group in groups:
            print group.name

    def do_add_group(self, line):
        "Creates a new group"
        group_name = line[0]
        group = models.Group(name=group_name)
        self.session.add(group)

if __name__ == '__main__':
    import sys
    shell = PuppetEncShell()
    if len(sys.argv) > 1:
        shell.onecmd(' '.join(sys.argv[1:]))
    else:
        shell.cmdloop()
