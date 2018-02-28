#!/usr/bin/env python3

import program
import xmlParser
import argparse
import sys

# class ArgumentParseError(Exception):
#
# class ArgumenttParser(argparse.ArgumentParser):
#     def error(self, message):
#         raise ArgumentParseError


parser = argparse.ArgumentParser()
parser.add_argument("--source", type=str, metavar="filename", help="the source file with IPPcode18 program")
parser.add_argument("--stats", type=str, metavar="filename", help="generate interpret"
                    " statistics and write them to file")
parser.add_argument("--insts", action='store_true', help="count the number "
                            "of instructions in program, can be used only "
                            "with argument --stats")
parser.add_argument("--vars", action='store_true', help="count number of all "
                            "created variables in program, can be used only "
                            "with argument --stats")
try:
    args = parser.parse_args()
except SystemExit:
    exit(10)

if (not args.stats):
    if (args.insts or args.vars):
        print("ERROR: Arguments --vars and --insts can be"
                            " used only with argument --stats")
        exit(10)
print(args)

if (args.stats is None):
    print("No Stats!")
