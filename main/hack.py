import abc
import string

from main.encode import CaesarDecoder
from main.train import DefaultTrainer


class Hacker:
    """
    Abstract class for hacking text
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, model):
        self.model = model

    @abc.abstractmethod
    def hack(self, text: str):
        """
        Decrypt text
        :param text: Text to decrypt
        :return: Decrypted text
        """
        pass


class CaesarHacker(Hacker):
    """
    Class for hacking Caesar cipher using frequency model
    """

    def __init__(self, model):
        super().__init__(model)
        self.caesar_decoders = [CaesarDecoder(shift) for shift in range(26)]
        self.trainer = DefaultTrainer()

    def hack(self, text: str):
        """
        Decrypt text, encrypted by Caesar cipher, with frequency model
        :param text: Text to decrypt
        :return: Decrypted text
        """
        results = [0 for shift in range(26)]
        shift_result = 0

        for shift in range(26):
            self.trainer.feed(self.caesar_decoders[shift].encode(text))
            current_model = self.trainer.get_model()

            for letter in string.ascii_lowercase:
                results[shift] += (self.model.get(letter, 0) - current_model.get(letter, 0)) ** 2

            self.trainer.clear()
            if results[shift] < results[shift_result]:
                shift_result = shift

        return self.caesar_decoders[shift_result].encode(text)


class CaesarBonusHacker(Hacker):
    """
    Class for hacking Caesar cipher using 3-chart frequency model
    """

    def __init__(self, model):
        super().__init__(model)
        self.caesar_decoders = [CaesarDecoder(shift) for shift in range(26)]

    def hack(self, text: str):
        """
        Decrypt text, encrypted by Caesar cipher, with 3-chart frequency model
        :param text: Text to decrypt
        :return: Decrypted text
        """
        results = [0 for shift in range(26)]
        shift_result = 0

        for shift in range(26):
            current_text = self.caesar_decoders[shift].encode(text).lower()

            for index in range(2, len(current_text)):
                letter_count = 0
                for position in range(3):
                    letter_count += 1 if current_text[index - position].isalpha() else 0
                if letter_count == 3:
                    try:
                        results[shift] += \
                            self.model[current_text[index - 2]][current_text[index - 1]][current_text[index]]
                    except KeyError:
                        raise KeyError('Wrong model format')

            if results[shift] > results[shift_result]:
                shift_result = shift

        return self.caesar_decoders[shift_result].encode(text)


class VigenereHacker(Hacker):
    """
    Class for hacking Vigenere cipher using frequency model and coincidence index method
    """

    def __init__(self, model):
        super().__init__(model)
        try:
            self.coincidence_index = self.model['coincidence_index']
        except KeyError:
            raise KeyError('Wrong model format')

    def calc_coincidence_index(self, text: str):
        """
        Calculate coincidence index
        :param text: Text for calculating
        :return: Coincidence index for text
        """
        count = [0 for letter in range(26)]
        sum_count = 0

        for letter in text:
            if letter.isalpha():
                count[ord(letter.lower()) - ord('a')] += 1
                sum_count += 1

        if sum_count <= 2:
            return 0

        result = 0
        for letter in range(26):
            result += (count[letter] * (count[letter] - 1)) / (sum_count * (sum_count - 1))

        return result

    def check_length(self, text: str, length: int):
        """
        Checks cipher's key length
        :param text: Text for calculating
        :param length: Key length
        :return: Calculated coincidence index for length
        """
        current_text = ''
        for position in range(0, len(text), length):
            current_text += text[position]
        return self.calc_coincidence_index(current_text)

    def hack(self, text: str):
        """
        Decrypt text, encrypted by Vigenere cipher, with frequency model and coincidence index method
        :param text: Text to decrypt
        :return: Decrypted text
        """
        letter_text = ''
        for letter in text:
            if letter.isalpha():
                letter_text += letter.lower()

        len_ic = []
        for length in range(1, len(letter_text)):
            len_ic.append(self.check_length(letter_text, length))

        key_len = 1
        for length, coincidence_index in enumerate(len_ic):
            if abs(coincidence_index - self.coincidence_index) < abs(len_ic[key_len - 1] - self.coincidence_index):
                key_len = length + 1

        strings = ['' for index in range(key_len)]
        for position, symbol in enumerate(letter_text):
            strings[position % key_len] += symbol

        caesar_hacker = CaesarHacker(self.model)

        for index in range(key_len):
            strings[index] = caesar_hacker.hack(strings[index])

        result = ''

        letter_id = 0
        for letter in text:
            if letter.isalpha():
                symbol = strings[letter_id % key_len][letter_id // key_len]
                if letter.isupper():
                    symbol = symbol.upper()
                result += symbol
                letter_id += 1
            else:
                result += letter

        return result
