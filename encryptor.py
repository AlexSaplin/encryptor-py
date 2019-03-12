import json
import sys

from main.encode import CaesarEncoder, VigenereEncoder, CaesarDecoder, VigenereDecoder, VernamEncoder, VernamDecoder
from main.hack import CaesarHacker, CaesarBonusHacker, VigenereHacker
from main.parser import get_args
from main.text_checker import TextChecker
from main.train import DefaultTrainer, BonusTrainer


def encode(args):
    if args.input_file:
        sys.stdin = args.input_file
    if args.output_file:
        sys.stdout = args.output_file
    if args.cipher == 'vernam':
        encoder = VernamEncoder(args.key)
    else:
        encoder = CaesarEncoder(args.key) if args.cipher == 'caesar' else VigenereEncoder(args.key)
    text = ''
    for line in sys.stdin:
        text += line
    TextChecker.check(text)
    sys.stdout.write(encoder.encode(text))


def decode(args):
    if args.input_file:
        sys.stdin = args.input_file
    if args.output_file:
        sys.stdout = args.output_file
    if args.cipher == 'vernam':
        encoder = VernamDecoder(args.key)
    else:
        encoder = CaesarDecoder(args.key) if args.cipher == 'caesar' else VigenereDecoder(args.key)
    text = ''
    for line in sys.stdin:
        text += line
    TextChecker.check(text)
    sys.stdout.write(encoder.encode(text))


def train(args):
    if args.text_file:
        sys.stdin = args.text_file
    sys.stdout = args.model_file
    trainer = BonusTrainer() if args.bonus_mode else DefaultTrainer()
    text = ''
    for line in sys.stdin:
        text += line
    TextChecker.check(text)
    trainer.feed(text)
    sys.stdout.write(trainer.get_json_model())


def hack(args):
    try:
        model = json.load(args.model_file)
    except json.JSONDecodeError:
        raise Exception('Incorrect model file')
    if args.input_file:
        sys.stdin = args.input_file
    if args.output_file:
        sys.stdout = args.output_file
    text = ''
    if args.bonus_mode:
        if args.cipher == 'vigenere':
            raise NotImplementedError('Current version does not support bonus hack for vigenere cipher')
        else:
            hacker = CaesarBonusHacker(model)
    else:
        hacker = CaesarHacker(model) if args.cipher == 'caesar' else VigenereHacker(model)
    for line in sys.stdin:
        text += line
    TextChecker.check(text)
    sys.stdout.write(hacker.hack(text))


if __name__ == '__main__':
    arguments = get_args()

    if arguments.mode == 'encode':
        encode(arguments)

    if arguments.mode == 'decode':
        decode(arguments)

    if arguments.mode == 'train':
        train(arguments)

    if arguments.mode == 'hack':
        hack(arguments)
