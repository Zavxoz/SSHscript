from subprocess import PIPE, Popen


class SshpassCommandExecutor(BaseCommandExecutor):
    def execute(self):
        data = Popen(self.command_to_execute, stdout=PIPE, stderr=PIPE)
        output_data, error = data.communicate()
        return_code = data.returncode
        parsed_output = self.BaseParser(output_data).parse()
        if return_code == 0:
            return parsed_output, str(error), return_code
        else:
            return None, str(error), return_code