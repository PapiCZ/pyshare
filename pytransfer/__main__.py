import argparse
import sys
from collections import deque

from pytransfer.utils import upload_file

files_queue = deque()


def get_args(args):
    arg = argparse.ArgumentParser(description="App that simplifies usage of https://transfer.sh")
    arg.add_argument(
        'filename',
        nargs='*',
        default=(),
        help='Name of file you want to upload'
    )

    return arg.parse_args(args)


def process_queue():
    while True:
        try:
            print(upload_file(files_queue.popleft()))
        except IndexError:
            break


def main():
    """
    Main entrypoint
    """
    args = get_args(sys.argv[1:])

    for filename in args.filename:
        files_queue.append(filename)

    process_queue()


if __name__ == '__main__':
    main()
