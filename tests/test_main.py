import random
import string

import pytest

from main.encode import CaesarEncoder, CaesarDecoder, VigenereEncoder, VigenereDecoder
from main.hack import VigenereHacker, CaesarHacker, CaesarBonusHacker
from main.train import DefaultTrainer, BonusTrainer


def get_random_string(text_length):
    return ''.join([random.choice(string.ascii_letters) for _ in range(text_length)])


class TestEncodeDecode:

    @pytest.mark.parametrize("text_length, key", [
        (1, 2),
        (1000, 26),
        (10000, 31),
        (100000, 11)
    ])
    def test_caesar_encoder_decoder(self, text_length, key):
        text = get_random_string(text_length)
        caesar_encoder = CaesarEncoder(key)
        encrypted_text = caesar_encoder.encode(text)
        caesar_decoder = CaesarDecoder(key)
        assert caesar_decoder.encode(encrypted_text) == text

    @pytest.mark.parametrize("text_length, key_length", [
        (1, 3),
        (1000, 5),
        (10000, 300),
        (100000, 7),
        (100000, 30)
    ])
    def test_vigenere_encoder_decoder(self, text_length, key_length):
        text = get_random_string(text_length)
        key = get_random_string(key_length)
        vigenere_encoder = VigenereEncoder(key)
        encrypted_text = vigenere_encoder.encode(text)
        vigenere_decoder = VigenereDecoder(key)
        assert vigenere_decoder.encode(encrypted_text) == text


class TestTrainerHacker:

    @pytest.mark.parametrize("train_filename, text_filename, key", [
        ('src/1.txt', 'src/2.txt', 5),
        ('src/3.txt', 'src/4.txt', 7),
        ('src/2.txt', 'src/3.txt', 11),
        ('src/4.txt', 'src/2.txt', 13)
    ])
    def test_main_caesar_hacker(self, train_filename, text_filename, key):
        train_file = open(train_filename, 'r')
        text_file = open(text_filename, 'r')

        trainer = DefaultTrainer()
        trainer.feed(train_file.read())
        model = trainer.get_model()

        text = text_file.read()

        caesar_encoder = CaesarEncoder(key)
        encrypted_text = caesar_encoder.encode(text)

        hacker = CaesarHacker(model)
        assert hacker.hack(encrypted_text) == text

    @pytest.mark.parametrize("train_filename, text_filename, key_length", [
        ('src/1.txt', 'src/2.txt', 2),
        ('src/3.txt', 'src/4.txt', 97),
        ('src/2.txt', 'src/3.txt', 31),
        ('src/4.txt', 'src/2.txt', 14)
    ])
    def test_vigenere_hacker(self, train_filename, text_filename, key_length):
        train_file = open(train_filename, 'r')
        text_file = open(text_filename, 'r')

        trainer = DefaultTrainer()
        trainer.feed(train_file.read())
        model = trainer.get_model()

        text = text_file.read()

        key = get_random_string(key_length)
        vigenere_encoder = VigenereEncoder(key)
        encrypted_text = vigenere_encoder.encode(text)

        hacker = VigenereHacker(model)
        assert hacker.hack(encrypted_text) == text

    @pytest.mark.parametrize("train_filename, text_filename, key, n", [
        ('src/1.txt', 'src/2.txt', 5, 3),
        ('src/3.txt', 'src/4.txt', 7, 4),
        ('src/2.txt', 'src/3.txt', 11, 2),
        ('src/4.txt', 'src/2.txt', 13, 6)
    ])
    def test_bonus_caesar_hacker(self, train_filename, text_filename, key, n):
        train_file = open(train_filename, 'r')
        text_file = open(text_filename, 'r')

        trainer = BonusTrainer(n)
        trainer.feed(train_file.read())
        model = trainer.get_model()

        text = text_file.read()

        caesar_encoder = CaesarEncoder(key)
        encrypted_text = caesar_encoder.encode(text)

        hacker = CaesarBonusHacker(model, n)
        assert hacker.hack(encrypted_text) == text
