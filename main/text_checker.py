class TextChecker:

    @staticmethod
    def check(text: str):
        for letter in text:
            if letter.isalpha() and ord(letter) > 122:
                raise Exception('Text cannot contain non-english alphabet letters')
