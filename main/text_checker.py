class TextChecker:
    """
    Class for check if text is correct
    """

    @staticmethod
    def check(text: str):
        """
        Check if text is correct
        :param text: input text
        :raises: Exception if text contains letters not from english alphabet
        """
        for letter in text:
            if letter.isalpha() and ord(letter) > 122:
                raise Exception('Text cannot contain non-english alphabet letters')
