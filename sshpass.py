from subprocess import PIPE, Popen
import os.path as path


class Sshpass(object):
    def __init__(self, subcommand=None):
        self._password = None
        self._server = None
        self._user = None
        self.subcommand = subcommand
        self.key = None

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, passwd):
        self._password = "'" + passwd + "'"

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server):
        self._server = server

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user


class SshSubcommand(Sshpass):
    def __init__(self, command):
        super().__init__(subcommand='ssh')
        self._command = command

    def new_command(self, new_command):
        self._command = new_command

    def execute(self):
        if path.isfile(self.password):
            self.key = '-f'
        else:
            self.key = '-p'
        fullname = self.user + '@' + self.server
        proc = Popen(['sshpass', self.key, self.password, self.subcommand,
                    fullname, self._command], stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()
        return_code = proc.returncode
        if stdout:
            return stdout, stderr, return_code
        else:
            return stdout, stderr, return_code


class ScpSubcommand(Sshpass):
    def __init__(self, local_path):
        super(ScpSubcommand, self).__init__(subcommand='scp')
        self.local_path = local_path
