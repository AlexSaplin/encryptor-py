import abc


class Encoder:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, key):
        self.key = key

    @abc.abstractmethod
    def calc(self, symbol: str, position: int):
        pass

    def encode(self, message: str):
        result = ''
        position = 0
        for symbol in message:
            if symbol.isalpha():
                result += self.calc(symbol, position)
                position += 1
            else:
                result += symbol
        return result


class CaesarEncoder(Encoder):

    def __init__(self, key):
        key = int(key) % 26
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(code_a + (ord(symbol) - code_a + self.key) % 26)


class VigenereEncoder(Encoder):

    def __init__(self, key):
        key = key.lower()
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(code_a + (ord(symbol) + ord(self.key[position % len(self.key)]) - 2 * code_a) % 26)


class CaesarDecoder(Encoder):

    def __init__(self, key):
        key = int(key) % 26
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(code_a + (ord(symbol) - code_a + 26 - self.key) % 26)


class VigenereDecoder(Encoder):

    def __init__(self, key):
        key = key.lower()
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(code_a + (ord(symbol) - ord(self.key[position % len(self.key)]) + 26) % 26)
