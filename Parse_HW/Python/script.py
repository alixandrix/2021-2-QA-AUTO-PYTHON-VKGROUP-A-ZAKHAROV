from txt_out import *
import argparse
from json_out import *


def parser_adoption():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action='store_true')
    return parser


if __name__ == '__main__':
    args = parser_adoption().parse_args().json
    if args==True:
        json_output('access.log', 'answer.json')
    else:
        txt_output('access.log', 'answer.txt')