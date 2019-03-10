import argparse
import json
import sys

from main.encode import CaesarEncoder, VigenereEncoder, CaesarDecoder, VigenereDecoder
from main.train import Trainer
from main.hack import CaesarHack


def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # encode
    parser_encode = subparsers.add_parser('encode', help='Encode help')
    parser_encode.set_defaults(mode='encode')
    parser_encode.add_argument('--cipher', choices=['caesar', 'vigenere'], help='Cipher type')
    parser_encode.add_argument('--key', help='Cipher key')
    parser_encode.add_argument('--input-file', type=argparse.FileType('r'), help='Input file')
    parser_encode.add_argument('--output-file', type=argparse.FileType('w'), help='Output file')

    # decode
    parser_decode = subparsers.add_parser('decode', help='Decode help')
    parser_decode.set_defaults(mode='decode')
    parser_decode.add_argument('--cipher', choices=['caesar', 'vigenere'], help='Cipher type')
    parser_decode.add_argument('--key', help='Cipher key')
    parser_decode.add_argument('--input-file', type=argparse.FileType('r'), help='Input file')
    parser_decode.add_argument('--output-file', type=argparse.FileType('w'), help='Output file')

    # train
    parser_train = subparsers.add_parser('train', help='Train help')
    parser_train.set_defaults(mode='train')
    parser_train.add_argument('--text-file', type=argparse.FileType('r'), help='Input file')
    parser_train.add_argument('--model-file', type=argparse.FileType('w'), help='Model file')

    # hack
    parser_hack = subparsers.add_parser('hack', help='Hack help')
    parser_hack.set_defaults(mode='hack')
    parser_hack.add_argument('--input-file', type=argparse.FileType('r'), help='Input file')
    parser_hack.add_argument('--output-file', type=argparse.FileType('w'), help='Output file')
    parser_hack.add_argument('--model-file', type=argparse.FileType('r'), help='Model file')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    if args.mode == 'encode':
        if args.input_file:
            sys.stdin = args.input_file
        if args.output_file:
            sys.stdout = args.output_file
        encoder = CaesarEncoder(args.key) if args.cipher == 'caesar' else VigenereEncoder(args.key)
        for line in sys.stdin:
            sys.stdout.write(encoder.encode(line))

    if args.mode == 'decode':
        if args.input_file:
            sys.stdin = args.input_file
        if args.output_file:
            sys.stdout = args.output_file
        encoder = CaesarDecoder(args.key) if args.cipher == 'caesar' else VigenereDecoder(args.key)
        for line in sys.stdin:
            sys.stdout.write(encoder.encode(line))

    if args.mode == 'train':
        if args.text_file:
            sys.stdin = args.text_file
        sys.stdout = args.model_file
        trainer = Trainer()
        for line in sys.stdin:
            trainer.feed(line)
        sys.stdout.write(trainer.get_json_model())

    if args.mode == 'hack':
        model = json.load(args.model_file)
        if args.input_file:
            sys.stdin = args.input_file
        if args.output_file:
            sys.stdout = args.output_file
        text = ''
        caesar_hacker = CaesarHack(model)
        for line in sys.stdin:
            text += line
        sys.stdout.write(caesar_hacker.hack(text))
