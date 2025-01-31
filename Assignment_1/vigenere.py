import argparse
from helpers import CharSets, read_file, write_file



class Vigenere:
    def __init__(self, text, charset='en'):
        self.charset = CharSets.get_charset(charset)
        self.text = text.lower()

    def get_shifts(self, key):
        return [self.charset.index(c) for c in key.lower() if c in self.charset]

    def encrypt(self, key):
        shifts = self.get_shifts(key)
        if not shifts:
            raise ValueError("Key must contain at least one letter")

        result = ""
        j = 0
        for c in self.text:
            if c in self.charset:
                shift = shifts[j % len(shifts)]
                idx = self.charset.index(c)
                result += self.charset[(idx + shift) % len(self.charset)]
                j += 1
            else:
                result += c
        return result

    def decrypt(self, key):
        shifts = self.get_shifts(key)
        if not shifts:
            raise ValueError("Key must contain at least one letter")

        result = ""
        j = 0
        for c in self.text:
            if c in self.charset:
                shift = shifts[j % len(shifts)]
                idx = self.charset.index(c)
                result += self.charset[(idx - shift) % len(self.charset)]
                j += 1
            else:
                result += c
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vigenere cipher encryption/decryption tool')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--text', help='Text to process')
    group.add_argument('-f', '--file', help='Input file path')

    parser.add_argument('-k', '--key', required=True, help='Encryption/decryption key')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt mode')
    parser.add_argument('-c', '--charset', default='en',
                        choices=['en', 'da', 'de'],
                        help='Character set to use (en=English, da=Danish)')
    parser.add_argument('-o', '--output', help='Output file path (optional)')

    args = parser.parse_args()

    try:
        input_text = read_file(args.file) if args.file else args.text
        cipher = Vigenere(input_text, args.charset)

        output = cipher.decrypt(args.key) if args.decrypt else cipher.encrypt(args.key)

        if args.output:
            write_file(args.output, output)
            print(f"Results written to {args.output}")
        else:
            print(output)

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)