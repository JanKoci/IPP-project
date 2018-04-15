#!/usr/bin/env python3
import xml.etree.ElementTree as ElementTree
import re
from MyExceptions import *

var_regex = r'^(GF|LF|TF)@[a-zA-Z_\-\&%\*\$]+[a-zA-Z0-9_\-\&%\*\$]*$'
int_regex = r'^[+-]?[0-9]+$'
bool_regex = r'^(true|false)$'
string_regex = r'^[^\s#]*$'

label_regex = r'^[a-zA-Z_\-\&%\*\$]+[a-zA-Z0-9_\-\&%\*\$]*$'
type_regex = r'^(int|string|bool)$'

class Argument(object):
    """docstring for Argument."""
    def __init__(self, argument):
        if (type(argument) is not ElementTree.Element):
            raise XmlParserException("NOT TREE ELEMENT") # NEW EXCEPTION !
        self.__create_arg(argument)
        self.__data_type = None

    @property
    def data_type(self):
        return self.__data_type

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    def __str__(self):
        return "{0}:{1}".format(self.type, self.value)

    def __repr__(self):
        return str(self)

    def __create_arg(self, argument):
        if ('type' not in argument.attrib):
            raise InstructException("Argument missing 'type' attribute")
        self.__type = argument.get('type')
        arg_value = argument.text
        err_message = "Incorrect format of type '{0}': {1}".format(self.type, arg_value)

        if (arg_value is None):
            if (self.type == 'string'):
                arg_value = ""
            else:
                raise InstructException(err_message)

        elif (self.type == 'var'):
            if (not re.match(var_regex, arg_value)):
                raise InstructException(err_message)

        elif (self.type == 'int'):
            if (not re.match(int_regex, arg_value)):
                raise InstructException(err_message)

        elif (self.type == 'string'):
            if (not re.match(string_regex, arg_value)):
                raise InstructException(err_message)

        elif (self.type == 'bool'):
            if (not re.match(bool_regex, arg_value)):
                raise InstructException(err_message)

        elif (self.type == 'label'):
            if (not re.match(label_regex, arg_value)):
                raise InstructException(err_message)

        elif (self.type == 'type'):
            if (not re.match(type_regex, arg_value)):
                raise InstructException(err_message)
        else:
            raise InstructException(err_message)
        self.__value = arg_value
