import json
import string

class Trainer:

    def __init__(self):
        self.count = {}
        self.letter_count = 0

    def feed(self, message: str):
        message = message.lower()
        for symbol in message:
            if symbol.isalpha():
                self.count[symbol] = self.count.get(symbol, 0) + 1
                self.letter_count += 1

    def clear(self):
        self.count.clear()
        self.letter_count = 0

    def get_model(self):
        result = {}
        for letter in string.ascii_lowercase:
            result[letter] = self.count.get(letter, 0) / self.letter_count
        return result

    def get_json_model(self):
        return json.dumps(self.get_model())
