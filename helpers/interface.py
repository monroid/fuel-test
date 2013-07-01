#!/usr/bin/env python
"""
This module is used for controlling CLI program output and debug levels.
"""
import sys
from color import Color


class Interface:
    """
    This class is used to control messages and logs
    """
    def __init__(
            self,
            debug_level=1,
            debug_output="stderr",
            error_output="stderr",
            notify_output="stdout",
            info_output="stdout",
            encoding="UTF-8",
            error_color=Color(foreground='red'),
            debug_color=Color(foreground='green'),
            notify_color=Color(foreground='cyan'),
            info_color=Color(foreground='blue'),
    ):
        """
        Constructor.
        """
        self.debug_level = debug_level
        self.debug_output = debug_output
        self.error_output = error_output
        self.notify_output = notify_output
        self.info_output = info_output
        self.encoding = encoding
        self.offset_character = "  "
        self.error_color = error_color
        self.debug_color = debug_color
        self.notify_color = notify_color
        self.info_color = info_color

    def __out(self, output, message, color=None):
        """
        Message output.
        """
        message = message.encode(self.encoding)
        if color:
            message = color(message)
        if output == "stderr":
            sys.stderr.write(message + "\n")
        elif output == "stdout":
            sys.stdout.write(message + "\n")
        else:
            print "to file: ", output, message

    def fill(self, message, width):
        """
        Fill string into column with width. Useful for making text tables.
        """
        if type(message) != unicode:
            message = message.decode('UTF-8')
        message = message.ljust(width)[0:width]
        return message

    def debug(self, message, level=1, offset=0):
        """
        Output debug messages. Arguments: message, (level), (offset)
        Show messages if their level is less or equal to program's
        debug level. If offset is not set then it is equal to debug level.
        """
        color = self.debug_color
        level = int(level)
        offset = int(offset)

        if not offset:
            offset = level

        if level <= self.debug_level:
            if type(message) != unicode:
                message = str(message).decode('UTF-8')
            message = offset * self.offset_character + message
            self.__out(self.debug_output, message, color)

    def error(self, message, code=0):
        """
        Output error messages. Arguments: message, (code)
        If code > 0 then exit program!
        """
        color = self.error_color
        if type(message) != unicode:
            message = str(message).decode('UTF-8')
        self.__out(self.error_output, message, color)
        if int(code) > 0:
            sys.exit(code)

    def notify(self, message, offset=0):
        """
        Output notify messages. Arguments: message, (offset_level)
        """
        color = self.notify_color
        offset = int(offset)

        if type(message) != unicode:
            message = str(message).decode('UTF-8')
        message = offset * self.offset_character + message
        self.__out(self.notify_output, message, color)

    def info(self, message, offset=0):
        """
        Output info messages. Arguments: message, (offset_level)
        """
        color = self.info_color
        offset = int(offset)

        if type(message) != unicode:
            message = str(message).decode('UTF-8')
        message = offset * self.offset_character + message
        self.__out(self.info_output, message, color)

if __name__ == '__main__':
    INT = Interface()
    message = 'Hello, World!'
    INT.error('Error: ' + message)
    INT.debug('Debug: ' + message)
    INT.notify('Notify: ' + message)
    INT.info('Info: ' + message)