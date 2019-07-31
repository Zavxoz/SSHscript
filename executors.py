from subprocess import PIPE, Popen
from iperf_parser import IperfParser, BaseParser
import json


class BaseCommandExcutor(object):
    def __init__(self, command, parser=BaseParser):
        self.command = command
        self.parser = parser


class IperfCommandExecutor(BaseCommandExecutor):
    def __init__(self, command):
        return super(IperfCommandExecutor, self).__init__(command, parser=IperfParser)


    def execute(self):
        data = Popen(self.command_to_execute, stdout=PIPE, stderr=PIPE)
        output_data, error = data.communicate()
        return_code = data.returncode
        parsed_output = self.parser(output_data).parse()
        if return_code == 0:
            return self.result(parsed_output, str(error), return_code)
        else:
            return self.result(None, str(error), return_code)


    def result(output, error, exit_code, ):
        data_as_dict = {
            'error': str(error),
            'result': output,
            'status': exit_code
        }
        json_data = json.dumps(data_as_dict, sort_keys=True,
                               indent=4, separators=(',', ': '))
        return json_data
