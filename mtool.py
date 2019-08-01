import argparse
import re


def main():
    parser = argparse.ArgumentParser(description = "Tool for measuring bandwidth\
                between two hosts in the network")
    parser.add_argument('-c', action='store', dest='client_addr', nargs=3)
    parser.add_argument('-s', action='store', dest='server_addr', nargs=3)
    args = parser.parse_args()
    


if __name__ == "__main__":
    main()