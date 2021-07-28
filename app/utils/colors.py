class Colored(object):
    def __init__(self, s, features=None):
        if features is None:
            features = []
        self.features = features
        self.string = s

    def __repr__(self):
        return '\033[' + ';'.join(self.features) + 'm' + self.string + '\033[0m'

    def generic_method(self, value):
        return Colored(self.string, features=self.features + [str(value)])

    def black(self):
        return self.generic_method(30)

    def red(self):
        return self.generic_method(31)

    def yellow(self):
        return self.generic_method(33)

    def green(self):
        return self.generic_method(32)

    def blue(self):
        return self.generic_method(34)

    def magenta(self):
        return self.generic_method(35)

    def cyan(self):
        return self.generic_method(36)

    def white(self):
        return self.generic_method(37)

    def bold(self):
        return self.generic_method(1)

    def dim(self):
        return self.generic_method(2)

    def italic(self):
        return self.generic_method(3)

    def underline(self):
        return self.generic_method(4)

    def inverse(self):
        return self.generic_method(7)

    def invisible(self):
        return self.generic_method(8)

    def strike(self):
        return self.generic_method(9)