from subprocess import PIPE, Popen
import re


class IperfCommandBase(object):
    def __init__(self, mode):
        self.command = 'iperf3'
        self.mode = mode


    def build_command(self):
        return self.command


    def parse(self, string):
        parametres = ['Interval', 'Transfer', 'Bandwidth']
        template = (r'(?P<first>\S+-\s*\S+ \w+)\s*'
                         r'(?P<second>\S+ \w+)\s*'
                         r'(?P<third>\S+ \w+/\w+)')
        output_dict = {}
        data = re.compile(template)
        matched_data = re.findall(data, string)
        j = 1
        for single_match in matched_data:
            i = 0
            dict_to_insert = dict()
            for name in self.column_names:
                dict_to_insert[name] = single_match[i]
                i += 1
            if j < len(matched_data)-1:
                interval_key = "Interval {}: {}".format(j, single_match[0])
            else:
                interval_key = "Average value:"
            j += 1
            output_dict[interval_key] = dict_to_insert
        return output_dict


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

