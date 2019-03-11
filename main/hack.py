import abc
import string
from tqdm import tqdm

from main.encode import CaesarDecoder
from main.train import Trainer


class Hacker:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, model):
        self.model = model

    @abc.abstractmethod
    def hack(self, text: str):
        pass


class CaesarHacker(Hacker):

    def __init__(self, model):
        super().__init__(model)
        self.caesar_decoders = [CaesarDecoder(shift) for shift in range(26)]
        self.trainer = Trainer()

    def hack(self, text: str):
        results = [0 for shift in range(26)]
        shift_results = 0

        for shift in range(26):
            self.trainer.feed(self.caesar_decoders[shift].encode(text))
            current_model = self.trainer.get_model()
            for letter in string.ascii_lowercase:
                results[shift] += (self.model.get(letter, 0) - current_model.get(letter, 0)) ** 2
            self.trainer.clear()
            if results[shift] < results[shift_results]:
                shift_results = shift

        return self.caesar_decoders[shift_results].encode(text)


class VigenereHacker(Hacker):

    def __init__(self, model):
        super().__init__(model)
        self.coincidence_index = self.model['coincidence_index']

    def calc_coincidence_index(self, text: str):
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

    def check_len(self, text: str, length: int):
        current_text = ''
        for position in range(0, len(text), length):
            current_text += text[position]
        return self.calc_coincidence_index(current_text)

    def hack(self, text: str):
        letter_text = ''
        for letter in text:
            if letter.isalpha():
                letter_text += letter.lower()

        len_ic = []
        for length in range(1, len(letter_text)):
            len_ic.append(self.check_len(letter_text, length))

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
