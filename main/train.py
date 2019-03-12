import abc
import json
import string


class Trainer:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def feed(self, text: str):
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def get_model(self):
        pass

    def get_json_model(self):
        return json.dumps(self.get_model())


class DefaultTrainer(Trainer):

    def __init__(self):
        super().__init__()
        self.count = {}
        self.letter_count = 0

    def feed(self, text: str):
        for symbol in text.lower():
            if symbol.isalpha():
                self.count[symbol] = self.count.get(symbol, 0) + 1
                self.letter_count += 1

    def clear(self):
        self.count.clear()
        self.letter_count = 0

    def get_model(self):
        result = {'coincidence_index': 0}

        for letter in string.ascii_lowercase:
            result[letter] = self.count.get(letter, 0) / self.letter_count
            if self.letter_count > 1:
                result['coincidence_index'] += (self.count.get(letter, 0) * (self.count.get(letter, 0) - 1)) / \
                                     (self.letter_count * (self.letter_count - 1))

        return result


class BonusTrainer(Trainer):

    def __init__(self):
        super().__init__()
        self.count = {}
        for letter_last in string.ascii_lowercase:
            self.count[letter_last] = {}
            for letter in string.ascii_lowercase:
                self.count[letter_last][letter] = {}
                for letter_next in string.ascii_lowercase:
                    self.count[letter_last][letter][letter_next] = 0

    def feed(self, text: str):
        text = text.lower()
        for index in range(2, len(text)):
            letter_count = 0
            for position in range(3):
                letter_count += 1 if text[index - position].isalpha() else 0
            if letter_count == 3:
                self.count[text[index - 2]][text[index - 1]][text[index]] += 1

    def clear(self):
        self.count = {}

    def get_model(self):
        return self.count
