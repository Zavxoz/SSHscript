from subprocess import PIPE, Popen
import os.path as path


class Sshpass(object):
    def __init__(self, password, server, user, host, subcommand = None):
        self.password = password
        self.server = server
        self.user = user
        self.host = host
        self.subcommand = subcommand
        self.key = None

        
    @property
    def get_subcommand(self):
        return self.subcommand

    
    @property.setter
    def set_subcommand(self, sub):
        self.subcommand = sub
        return self

    
    @property
    def get_password(self):
        return self.password


    @property.setter
    def set_password(self, passwd):
        self.password = passwd
        return self
    

class SshSubcommand(Sshpass):
    def __init__(self, command):
        super(SshSubcommand, self).__init__(subcommand = 'ssh')
        self.command = command


    def execute(self):
        if path.isfile(self.password):
            self.key = '-p'
        else:
            self.key = '-f'
        with Popen(['sshpass', self.key, self.password, self.subcommand,
                        self.server, self.command], stdout=PIPE, stderr=PIPE) as proc:
            stdout, stderr = proc.communicate()
            return_code = proc.returncode
            if stdout:
                return stdout, stderr, return_code, 0
            else:
                return stdout, stderr, return_code, 1


class ScpSubcommand(Sshpass):
    def __init__(self, local_path):
        super(ScpSubcommand, self).__init__(subcommand = 'scp')
        self.local_path = local_path