import json
import sys

from main.encode import CaesarEncoder, VigenereEncoder, CaesarDecoder, VigenereDecoder, VernamEncoder, VernamDecoder
from main.hack import CaesarHack
from main.parser import get_args
from main.train import Trainer


if __name__ == '__main__':
    args = get_args()

    if args.mode == 'encode':
        if args.input_file:
            sys.stdin = args.input_file
        if args.output_file:
            sys.stdout = args.output_file
        if args.cipher == 'vernam':
            encoder = VernamEncoder(args.key)
        else:
            encoder = CaesarEncoder(args.key) if args.cipher == 'caesar' else VigenereEncoder(args.key)
        for line in sys.stdin:
            sys.stdout.write(encoder.encode(line))

    if args.mode == 'decode':
        if args.input_file:
            sys.stdin = args.input_file
        if args.output_file:
            sys.stdout = args.output_file
        if args.cipher == 'vernam':
            encoder = VernamDecoder(args.key)
        else:
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
