#!/usr/bin/env python3
##########################################
# Project IPP
# Author: Jan Koci
# Date:   28.2.2018
# Brief:  Implementation of class Program
##########################################

import sys


class Program(object):
"""Docstring for class Program.
This class represents the program to be interpreted """
    def __init__(self, code):
        self.__gf = dict()
        self.__frameStack = list()
        self.__labels = list() # labels could be in frames
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

    def interpret(self):
        # pokud je instrukce bez argumentu
        # musi byt ulozena jako: ("createframe", "")
        for (inst, *args) in self.code:
            try:
                method = getattr(__class__, inst)
                self.method(args)
            except AttributeError as e:
                print("ERROR: Method for instruction {} "
                "is not implemented".format(inst) ,file=sys.stderr)
                raise

    def move(self, args):
        # perform move instruction

    def createframe(self):
        # perform createframe instruction
