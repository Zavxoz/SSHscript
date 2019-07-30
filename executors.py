from subprocess import PIPE, Popen
from iperf_parser import IperfParser, BaseParser


class BaseCommandExcutor(object):
    def __init__(self, command, parser=BaseParser):
        self.command = command
        self.parser = parser


class SshpassCommandExecutor(BaseCommandExecutor):
    def __init__(self, command):
        return super(SshpassCommandExecutor,self).__init__(command)


    def execute(self):
        data = Popen(self.command_to_execute, stdout=PIPE, stderr=PIPE)
        output_data, error = data.communicate()
        return_code = data.returncode
        parsed_output = self.parser(output_data).parse()
        if return_code == 0:
            return parsed_output, str(error), return_code
        else:
            return None, str(error), return_code


class IperfCommandExecutor(BaseCommandExecutor):
    def __init__(self, command):
        return super(IperfCommandExecutor, self).__init__(command, parser=IperfParser)


    def execute(self):
        data = Popen(self.command_to_execute, stdout=PIPE, stderr=PIPE)
        output_data, error = data.communicate()
        return_code = data.returncode
        if output_data:
            return_code_of_execution = int(output_data.split()[-1])
        else:
            return_code_of_execution = 0
        parsed_output = self.parser(output_data).parse()
        if return_code == 0:
            return parsed_output, str(error), return_code, return_code_of_execution
        else:
            return None, str(error), return_code, return_code_of_execution#############need to finish