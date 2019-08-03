from subprocess import PIPE, Popen


class IperfCommandBase(object):
    def __init__(self, mode):
        self.command = 'iperf3'
        self.mode = mode


    def build_command(self):
        return self.command


class IperfServerCommand(IperfCommandBase):
    def __init__(self):
        return super(IperfServerCommand, self).__init__(mode='-s')
        

    def build_command(self):
        cmd = f'{self.command} {self.mode}'
        return cmd


class IperfClientCommand(IperfCommandBase):
    def __init__(self, mode=None):
        return super(IperfClientCommand, self).__init__(mode='-c')
        self._ip = None


    @property
    def ip(self):
        return self._ip

    
    @ip.setter
    def ip(self, value):
        self._ip = value

    
    def build_command(self):
        return f'{self.command} {self. mode} {self.ip}'

