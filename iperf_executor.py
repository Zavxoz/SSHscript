from iperf_parser import IperfParser
from subprocess import PIPE, Popen


class IperfCommandExecutor(BaseCommandExecutor):
    def execute(self):
        data = Popen(self.command_to_execute, stdout=PIPE, stderr=PIPE)
        output_data, error = data.communicate()
        return_code = data.returncode
        if output_data:
            return_code_of_execution = int(output_data.split()[-1])
        else:
            return_code_of_execution = 0
        parsed_output = IperfParser(output_data).parse()
        if return_code == 0:
            return parsed_output, str(error), return_code, return_code_of_execution
        else:
            return None, str(error), return_code, return_code_of_execution#############need to finish