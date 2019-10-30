"""Unit tests"""

import unittest
from mock import Mock, patch
from iperf_command import IperfClientCommand, IperfServerCommand, IperfCommandBase
from sshpass import Sshpass, SshSubcommand
from check_errors import MyError
from test_data import *
from mtool import make_result, kill_iperf


class TestIperfCommandBase(unittest.TestCase):
    """unit tests for BaseIperfCommandBuilder class"""
        
    def test_string_to_dict(self):
        """testing of correct transformation of string to dict"""
        actual_result = IperfCommandBase().parse(OUTPUT_RESULT)
        self.assertEqual(actual_result, IPERF_PARSER_EXPECTED_RESULT)


class TestIperfServerCommandBuilder(unittest.TestCase):
    """unit tests for IperfServerCommandBuilder class"""

    def test_build_command(self):
        """testing of 'iperf -s' command building"""
        actual_result = IperfServerCommand().build_server_command()
        self.assertListEqual(actual_result, ['iperf', '-s'])


class TestIperfClientCommandBuilder(unittest.TestCase):
    """unit tests for IperfClientCommandBuilder class"""

    def test_set_server_address_ip(self):
        """testing self.server)ip setter"""
        actual_result = IperfClientCommand()\
            .set_server_ip(SERVER_IP)\
            .server_ip
        self.assertEqual(actual_result, '192.168.1.1')

    def test_set_server__address_hostname(self):
        """testing self.server_hostname setter"""
        actual_result = IperfClientCommand()\
            .set_server_hostname(SERVER_HOST)\
            .server_hostname
        self.assertEqual(actual_result, 'server')

    def test_build_command_ip(self):
        """testing of 'iperf -c 192.168.1.1' command building"""
        actual_result = IperfClientCommand()\
            .set_server_ip(SERVER_IP)\
            .build_client_command()
        self.assertListEqual(actual_result, ['iperf', '-c', '192.168.1.1'])

    def test_build_command_hostname(self):
        """testing of 'iperf -c server' command building"""
        actual_result = IperfClientCommand()\
            .set_server_hostname(SERVER_HOST)\
            .build_client_command()
        self.assertListEqual(actual_result, ['iperf', '-c', 'server'])


class TestResultBuilder(unittest.TestCase):
    """unit tests for class ResultBuilder"""
    def test_to_json(self):
        """testing of correct output in json"""
        actual_result = make_result(IPERF_PARSER_EXPECTED_RESULT,
                                      OK_MESSAGE,
                                      OK_RETURN_CODE)
        self.assertMultiLineEqual(actual_result,
                                  EXPECTED_OUTPUT_BUILDER_RESULT)

    def test_to_json_with_non_result(self):
        """testing of correct output in json when there is no result,
        message about error and error returncode"""
        actual_result = make_result(None,
                                      ERROR_MESSAGE,
                                      ERROR_RETURN_CODE)
        self.assertMultiLineEqual(actual_result, EXPECTED_OUTPUT_BUILDER_ERROR)


class TestBaseCommandExecutor(unittest.TestCase):
    """unit test for class BaseCommandExecutor"""
    def test_execute(self):
        """testing of correct output of bandwidth measurements"""
        with patch('command_executor.subprocess.Popen') as mock_subproc_popen:
            communicate_mock = Mock()
            attrs = {'communicate.return_value': (OUTPUT_RESULT,
                                                  OK_MESSAGE),
                     'returncode': OK_RETURN_CODE}
            communicate_mock.configure_mock(**attrs)
            mock_subproc_popen.return_value = communicate_mock
            actual_result = BaseCommandExecutor(COMMAND).to_execute()
            self.assertIs(actual_result.error, OK_MESSAGE)
            self.assertIs(actual_result.exit_code, OK_RETURN_CODE)
            self.assertMultiLineEqual(actual_result.output,
                                      EXECUTE_EXPECTED_RESULT)


class TestClientCommandExecutor(unittest.TestCase):
    """unit test for class ClientCommandExecutor"""
    def test_execute(self):
        """testing of correct output of bandwidth measurements"""
        with patch('command_executor.subprocess.Popen') as mock_subproc_popen:
            communicate_mock = Mock()
            attrs = {'communicate.return_value': (OUTPUT_RESULT,
                                                  OK_MESSAGE),
                     'returncode': OK_RETURN_CODE}
            communicate_mock.configure_mock(**attrs)
            mock_subproc_popen.return_value = communicate_mock
            actual_result = IperfCommandExecutor(COMMAND).to_execute()
            self.assertIs(actual_result.error, OK_MESSAGE)
            self.assertIs(actual_result.exit_code, OK_RETURN_CODE)
            self.assertDictEqual(actual_result.output,
                                 IPERF_PARSER_EXPECTED_RESULT)


class TestSshpassBaseCommandBuilder(unittest.TestCase):
    """unit tests for SshpassBaseCommandBuilder class"""
    def test_set_password(self):
        """testing self.password setter"""
        actual_result = Sshpass(COMMAND) \
            .set_password(SERVER_PASSWORD).password
        self.assertEqual(actual_result, 'QWERTY')

    def test_set_password_file(self):
        """testing self.password_file setter"""
        actual_result = Sshpass(COMMAND) \
            .set_file(PASSWORD_FILE).password_file
        self.assertEqual(actual_result, 'file.txt')
    
    def test_set_ip_address(self):
        """testing self.ip_address setter"""
        actual_result = SshCommandBuilder(SERVER_USER, COMMAND)\
            .set_ip_address(SERVER_IP)\
            .ip_address
        self.assertEqual(actual_result, '192.168.1.1')

    def test_set_hostname(self):
        """testing self.hostname setter"""
        actual_result = SshCommandBuilder(SERVER_USER, COMMAND)\
            .set_hostname(SERVER_HOST)\
            .hostname
        self.assertEqual(actual_result, 'server')
    


class TestSshCommandBuilder(unittest.TestCase):
    """unit tests for SshCommandBuilder class"""
    pass


class TestConnectionToServer(unittest.TestCase):
    """unit tests for connection_to_server() function"""
    @patch('mtool.parse_command_line_args')
    @patch('mtool.IperfCommandExecutor.to_execute')
    def test_correct_connectiom(self, mock_execute, mock_parse):
        """testing of error not occurring if exit code is 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION1
        mock_execute.return_value = result
        actual_result = connection_to_server()
        self.assertIs(actual_result.error, "")
        self.assertIs(actual_result.exit_code, 0)
        self.assertIs(actual_result.exit_code_execution, 0)
        self.assertIs(actual_result.output, IPERF_PARSER_EXPECTED_RESULT)

    @patch('mtool.parse_command_line_args')
    @patch('mtool.IperfCommandExecutor.to_execute')
    def test_connection_raises_error(self, mock_execute, mock_parse):
        """testing of error occurring if exit code is not 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION2
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_server()

    @patch('mtool.parse_command_line_args')
    @patch('mtool.IperfCommandExecutor.to_execute')
    def test_connection_raises_error_execute(self, mock_execute, mock_parse):
        """testing of error occurring if execution exit code is not 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION3
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_server()

    @patch('mtool.parse_command_line_args')
    @patch('mtool.IperfCommandExecutor.to_execute')
    def test_connection_raises_message_error(self, mock_execute, mock_parse):
        """testing of error not occurring if error message is 'Error!'"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION4
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_server()


class TestConnectionToClient(unittest.TestCase):
    """unit tests for connection_to_client() function"""
    @patch('mtool.parse_command_line_args')
    @patch('mtool.IperfCommandExecutor.to_execute')
    def test_correct_connection(self, mock_execute, mock_parse):
        """testing of error not occurring if exit code is 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION1
        mock_execute.return_value = result
        actual_result = connection_to_client()
        self.assertIs(actual_result.exit_code, 0)
        self.assertIs(actual_result.error, "")
        self.assertIs(actual_result.exit_code_execution, 0)
        self.assertIs(actual_result.output, IPERF_PARSER_EXPECTED_RESULT)

    @patch('mtool.parse_command_line_args')
    @patch('mtool.IperfCommandExecutor.to_execute')
    def test_connection_raises_error(self, mock_execute, mock_parse):
        """testing of error occurring if exit code is not 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION2
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_client()

    @patch('mtool.parse_command_line_args')
    @patch('mtool.IperfCommandExecutor.to_execute')
    def test_connection_raises_error_execute(self, mock_execute, mock_parse):
        """testing of error occurring if execution exit code is not 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION3
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_client()

    @patch('mtool.parse_command_line_args')
    @patch('mtool.IperfCommandExecutor.to_execute')
    def test_connection_raises_message_error(self, mock_execute, mock_parse):
        """testing of error not occurring if error message is 'Error!'"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION4
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_client()

    @patch('mtool.parse_command_line_args')
    @patch('mtool.IperfCommandExecutor.to_execute')
    def test_connection_raises_message_error_and_no_exit(self, mock_execute,
                                                         mock_parse):
        """testing of error occurring if error message is
        'connect failed: No route to host\n'"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION5
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_client()

    @patch('mtool.parse_command_line_args')
    @patch('mtool.IperfCommandExecutor.to_execute')
    def test_connection_raises_message_error_and_no_exit2(self, mock_execute,
                                                          mock_parse):
        """testing of error occurring if error message is
        'connect failed: Connection refused\n'"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION6
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_client()
from mtool import make_result


class TestConnectionToKillIperf(unittest.TestCase):
    """unit tests for connection_to_server_to_kill_iperf() function"""
    @patch('mtool.parse_command_line_args')
    @patch('mtool.IperfCommandExecutor.to_execute')
    def test_correct_connection(self, mock_execute, mock_parse):
        """testing of error not occurring if exit code is 0"""  
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION_KILL
        mock_execute.return_value = result
        actual_result = connection_to_server_to_kill_iperf()
        self.assertIs(actual_result.exit_code, 0)
        self.assertIs(actual_result.error, '')
        self.assertIs(actual_result.exit_code_execution, '')
        self.assertIs(actual_result.output, 0)


if __name__ == '__main__':
    unittest.main()