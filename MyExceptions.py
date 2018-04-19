#!/usr/bin/env python3
import sys

class InterpretException(Exception):
    """docstring for InterpretException."""
    def __init__(self, message):
        print("ERROR: " + message, file=sys.stderr)

class RuntimeException(InterpretException):
    """docstring for RuntimeException."""
    def __init__(self, message="", exit_code=99):
        self.exit_code = exit_code
        self.message = "RuntimeException: " + message
        super().__init__(self.message)

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
