#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ElementTree
import re

TYPES = ["MOVE",
         "CREATEFRAME",
         "PUSHFRAME",
         "POPFRAME",
         "DEFVAR",
         "CALL",
         "RETURN",
         "PUSHS",
         "POPS",
         "ADD",
         "SUB",
         "MUL",
         "IDIV",
         "LT",
         "GT",
         "EQ",
         "AND",
         "OR",
         "NOT",
         "INT2CHAR",
         "STRI2INT",
         "READ",
         "WRITE",
         "CONCAT",
         "STRLEN",
         "GETCHAR",
         "SETCHAR",
         "TYPE",
         "LABEL",
         "JUMP",
         "JUMPIFEQ",
         "JUMPIFNEQ",
         "DPRINT",
         "BREAK",
         "CLEARS",
         "ADDS",
         "SUBS",
         "MULS",
         "IDIVS",
         "LTS",
         "GTS",
         "EQS",
         "ANDS",
         "ORS",
         "NOTS",
         "INT2CHARS",
         "STRI2INTS",
         "JUMPIFEQS",
         "JUMPIFNEQS"]


var_regex = r'^(GF|LF|TF)@[a-zA-Z_\-\&%\*\$]+[a-zA-Z0-9_\-\&%\*\$]*$'
int_regex = r'^[+-]?[0-9]+$'
bool_regex = r'^(true|false)$'
string_regex = r'^[^\s#]*$'
float_regex = r'^[+-]?0x[01]\.[0-9a-fA-F]+p[+-][0-9]+$' # IS IT OK ????
label_regex = r'^[a-zA-Z_\-\&%\*\$]+[a-zA-Z0-9_\-\&%\*\$]*$'
type_regex = r'^(int|string|bool|float)$'
symb_regex = [var_regex, int_regex, bool_regex, string_regex, float_regex]

class Argument(object):
    """docstring for Argument."""
    def __init__(self, argument):
        if (type(argument) is not ElementTree.Element):
            raise XmlParserException("NOT TREE ELEMENT") # NEW EXCEPTION !
        self.__create_arg(argument)

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
        symb = ["var", "int", "float", "string", "bool"]
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

        elif (self.type in symb):
            if (not any([re.match(regex, arg_value) for regex in symb_regex])):
                raise InstructException(err_message)

        elif (self.type == 'label'):
            if (not re.match(label_regex, arg_value)):
                raise InstructException(err_message)

        elif (self.type == 'type'):
            if (not re.match(type_regex, arg_value)):
                raise InstructException(err_message)
        self.__value = arg_value



class Instruction(object):
    """docstring for Instruction."""
    def __init__(self, instruction):
        if (type(instruction) is not ElementTree.Element):
            raise XmlParserException("NOT TREE ELEMENT")
        self.__type = ""
        self.__arguments = list()
        self.__create_instruction(instruction)

    @property
    def type(self):
        return self.__type

    @property
    def arguments(self):
        return self.__arguments

    def __str__(self):
        return "{0} {1}".format(self.type, self.arguments)

    def __create_instruction(self, instruction):
        if ('opcode' not in instruction.attrib):
            raise XmlParserException("Missing 'opcode' attribute")
        inst_type = instruction.get('opcode')
        if (inst_type not in TYPES):
            raise InstructException("Unknown opcode '{0}'".format(inst_type))
        # deal with this in Instruction class ?
        for arg in instruction:
            if ('type' not in arg.attrib):
                raise XmlParserException("Argument tag missing 'type' attribute")
        self.__type = inst_type
        self.__parse_args(instruction)

    def __parse_args(self, instruction):
        symb = ["var", "int", "float", "string", "bool"]
        opcode = instruction.get('opcode')
        order = instruction.get('order')
        err_message = "Instruction order = '{0}' ".format(order)
        args_count = len(instruction)

        # <var> <symb>
        if (opcode in ["MOVE", "INT2CHAR", "STRLEN", "TYPE"]):
            err_message += "\nInstruction '{0}' expects arguments <var> <symb>".format(opcode)
            if (args_count != 2):
                raise InstructException(err_message)
            if (instruction[0].get('type') != 'var'):
                raise InstructException(err_message)
            if (instruction[1].get('type') not in symb):
                raise InstructException(err_message)

        # no arguments
        elif (opcode in ["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"]):
            err_message += "\nInstruction '{0}' expects no arguments".format(opcode)
            if (args_count != 0):
                raise InstructException(err_message)
        # <var>
        elif (opcode in ["DEFVAR", "POPS"]):
            err_message += "\nInstruction '{0}' expects argument <var>".format(opcode)
            if (args_count != 1):
                raise InstructException(err_message)
            if (instruction[0].get('type') != 'var'):
                raise InstructException(err_message)
        # <label>
        elif (opcode in ["CALL", "LABEL", "JUMP"]):
            err_message += "\nInstruction '{0}' expects argument <label>".format(opcode)
            if (args_count != 1):
                raise InstructException(err_message)
            if (instruction[0].get('type') != 'label'):
                raise InstructException(err_message)
        # <symb>
        elif (opcode in ["PUSHS", "WRITE", "DPRINT"]):
            err_message += "\nInstruction '{0}' expects argument <symb>".format(opcode)
            if (args_count != 1):
                raise InstructException(err_message)
            if (instruction[0].get('type') not in symb):
                raise InstructException(err_message)
        # <var> <symb1> <symb2>
        elif (opcode in ["ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ",
            "AND", "OR", "NOT", "STRI2INT", "CONCAT", "GETCHAR", "SETCHAR"]):
            err_message += ("\nInstruction '{0}' expects arguments "
                            "<var> <symb1> <symb2>".format(opcode))
            if (args_count != 3):
                raise InstructException(err_message)
            if (instruction[0].get('type') != 'var'):
                raise InstructException(err_message)
            if (instruction[1].get('type') not in symb):
                raise InstructException(err_message)
            if (instruction[2].get('type') not in symb):
                raise InstructException(err_message)
        # <var> <type>
        elif (opcode == "READ"):
            err_message += ("\nInstruction '{0}' expects arguments "
                            "<var> <type>".format(opcode))
            if (args_count != 2):
                raise InstructException(err_message)
            if (instruction[0].get('type') != 'var'):
                raise InstructException(err_message)
            if (instruction[1].get('type') != 'type'):
                raise InstructException(err_message)
        # <label> <symb1> <symb2>
        elif (opcode in ["JUMPIFEQ", "JUMPIFNEQ"]):
            err_message += ("\nInstruction '{0}' expects arguments "
                            "<label> <symb1> <symb2>".format(opcode))
            if (args_count != 3):
                raise InstructException(err_message)
            if (instruction[0].get('type') != 'label'):
                raise InstructException(err_message)
            if (instruction[1].get('type') not in symb):
                raise InstructException(err_message)
            if (instruction[2].get('type') not in symb):
                raise InstructException(err_message)
        else:
            err_message += "\nUnknown instruction '{0}'".format(opcode)
            raise InstructException(err_message)

        for arg in instruction:
            self.__arguments.append(Argument(arg))



class InterpretException(Exception):
    """docstring for InterpretException."""
    def __init__(self, message):
        print("ERROR: " + message, file=sys.stderr)

class InstructException(InterpretException):
    """docstring for InstructException."""
    def __init__(self, message="", exit_code=32):
        self.exit_code = exit_code
        self.message = "InstructException: " + message
        super().__init__(self.message)


class XmlParserException(InterpretException):
    """docstring for XmlParserException."""
    def __init__(self, message="", exit_code=31):
        self.exit_code = exit_code
        self.message = "XmlParserException: " + message
        super().__init__(self.message)


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

            new_instruction = Instruction(child)
            self.__instructions.append(new_instruction)

    def parse(self):
        # return list here ?
        self.__parse_header()
        self.__parse_instructions()
        return self.instructions


try:
    parser = XmlParser(file_handle='a.xml')
    code = parser.parse()
except InterpretException as e:
    exit(e.exit_code)

for instruction in code:
    print(instruction)
