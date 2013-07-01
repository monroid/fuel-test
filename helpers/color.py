#!/usr/bin/env pyton

# 8 colors mode
# 30 - 37 - Foreground color codes
# 40 - 47 - Background color codes
# 0 - 9 - Special Attributes
#
# 16 colors mode
# color + 60 = 'bright' version
#
# 256 Colors mode (not supported by this module)
# 38;5;ColorNumber - 256 color mode Foreground
# 48;5;ColorNumber - 256 color mode Background
# ColorNumber - 1 - 256 color code


class Color:
    """
    This class is used for coloring terminal output of Python programs
    """

    def __init__(self, foreground=None, background=None, attribute=0, enabled=True, bright_foreground=False,
                 bright_background=False):
        """
        Constructor. Can take color settins when creating class.
        """
        self.start = "\033["
        self.end = "m"
        self.reset = self.start + "0" + self.end

        if enabled:
            self.enabled = True
        else:
            self.enabled = False

        if bright_foreground:
            self.bright_foreground = True
        else:
            self.bright_foreground = False

        if bright_background:
            self.bright_background = True
        else:
            self.bright_background = False

        self.foreground_offset = 30
        self.background_offset = 40
        self.bright_offset = 60

        self.color_table = {
            'black': 0,
            'red': 1,
            'green': 2,
            'yellow': 3,
            'blue': 4,
            'magneta': 5,
            'cyan': 6,
            'white': 7,
            'off': None,
        }

        self.attribute_table = {
            'normal': 0,
            'bold': 1,
            'faint': 2,
            'italic': 3,
            'underline': 4,
            'blink': 5,
            'rblink': 6,
            'negative': 7,
            'conceal': 8,
            'crossed': 9,
            'off': 0,
        }

        self.set_foreground_color(foreground)
        self.set_background_color(background)
        self.set_attribute(attribute)

    def set_enabled(self, status):
        """"
        Enable or disable all colors.
        """
        if status:
            self.enabled = True
        else:
            self.enabled = False

    def set_bright_foreground(self, status):
        """
        Enable and disable of bright foreground.
        """
        if status:
            self.bright_foreground = True
        else:
            self.bright_foreground = False

    def set_bright_background(self, status):
        """
        Enable and disable of bright background.
        """
        if status:
            self.bright_background = True
        else:
            self.bright_background = False

    def set_foreground_color(self, color):
        """
        Set foreground color or color code.
        """
        if type(color) == int:
            self.foreground = color
            return True
        if self.color_table.has_key(color):
            self.foreground = self.color_table[color]
            return True
        self.foreground = None
        return False

    def set_background_color(self, color):
        """
        Set background color or color code.
        """
        if type(color) == int:
            self.background = color
            return True
        if self.color_table.has_key(color):
            self.background = self.color_table[color]
            return True
        self.background = None
        return False

    def set_attribute(self, color):
        """
        Set additional text attribute code.
        """
        if type(color) == int:
            self.attribute = color
            return True
        if self.attribute_table.has_key(color):
            self.attribute = self.attribute_table[color]
            return True
        self.attribute = 0
        return False

    def make_escapes(self):
        """
        Print color enabling escape chars.
        """
        codes = []
        attribute = self.attribute

        if self.foreground is not None:
            foreground = self.foreground_offset + self.foreground
            if self.bright_foreground:
                foreground += self.bright_offset
        else:
            foreground = None

        if self.background is not None:
            background = self.background_offset + self.background
            if self.bright_background:
                background += self.bright_offset
        else:
            background = None

        codes.append(attribute)

        if foreground:
            codes.append(foreground)
        if background:
            codes.append(background)

        escape_string = self.start + ";".join(map(str, codes)) + self.end
        return escape_string

    def print_chart(self):
        """
        Prints demo color chart tot test terminal support.
        """
        for fg in range(0, 7):
            for bg in range(0, 7):
                for attr in sorted(self.attribute_table.values()):
                    demo_color = Color(foreground=fg, background=bg, attribute=attr,
                                       bright_foreground=False, bright_background=False)
                    print demo_color("Hello World!"), repr(demo_color)
                    demo_color.bright_foreground = True
                    print demo_color("Hello World!"), repr(demo_color)
                    demo_color.bright_background = True
                    print demo_color("Hello World!"), repr(demo_color)

    def __str__(self):
        return self.make_escapes()

    def __repr__(self):
        return "Color(fgcode = %s, bgcode = %s, attrcode = %s, enabled = %s, brightfg = %s, brightbg = %s)" % (
            str(self.foreground),
            str(self.background),
            str(self.attribute),
            str(self.enabled),
            str(self.bright_foreground),
            str(self.bright_background),
        )

    def __call__(self, input_string):
        if self.enabled:
            return self.make_escapes() + input_string + self.reset
        else:
            return input_string


if __name__ == '__main__':
    CLR = Color()
    CLR.print_chart()
