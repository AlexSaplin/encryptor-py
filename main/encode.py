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
        return chr(code_a + (ord(symbol) + ord(self.key[position % len(self.key)]) - code_a - ord('a')) % 26)


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


class VernamEncoder:

    def __init__(self, key):
        self.key = int(key)

    def encode(self, message):
        binary_message = ''
        for symbol in message:
            binary_message += bin(ord(symbol))[2:]
        return bin(int(binary_message, 2) ^ self.key)[2:]


class VernamDecoder:

    def __init__(self, key):
        self.key = int(key)

    def encode(self, message: str):
        binary_result = bin(self.key ^ int(message, 2))[2:]
        result = ''
        for symbol in range(0, len(binary_result), 7):
            result += chr(int(binary_result[symbol:symbol + 7], 2))
        return result
