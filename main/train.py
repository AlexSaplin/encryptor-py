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
    Class for building n-chart frequency model
    """

    def __init__(self, n):
        super().__init__()
        self.count = {}
        self.n = n

    def feed(self, text: str):
        """
        Update model
        :param text: Text for feeding
        """
        text = text.lower()
        for index in range(0, len(text) - self.n + 1):
            current_slice = text[index:index + self.n]
            if current_slice.isalpha():
                self.count[current_slice] = self.count.get(current_slice, 0) + 1

    def clear(self):
        """
        Clear all data
        """
        self.count = {}

    def get_model(self):
        """
        Get n-chart frequency model
        :return: n-chart frequency model
        """
        return self.count
