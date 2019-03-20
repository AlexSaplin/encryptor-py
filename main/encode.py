import abc


class Encoder:
    """
    Abstract class for caesar/vigenere encoders/decoders
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, key):
        self.key = key

    @abc.abstractmethod
    def calc(self, symbol: str, position: int):
        """
        Get encoded/decoded symbol
        :param symbol: char to encode/decode
        :param position: symbol's position in text
        :return: Calculated symbol
        """
        pass

    def encode(self, text: str):
        """
        Encode/decode text
        :param text: text to encode/decode
        :return: Encoded/decoded text
        """
        result = ''
        position = 0
        for symbol in text:
            if symbol.isalpha():
                result += self.calc(symbol, position)
                position += 1
            else:
                result += symbol
        return result


class CaesarEncoder(Encoder):
    """
    Class for encoding by Caesar cipher
    """

    def __init__(self, key):
        key = int(key) % 26
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        """
        Get encoded/decoded symbol
        :param symbol: char to encode/decode
        :param position: symbol's position in text
        :return: Calculated symbol
        """
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(code_a + (ord(symbol) - code_a + self.key) % 26)


class VigenereEncoder(Encoder):
    """
    Class for encoding by Vigenere cipher
    """

    def __init__(self, key):
        key = key.lower()
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        """
        Get encoded/decoded symbol
        :param symbol: char to encode/decode
        :param position: symbol's position in text
        :return: Calculated symbol
        """
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(code_a + (ord(symbol) + ord(self.key[position % len(self.key)]) - code_a - ord('a')) % 26)


class CaesarDecoder(Encoder):
    """
    Class for decoding by Caesar cipher
    """

    def __init__(self, key):
        key = int(key) % 26
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        """
        Get encoded/decoded symbol
        :param symbol: char to encode/decode
        :param position: symbol's position in text
        :return: Calculated symbol
        """
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(code_a + (ord(symbol) - code_a + 26 - self.key) % 26)


class VigenereDecoder(Encoder):
    """
    Class for decoding by Vigenere cipher
    """

    def __init__(self, key):
        key = key.lower()
        super().__init__(key)

    def calc(self, symbol: str, position: int):
        """
        Get encoded/decoded symbol
        :param symbol: char to encode/decode
        :param position: symbol's position in text
        :return: Calculated symbol
        """
        code_a = ord('A') if symbol.isupper() else ord('a')
        return chr(code_a + (ord(symbol) - code_a - ord(self.key[position % len(self.key)]) + ord('a') + 26) % 26)


class VernamEncoder:
    """
    Class for encoding by Vernam cipher
    """

    def __init__(self, key):
        self.key = int(key)

    def encode(self, text):
        """
        Encode/decode text
        :param text: text to encode/decode
        :return: Encoded/decoded text
        """
        binary_text = ''
        for symbol in text:
            binary_text += bin(ord(symbol))[2:]
        return bin(int(binary_text, 2) ^ self.key)[2:]


class VernamDecoder:
    """
    Class for decoding by Vernam cipher
    """

    def __init__(self, key):
        self.key = int(key)

    def encode(self, text: str):
        """
        Encode/decode text
        :param text: text to encode/decode
        :return: Encoded/decoded text
        """
        binary_result = bin(self.key ^ int(text, 2))[2:]
        result = ''
        for symbol in range(0, len(binary_result), 7):
            result += chr(int(binary_result[symbol:symbol + 7], 2))
        return result
