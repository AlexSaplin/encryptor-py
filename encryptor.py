import argparse
import json
import sys

from main.encode import CaesarEncoder, VigenereEncoder, CaesarDecoder, VigenereDecoder, VernamEncoder, VernamDecoder
from main.hack import CaesarHacker, CaesarBonusHacker, VigenereHacker
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
    text = args.input_file.read() if args.input_file else sys.stdin.read()
    TextChecker.check(text)
    if args.output_file:
        args.output_file.write(encoder.encode(text))
    else:
        sys.stdout.write(encoder.encode(text))


def decode(args):
    if args.input_file:
        sys.stdin = args.input_file
    if args.output_file:
        sys.stdout = args.output_file
    if args.cipher == 'vernam':
        decoder = VernamDecoder(args.key)
    else:
        decoder = CaesarDecoder(args.key) if args.cipher == 'caesar' else VigenereDecoder(args.key)
    text = args.input_file.read() if args.input_file else sys.stdin.read()
    TextChecker.check(text)
    if args.output_file:
        args.output_file.write(decoder.encode(text))
    else:
        sys.stdout.write(decoder.encode(text))


def train(args):
    if args.text_file:
        sys.stdin = args.text_file
    sys.stdout = args.model_file
    trainer = BonusTrainer() if args.bonus_mode else DefaultTrainer()
    text = args.input_file.read() if args.input_file else sys.stdin.read()
    TextChecker.check(text)
    trainer.feed(text)
    if args.output_file:
        args.output_file.write(trainer.get_json_model())
    else:
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
    if args.bonus_mode:
        if args.cipher == 'vigenere':
            raise NotImplementedError('Current version does not support bonus hack for vigenere cipher')
        else:
            hacker = CaesarBonusHacker(model)
    else:
        hacker = CaesarHacker(model) if args.cipher == 'caesar' else VigenereHacker(model)
    text = args.input_file.read() if args.input_file else sys.stdin.read()
    TextChecker.check(text)
    if args.output_file:
        args.output_file.write(hacker.hack(text))
    else:
        sys.stdout.write(hacker.hack(text))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Allows you to work with caesar/vigenere/vernam ciphers.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()

    # encode
    parser_encode = subparsers.add_parser('encode', help='Encode help')
    parser_encode.set_defaults(mode='encode', func=encode)
    parser_encode.add_argument('--cipher', choices=['caesar', 'vigenere', 'vernam'], help='Cipher type', required=True)
    parser_encode.add_argument('--key', help='Cipher key', required=True)
    parser_encode.add_argument('--input-file', type=argparse.FileType('r'), help='Input file')
    parser_encode.add_argument('--output-file', type=argparse.FileType('w'), help='Output file')

    # decode
    parser_decode = subparsers.add_parser('decode', help='Decode help')
    parser_decode.set_defaults(mode='decode', func=decode)
    parser_decode.add_argument('--cipher', choices=['caesar', 'vigenere', 'vernam'], help='Cipher type', required=True)
    parser_decode.add_argument('--key', help='Cipher key', required=True)
    parser_decode.add_argument('--input-file', type=argparse.FileType('r'), help='Input file')
    parser_decode.add_argument('--output-file', type=argparse.FileType('w'), help='Output file')

    # train
    parser_train = subparsers.add_parser('train', help='Train help')
    parser_train.set_defaults(mode='train', func=train)
    parser_train.add_argument('--text-file', type=argparse.FileType('r'), help='Input file')
    parser_train.add_argument('--model-file', type=argparse.FileType('w'), help='Model file', required=True)
    parser_train.add_argument('--bonus', dest='bonus_mode', action='store_true')

    # hack
    parser_hack = subparsers.add_parser('hack', help='Hack help')
    parser_hack.set_defaults(mode='hack', func=hack)
    parser_hack.add_argument('--cipher', choices=['caesar', 'vigenere'], help='Cipher type', required=True)
    parser_hack.add_argument('--input-file', type=argparse.FileType('r'), help='Input file')
    parser_hack.add_argument('--output-file', type=argparse.FileType('w'), help='Output file')
    parser_hack.add_argument('--model-file', type=argparse.FileType('r'), help='Model file', required=True)
    parser_hack.add_argument('--bonus', dest='bonus_mode', action='store_true')

    arguments = parser.parse_args()
    arguments.func(arguments)
