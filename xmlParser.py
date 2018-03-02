#!/usr/bin/env python3


class XmlParserException(Exception):
    """docstring for XmlParserException."""
    pass
    # def __init__(self, arg):
    #     super(XmlParserException, self).__init__()
    #     self.arg = arg


class XmlParser(object):
    """docstring for XmlParser."""
    def __init__(self, handle):
        self.__handle = handle

    def parse_header(self):
        # parse header
        raise XmlParserException

    def parse_instruction(self):
        # parse instruction
        # return list [instruction-type, arg1, arg2, ...]
        raise XmlParserException
