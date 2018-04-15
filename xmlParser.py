#!/usr/bin/env python3
import xml.etree.ElementTree as ElementTree
# import Argument
from MyExceptions import *
import Instruction


class XmlParser(object):
    """docstring for XmlParser."""
    def __init__(self, file_handle):
        self.__file = file_handle
        self.__instructions = list()
        try:
            tree = ElementTree.parse(source=self.__file)
        except FileNotFoundError:
            raise XmlParserException(message="File {0} not found".format(self.__file),
                                     exit_code=11)
        except ElementTree.ParseError:
            raise XmlParserException()
        self.__root = tree.getroot()


    @property
    def instructions(self):
        return self.__instructions

    def __parse_header(self):
        # parse header
        # How to check xml version ??

        if (self.__root.tag != 'program'):
            raise XmlParserException("Missing 'program' tag")
        if ('language' not in self.__root.attrib):
            raise XmlParserException("Missing 'language' attribute in 'program' tag")
        for attr, value in self.__root.attrib.items():
            if (attr == 'language'):
                if (value != 'IPPcode18'):
                    raise XmlParserException("Unexpected value '{0}' of 'language' attribute "
                                            "'IPPcode18' expected".format(value))
            elif (attr == 'name' or attr == 'description'):
                pass
            else:
                raise XmlParserException("Unknown attribute '{0}' in 'program' tag".format(attr))

    def __parse_instructions(self):
        # parse instruction
        # return list [instruction-type, arg1, arg2, ...]
        for child in self.__root:
            if (child.tag != 'instruction'):
                raise XmlParserException("Unknown tag '{0}' where 'instruction '"
                                        "tag expected".format(child.tag))
            if ('order' not in child.attrib):
                raise XmlParserException("Missing 'order' attribute")
            if ('opcode' not in child.attrib):
                raise XmlParserException("Missing 'opcode' attribute")

            new_instruction = Instruction.Instruction(child)
            self.__instructions.append(new_instruction)

    def parse(self):
        # return list here ?
        self.__parse_header()
        self.__parse_instructions()
        return self.instructions


############## USAGE ##############
# if __name__ == "__main__":
#     try:
#         parser = XmlParser(file_handle='a.xml')
#         code = parser.parse()
#     except InterpretException as e:
#         exit(e.exit_code)
#
#         for instruction in code:
#             print(instruction)
