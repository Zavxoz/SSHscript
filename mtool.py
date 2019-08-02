import argparse
import re
import sys


def parse_args():
    parser = argparse.ArgumentParser(description = "Tool for measuring bandwidth\
                between two hosts in the network")
    subparsers = parser.add_subparsers(dest='command')
    client_parser = subparsers.add_parser('client')
    client_parser.add_argument('-u', action='store', dest='username_client', 
                                                help='username on host')
    client_parser.add_argument('-p', action='store', dest='passwd_client',
                                                help='password for sign in')
    client_parser.add_argument('-a', action='store', dest='client_addr',
                                            help='ip address or hostname of the client')
    server_parser = subparsers.add_parser('server')
    server_parser.add_argument('-u', action='store', dest='username_server', 
                                                help='username on host')
    server_parser.add_argument('-p', action='store', dest='passwd_server',
                                                help='password for sign in')
    server_parser.add_argument('-a', action='store', dest='server_addr',
                                            help='ip address or hostname of the server')
    args_for_client = client_parser.parse_args(sys.argv[2:8])
    args_for_server = server_parser.parse_args(sys.argv[9:16])
    return args_for_client, args_for_server


def main():
    if sys.argv[1]!='client':
        raise Exception('You did not specify data for the client')
    if sys.argv[8]!='server':
        raise Exception('You did not specify data for the server')
    else:
        args_for_client, agrs_for_server = parse_args()
        

    
    

if __name__ == "__main__":
    main()