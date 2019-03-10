import string

from main.encode import CaesarDecoder
from main.train import Trainer


class CaesarHack:

    def __init__(self, model):
        self.model = model
        self.caesar_decoders = [CaesarDecoder(shift) for shift in range(26)]
        self.trainer = Trainer()

    def hack(self, text):
        results = [[0, 0] for shift in range(26)]
        shift_results = 0

        for shift in range(26):
            self.trainer.feed(self.caesar_decoders[shift].encode(text))
            current_model = self.trainer.get_model()
            for letter in string.ascii_lowercase:
                results[shift][0] += (self.model.get(letter, 0) - current_model.get(letter, 0)) ** 2
                results[shift][1] += (self.model.get(letter, 0) - current_model.get(letter, 0)) ** 1.879
            self.trainer.clear()
            if results[shift] < results[shift_results]:
                shift_results = shift

        return self.caesar_decoders[shift_results].encode(text)
