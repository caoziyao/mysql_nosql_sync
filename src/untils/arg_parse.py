# coding: utf-8


import argparse
parser = argparse.ArgumentParser()

parser.add_argument(
    "-p", "--port",
    type=int,
    help="port"
)
parser.add_argument(
    "-s", "--server",
    help="master or slave"
)


class Option(object):

    def __init__(self):
        args = parser.parse_args()
        self._args = args
        self._option = vars(args)

    @property
    def args(self):
        return self._args


    def __getattr__(self, item):
        if item in self._option:
            return self._option[item]
        else:
            return None

option = Option()