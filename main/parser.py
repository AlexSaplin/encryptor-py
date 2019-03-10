import argparse

def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # encode
    parser_encode = subparsers.add_parser('encode', help='Encode help')
    parser_encode.set_defaults(mode='encode')
    parser_encode.add_argument('--cipher', choices=['caesar', 'vigenere', 'vernam'], help='Cipher type')
    parser_encode.add_argument('--key', help='Cipher key')
    parser_encode.add_argument('--input-file', type=argparse.FileType('r'), help='Input file')
    parser_encode.add_argument('--output-file', type=argparse.FileType('w'), help='Output file')

    # decode
    parser_decode = subparsers.add_parser('decode', help='Decode help')
    parser_decode.set_defaults(mode='decode')
    parser_decode.add_argument('--cipher', choices=['caesar', 'vigenere', 'vernam'], help='Cipher type')
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