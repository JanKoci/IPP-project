#!/usr/bin/env python3
import xml.etree.ElementTree as ElementTree
import Argument
from MyExceptions import *

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
            self.__arguments.append(Argument.Argument(arg))
