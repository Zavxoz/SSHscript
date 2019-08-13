#! /usr/bin/python
"""Unit tests input data and expected results"""

import argparse
from collections import OrderedDict


IPERF_MODE = True
COMMAND = ['command']
IPERF_PORT = '22'
SERVER_IP = '192.168.1.1'
SERVER_HOST = 'server'
OK_MESSAGE = ''
ERROR_MESSAGE = 'Error!'
ERROR_MESSAGE_HOST1 = "connect failed: No route to host\n"
ERROR_MESSAGE_HOST2 = "connect failed: Connection refused\n"
OK_RETURN_CODE = 0
ERROR_RETURN_CODE = 1
SERVER_USER = 'root'
SERVER_PASSWORD = 'QWERTY'
PASSWORD_FILE = 'file.txt'
OUTPUT_RESULT = """
Connecting to host 192.168.43.211, port 5201
[  5] local 192.168.43.211 port 44068 connected to 192.168.43.211 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  5.81 GBytes  49.9 Gbits/sec    0   1.12 MBytes       
[  5]   1.00-2.00   sec  5.83 GBytes  50.0 Gbits/sec    0   1.19 MBytes       
[  5]   2.00-3.00   sec  5.53 GBytes  47.5 Gbits/sec    0   1.44 MBytes       
[  5]   3.00-4.00   sec  4.63 GBytes  39.7 Gbits/sec    0   1.44 MBytes       
[  5]   4.00-5.00   sec  4.69 GBytes  40.3 Gbits/sec    0   1.44 MBytes       
[  5]   5.00-6.00   sec  3.95 GBytes  33.9 Gbits/sec    1   1.44 MBytes       
[  5]   6.00-7.00   sec  4.61 GBytes  39.6 Gbits/sec    0   1.44 MBytes       
[  5]   7.00-8.00   sec  4.68 GBytes  40.2 Gbits/sec    0   1.44 MBytes       
[  5]   8.00-9.00   sec  3.68 GBytes  31.6 Gbits/sec    0   1.44 MBytes       
[  5]   9.00-10.00  sec  3.51 GBytes  30.2 Gbits/sec    0   1.44 MBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  46.9 GBytes  40.3 Gbits/sec    1             sender
[  5]   0.00-10.04  sec  46.9 GBytes  40.1 Gbits/sec                  receiver

"""
EXPECTED_IP = {'client ip': '192.168.2.2', 'server ip': '192.168.1.1'}
IPERF_PARSER_EXPECTED_RESULT = OrderedDict([('Total result:',
                                           {'Transfer': '2.57 GBytes',
                                            'Bandwidth': '2.21 Gbits/sec',
                                            'Interval': '0.0-10.0 sec'})])

EXPECTED_OUTPUT_BUILDER_RESULT = """{
    "error": "",
    "result": {
        "Total result:": {
            "Bandwidth": "2.21 Gbits/sec",
            "Interval": "0.0-10.0 sec",
            "Transfer": "2.57 GBytes"
        }
    },
    "status": 0
}"""
EXPECTED_OUTPUT_BUILDER_ERROR = """{
    "error": "Error!",
    "result": null,
    "status": 1
}"""
EXECUTE_EXPECTED_RESULT =\
    ("\nClient connecting to 192.168.1.1, TCP port 5001\n"
     "TCP window size: 85.0 KByte (default)\n"
     "------------------------------------------------------------\n"
     "[  3] local 192.168.2.2 port 42780 connected with 192.168.1.1 port 5001"
     "\n"
     "[ ID] Interval       Transfer     Bandwidth\n"
     "[  3]  0.0-10.0 sec  2.57 GBytes  2.21 Gbits/sec\n"
     "0\n")

ARGS_INPUT = argparse.Namespace(
            client_host=None, client_ip='192.168.56.101',
            client_password='222222', client_username='root',
            file_client_password=None, file_server_password=None,
            interval=None, port=None, server_host=None,
            server_ip='192.168.56.100', server_password='111111',
            server_username='root', time=None, udp=False)

CONNECTION1 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                OK_MESSAGE,
                                                 OK_RETURN_CODE,
                                                 OK_RETURN_CODE)
CONNECTION2 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                                 OK_MESSAGE,
                                                 ERROR_RETURN_CODE,
                                                 OK_RETURN_CODE)
CONNECTION3 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                                 OK_MESSAGE,
                                                 OK_RETURN_CODE,
                                                 ERROR_RETURN_CODE)
CONNECTION4 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                                 ERROR_MESSAGE,
                                                 OK_RETURN_CODE,
                                                 OK_RETURN_CODE)
CONNECTION5 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                                 ERROR_MESSAGE_HOST2,
                                                 OK_RETURN_CODE,
                                                 OK_RETURN_CODE)
CONNECTION6 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                                 ERROR_MESSAGE_HOST2,
                                                 OK_RETURN_CODE,
                                                 OK_RETURN_CODE)
CONNECTION_KILL = ResultBuilderWithExecutionExitCode(OK_RETURN_CODE,
                                                     OK_MESSAGE,
                                                     OK_RETURN_CODE,
                                                     OK_MESSAGE)