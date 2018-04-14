#!/usr/bin/env python3
##########################################
# Project IPP
# Author: Jan Koci
# Date:   28.2.2018
# Brief:  Implementation of class Program
##########################################

import sys
import Instruction
from MyExceptions import *


# is it needed ??? Make it just a dict
# class Frame(object):
#     """docstring for Frame."""
#     def __init__(self):
#         self.content = dict()

class Variable(object):
    """docstring for Variable."""
    def __init__(self, dtype=None, value=None):
        self.__dtype = dtype
        self.__value = value

    @property
    def dtype(self):
        return self.__dtype

    # @dtype.setter
    # def dtype(self, dtype):
    #     if (self.dtype is not None):
    #         raise RuntimeException("Cannot change type of a variable",
    #                                 exit_code=53)
    #     self.__dtype = dtype

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, variable):
        if (self.dtype is None):
            self.__dtype = variable.dtype

        if (variable.dtype != self.dtype):
            raise RuntimeException("Assigning variables of different types",
                                    exit_code=53)
        self.__value = variable.value

    def __str__(self):
        return "{0} {1}".format(self.dtype, self.value)

    def __repr__(self):
        return str(self)



class Program(object):
    def __init__(self, code):
        self.__frameStack = list()
        self.__callStack = list()
        self.__dataStack = list()
        self.__gf = dict()
        self.__labels = dict() # name and position in code
        self.__tempFrame = None
        self.__localFrame = None
        self.__instCounter = 0
        # labels could be in frames ?
        self.__code = code

    @property
    def gf(self):
        return self.__gf

    @property
    def frameStack(self):
        return self.__frameStack

    @property
    def labels(self):
        return self.__labels

    @property
    def code(self):
        return self.__code

    @property
    def localFrame(self):
        return self.__localFrame

    # @localFrame.setter
    # def localFrame(self)
    # def __setitem__(self,key,value):

    def __get_frame(self, frame_string):
        if (frame_string == "TF"):
            return self.__tempFrame
        elif (frame_string == "LF"):
            return self.__localFrame
        elif (frame_string == 'GF'):
            return self.__gf
        else:
            raise RuntimeException("Internal error", exit_code=99)

    def __check_var(self, var_frame, var_name):
        if (var_frame is None):
            raise RuntimeException("Frame is not defined", exit_code=55)
        if (var_name not in var_frame):
            raise RuntimeException("Variable {0} not defined".format(arg[0].value),
                                    exit_code=54)

    def __split_var(self, var):
        var_frame = self.__get_frame(var.split('@')[0])
        var_name = var.split('@')[1]
        return (var_frame, var_name)

    def interpret(self):
        print("Inst: {0}:\nGF = {1}\nTR = {2}\nLF = {3}\nDataStack = {4}\nCallStack = {5}\nLabels = {6}\n".format(self.__instCounter,
            self.__gf, self.__tempFrame, self.__localFrame, self.__dataStack, self.__callStack, self.__labels))
        while True:
            inst = self.code[self.__instCounter]
            try:
                method = getattr(__class__, inst.type)
            except AttributeError:
                print("ERROR: Method for instruction {} "
                "is not implemented".format(inst.type) ,file=sys.stderr)
                exit(1) #todo what to exit ???
            try:
                method(self, inst.arguments)
            except InterpretException as e:
                print ("Instruction {0}".format(self.__instCounter+1))
                raise e
            self.__instCounter += 1
            print("Inst: {0}:\nGF = {1}\nTR = {2}\nLF = {3}\nDataStack = {4}\nCallStack = {5}\nLabels = {6}\n".format(self.__instCounter,
                self.__gf, self.__tempFrame, self.__localFrame, self.__dataStack, self.__callStack, self.__labels))
            if (self.__instCounter >= len(self.code)):
                break

    def MOVE(self, args):
        # perform move instruction
        var1_frame, var1_name = self.__split_var(args[0].value)
        self.__check_var(var1_frame, var1_name)

        if (args[1].type == 'var'):
            var2_frame, var2_name = self.__split_var(args[1].value)
            self.__check_var(var2_frame, var2_name)
            var2 = var2_frame[var2_name]
        else:
            dtype = args[1].type
            value = args[1].value
            var2 = Variable(dtype=dtype, value=value)

        var1_frame[var1_name].value = var2


    def CREATEFRAME(self, no_args):
        # perform createframe instruction
        self.__tempFrame = dict()

    def PUSHFRAME(self, no_args):
        if (self.__tempFrame is None):
            raise RuntimeException("TF does not exist", exit_code=55)
        self.__frameStack.append(self.__tempFrame)
        self.__localFrame = self.__frameStack[-1]
        self.__tempFrame = None

    def POPFRAME(self, no_args):
        if (self.__localFrame is None):
            raise RuntimeException("Frame does not exit", exit_code=55)
        self.__tempFrame = self.__frameStack.pop()
        if (len(self.__frameStack) == 0):
            self.__localFrame = None
        else:
            self.__localFrame = self.__frameStack[-1]

    def DEFVAR(self, arg):
        var_frame, var_name = self.__split_var(arg[0].value)
        if (var_name in var_frame):
            raise RuntimeException("Redefinition of variable {0}".format(
                                    var_name), exit_code=52) #todo: what exit ERROR

        new_var = Variable()
        var_frame[var_name] = new_var

    def CALL(self, arg):
        label_name = arg[0].value
        if (label_name not in self.__labels):
            raise RuntimeException("Label {0} is not defined".format(label_name),
                                    exit_code=52)

        label_position = self.__labels[label_name]
        self.__callStack.append(self.__instCounter+1)
        self.__instCounter = label_position


    def LABEL(self, arg):
        label_name = arg[0].value
        if (label_name in self.__labels):
            raise RuntimeException("Redefinition of label {0}".format(label_name),
                                    exit_code=52)
        self.__labels[label_name] = self.__instCounter


    def RETURN(self, no_args):
        if (len(self.__callStack) == 0):
            raise RuntimeException("No return position found", exit_code=56)
        self.__instCounter = self.__callStack.pop()

    def PUSHS(self, arg):
        if (arg[0].type == 'var'):
            var_frame, var_name = self.__split_var(arg[0].value)
            self.__check_var(var_frame, var_name)
            var = var_frame[var_name]
        else:
            var = Variable(dtype=arg[0].type, value=arg[0].value)
        self.__dataStack.append(var)

    def POPS(self, arg):
        if (len(self.__dataStack) == 0):
            raise RuntimeException("Data stack is empty", exit_code=56)
        var_frame, var_name = self.__split_var(arg[0].value)
        self.__check_var(var_frame, var_name)
        pop_var = self.__dataStack.pop()
        var_frame[var_name].value = pop_var

    def ADD(self, args):
        var_frame, var_name = self.__split_var(args[0].value)
        self.__check_var(var_frame, var_name)

        if (args[1].type == 'var'):
            var1_frame, var1_name = self.__split_var(args[1].value)
            self.__check_var(var1_frame, var1_name)
            symb = var1_frame[var1_name]
            dtype = symb.dtype
            value = symb.value
        else:
            dtype = args[1].type
            value = args[1].value
        if (dtype != 'int'):
            raise RuntimeException("Instruction ADD expects all arguments "
                    "of type 'int'", exit_code=53)
        value1 = int(value)

        if (args[2].type == 'var'):
            var2_frame, var2_name = self.__split_var(args[2].value)
            self.__check_var(var2_frame, var2_name)
            symb = var2_frame[var2_name]
            dtype = symb.dtype
            value = symb.value
        else:
            dtype = args[2].type
            value = args[2].value
        if (dtype != 'int'):
            raise RuntimeException("Instruction ADD expects all arguments "
                    "of type 'int'", exit_code=53)
        value2 = int(value)
        add_value = value1 + value2
        var_frame[var_name].value = Variable(dtype=dtype, value=str(add_value))

    def SUB(self, args):
        var_frame, var_name = self.__split_var(args[0].value)
        self.__check_var(var_frame, var_name)

        if (args[1].type == 'var'):
            var1_frame, var1_name = self.__split_var(args[1].value)
            self.__check_var(var1_frame, var1_name)
            symb = var1_frame[var1_name]
            dtype = symb.dtype
            value = symb.value
        else:
            dtype = args[1].type
            value = args[1].value
        if (dtype != 'int'):
            raise RuntimeException("Instruction ADD expects all arguments "
                    "of type 'int'", exit_code=53)
        value1 = int(value)

        if (args[2].type == 'var'):
            var2_frame, var2_name = self.__split_var(args[2].value)
            self.__check_var(var2_frame, var2_name)
            symb = var2_frame[var2_name]
            dtype = symb.dtype
            value = symb.value
        else:
            dtype = args[2].type
            value = args[2].value
        if (dtype != 'int'):
            raise RuntimeException("Instruction ADD expects all arguments "
                    "of type 'int'", exit_code=53)
        value2 = int(value)
        sub_value = value1 - value2
        var_frame[var_name].value = Variable(dtype=dtype, value=str(sub_value))
