from subprocess import PIPE, Popen


class IperfCommandBase(object):
    def __init__(self, mode = None):
        self._command = ['iperf3']
        self._ip = None

    @property.setter
    def set_ip(self, ip):
        self._ip = ip
        return self


    def build_command(self):
        return self._command


class IperfServerCommand(IperfCommandBase):
    def __init__(self, mode=None):
        return super().__init__(mode=['-s'])

    
    def build_command(self):
        return self._command.append(self.mode)


class IperfClientCommand(IperfCommandBase):
    def __init__(self, mode=None):
        return super().__init__(mode=['-c'])

    
    def build_command(self):
        return self._command.append(self.mode, self.ip)

