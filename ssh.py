from subprocess import PIPE, Popen
import os.path as path


class Sshpass(object):
    def __init__(self, subcommand, password, server):
        self.subcommand = subcommand
        self.password = password
        self.server = server
    
    def __call__(self):
        if path.isfile(self.password):
            return self.pass_from_file(self.password, self.subcommand, self.server)
        else:
            return self.pass_from_cmd(self.password, self.subcommand, self.server)

    @staticmethod
    def pass_from_file(password, subcommand, server):
        with Popen(['sshpass', '-f', password, subcommand, server], 
                        stdout=PIPE, stderr=PIPE) as proc:
            stdout, stderr = proc.communicate()
        return stdout, stderr

    @staticmethod
    def pass_from_cmd(password, subcommand, server):
        with Popen(['sshpass', '-p', password, subcommand, server], 
                        stdout=PIPE, stderr=PIPE) as proc:
            stdout, stderr = proc.communicate()
        return stdout, stderr