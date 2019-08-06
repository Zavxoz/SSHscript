import argparse
import re
import sys
from iperf_command import IperfClientCommand, IperfServerCommand
from sshpass import SshSubcommand
import json


def validation(args):
    try:
        if args[1] != 'client':
            raise Exception('Wrong format of arguments, expect word "client" before '
                            'arguments for client')
        if args[8] != 'server':
            raise Exception('Wrong format of arguments, expect word "server" before '
                            'arguments for server')
        example_of_host = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$|^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)+([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$'
        example_of_username = '^[a-z_][a-z0-9_-]{1,15}$'
        rg_addr = re.compile(example_of_host, re.IGNORECASE | re.DOTALL)
        r1 = rg_addr.search(args[7])
        r2 = rg_addr.search(args[14])
        if not r1:
            raise Exception('Wrong ip addres or hostname of client')
        if not r2:
            raise Exception('Wrong ip addres or hostname of server')
        rg_user = re.compile(example_of_username, re.IGNORECASE | re.DOTALL)
        r1 = rg_user.search(args[3])
        r2 = rg_user.search(args[10])
        if not r1:
            raise Exception(
                'Invalid username of client, check spelling of username')
        if not r2:
            raise Exception(
                'Invalid username of server, check spelling of username')
    except Exception as ex:
        print(ex)
        return 1


def parse_args():
    parser = argparse.ArgumentParser(description="Tool for measuring bandwidth\
                between two hosts in the network")
    subparsers = parser.add_subparsers(dest='command')
    client_parser = subparsers.add_parser('client')
    client_parser.add_argument('-u', action='store', dest='username_client',
                               help='username on host')
    client_parser.add_argument('-p', action='store', dest='passwd_client',
                               help='password for sign in')
    client_parser.add_argument('-a', action='store', dest='addr_client',
                                            help='ip address or hostname of the client')
    server_parser = subparsers.add_parser('server')
    server_parser.add_argument('-u', action='store', dest='username_server',
                               help='username on host')
    server_parser.add_argument('-p', action='store', dest='passwd_server',
                               help='password for sign in')
    server_parser.add_argument('-a', action='store', dest='addr_server',
                                            help='ip address or hostname of the server')
    args_for_client = client_parser.parse_args(sys.argv[2:8])
    args_for_server = server_parser.parse_args(sys.argv[9:16])
    return args_for_client, args_for_server


def initialization(init_object, args):
    init_object.user, init_object.password, init_object.server = vars(
        args).values()
    return init_object


def result(parsed_dict, error, exit_code):
    data_as_dict = {
        'error': str(error),
        'result': parsed_dict,
        'status': exit_code
    }
    json_data = json.dumps(data_as_dict, sort_keys=True,
                           indent=4, separators=(',', ': '))

    return json_data


def kill_iperf():
    try:
        client_args, server_args = parse_args()
        initialization(
                SshSubcommand('"pkill -9 iperf3 echo $?"'),
                server_args).execute()
    except Exception("Can't kill iperf process on the server"):
        sys.exit()


def main():
    try:
        validation(sys.argv)
        args_for_client, args_for_server = parse_args()
        iperf_client = IperfClientCommand()
        iperf_client.ip = args_for_server.addr_server
        command_to_client = iperf_client.build_command()
        command_to_server = IperfServerCommand().build_command()
        server = initialization(
            SshSubcommand(command_to_server),
            args_for_server)
        server.execute()
        client = initialization(
            SshSubcommand(command_to_client),
            args_for_client)
        output, error, exit_code = client.execute()
        output_dict = iperf_client.parse(output)
        result = result(output_dict, error, exit_code)
        with open('result.json', 'w') as f:
            f.write(result)
    except Exception as ex:
        print(ex)
        with open('result.json', 'w') as f:
            f.write(result(None, ex, exit_code))
    finally:
        kill_iperf()


if __name__ == "__main__":
    main()
