import json
import string


class Trainer:

    def __init__(self):
        self.count = {}
        self.letter_count = 0

    def feed(self, message: str):
        for symbol in message.lower():
            if symbol.isalpha():
                self.count[symbol] = self.count.get(symbol, 0) + 1
                self.letter_count += 1

    def clear(self):
        self.count.clear()
        self.letter_count = 0

    def get_model(self):
        result = {}
        coincidence_index = 0
        for letter in string.ascii_lowercase:
            result[letter] = self.count.get(letter, 0) / self.letter_count
            if self.letter_count > 1:
                coincidence_index += (self.count.get(letter, 0) * (self.count.get(letter, 0) - 1)) / \
                                     (self.letter_count * (self.letter_count - 1))
        result['coincidence_index'] = coincidence_index
        return result

    def get_json_model(self):
        return json.dumps(self.get_model())
