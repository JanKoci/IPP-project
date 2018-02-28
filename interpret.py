#!/usr/bin/env python3

# import program
# import xmlParser
import argparse

class ArgsParseError(object):
    """docstring for ArgsParseError."""
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs ???
        super(ValidationError, self).__init__(message)


try:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="The source file with IPPcode18 program")
    parser.add_argument("--stats", help="The file to write interpreter statistics to")
    parser.add_argument("--insts", action='store_true', help="Count the number "
                                "of instructions in program")
    parser.add_argument("--vars", action='store_true', help="Count number of all "
                                "created variables in program")

    args = parser.parse_args()

    if (not args.stats):
        if (args.insts or args.vars):
            raise SystemExit
    print(args)


except SystemExit:
    exit(10)
