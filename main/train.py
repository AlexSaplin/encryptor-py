import abc
import json
import string


class Trainer:
    """
    Abstract class for model builders
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def feed(self, text: str):
        """
        Update model
        :param text: Text for feeding
        """
        pass

    @abc.abstractmethod
    def clear(self):
        """
        Clear all data
        """
        pass

    @abc.abstractmethod
    def get_model(self):
        """
        Get model
        :return: Model
        """
        pass

    def get_json_model(self):
        """
        Get model in json format
        :return: Model in json format
        """
        return json.dumps(self.get_model())


class DefaultTrainer(Trainer):
    """
    Class for building frequency model and calculating coincidence index
    """

    def __init__(self):
        super().__init__()
        self.count = {}
        self.letter_count = 0

    def feed(self, text: str):
        """
        Update model
        :param text: Text for feeding
        """
        for symbol in text.lower():
            if symbol.isalpha():
                self.count[symbol] = self.count.get(symbol, 0) + 1
                self.letter_count += 1

    def clear(self):
        """
        Clear all data
        """
        self.count.clear()
        self.letter_count = 0

    def get_model(self):
        """
        Get frequency model with coincidence index
        :return: Frequency model with coincidence index
        """
        result = {'coincidence_index': 0}

        for letter in string.ascii_lowercase:
            result[letter] = self.count.get(letter, 0) / self.letter_count
            if self.letter_count > 1:
                result['coincidence_index'] += (self.count.get(letter, 0) * (self.count.get(letter, 0) - 1)) / \
                                     (self.letter_count * (self.letter_count - 1))

        return result


class BonusTrainer(Trainer):
    """
    Class for building 3-chart frequency model
    """

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
        """
        Update model
        :param text: Text for feeding
        """
        text = text.lower()
        for index in range(2, len(text)):
            letter_count = 0
            for position in range(3):
                letter_count += 1 if text[index - position].isalpha() else 0
            if letter_count == 3:
                self.count[text[index - 2]][text[index - 1]][text[index]] += 1

    def clear(self):
        """
        Clear all data
        """
        self.count = {}

    def get_model(self):
        """
        Get 3-chart frequency model
        :return: 3-chart frequency model
        """
        return self.count
