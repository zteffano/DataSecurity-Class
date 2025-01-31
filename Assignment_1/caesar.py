import argparse
from typing import List, Tuple, Any
from helpers import CharSets, Colors, read_file, write_file


class Caesar:
    def __init__(self, text, charset='en'):
        self.charset = CharSets.get_charset(charset)
        self.text = text.lower()

    def encrypt(self, shift):
        result = ""
        for c in self.text:
            if c in self.charset:
                idx = self.charset.index(c)
                result += self.charset[(idx + shift) % len(self.charset)]
            else:
                result += c
        return result

    def decrypt(self, shift):
        return self.encrypt(-shift)

    def bruteforce(self, danish_guess=False) -> List[Any]:
        """
        Returns list of tuples containing:
        (shift, decrypted_text, word_matches, matched_words)
        """
        outputs = []
        for shift in range(len(self.charset)):
            decrypted = self.decrypt(shift)
            if danish_guess:
                matches, words, positions = danish_words_with_positions(decrypted)
                outputs.append((shift, decrypted, matches, words, positions))
            else:
                outputs.append((shift, decrypted, 0, [], []))

        if danish_guess:
            outputs.sort(key=lambda x: x[2], reverse=True)
        return outputs


def danish_words_with_positions(text: str) -> Tuple[int, List[str], List[Tuple[str, int, int]]]:
    """Returns (number of matches, list of matched words, list of (word, start, end) positions)"""
    word_list = {
        "er", "jeg", "det", "du", "ikke", "at", "en", "og", "har", "vi",
        "til", "på", "hvad", "mig", "med", "de", "den", "for", "der",
        "så", "dig", "han", "kan", "af", "vil"
    }
    matches = []
    positions = []
    words = text.lower().split()

    current_pos = 0
    for word in words:
        word_start = text.find(word, current_pos)
        if word in word_list:
            matches.append(word)
            positions.append((word, word_start, word_start + len(word)))
        current_pos = word_start + len(word)

    return len(matches), matches, positions


def create_bar(value: int, max_value: int, width: int = 20) -> str:
    """Creates a visual bar representation of a value"""
    if max_value == 0:
        return f"{Colors.BLUE}{'█' * width}{Colors.END}"
    filled = int((value / max_value) * width)
    return f"{Colors.BLUE}{'█' * filled}{Colors.END}{'░' * (width - filled)}"


def colorize_text(text: str, positions: List[Tuple[str, int, int]]) -> str:
    """Colorize matched words in text"""
    if not positions:
        return text

    result = []
    last_end = 0

    for word, start, end in sorted(positions, key=lambda x: x[1]):
        # Add text before the match
        result.append(text[last_end:start])
        # Add the highlighted match
        result.append(f"{Colors.GREEN}{text[start:end]}{Colors.END}")
        last_end = end

    # Add remaining text
    result.append(text[last_end:])
    return "".join(result)


def format_bruteforce_results(brute_results: List[Tuple[int, str, int, List[str], List]],
                              max_results: int = 26) -> str:
    """Format bruteforce brute_results with visual indicators and colored matches"""
    if not brute_results:
        return "No results found."

    # Get maximum match count for scaling bars
    max_matches = max(result[2] for result in brute_results) if brute_results[0][2] > 0 else 1

    # Limit brute_results if specified
    if max_results:
        brute_results = brute_results[:max_results]

    # Format each result
    output_lines = [
        f"{Colors.BOLD}Bruteforce Analysis Results:{Colors.END}",
        "=" * 80
    ]

    for shift, text, matches, words, positions in brute_results:
        if matches > 0:
            bar = create_bar(matches, max_matches)
            matched_words = f"{Colors.YELLOW}{', '.join(words)}{Colors.END}"
            colored_text = colorize_text(text, positions)
            output_lines.extend([
                f"Shift {shift:2d} | Matches: {matches:2d} {bar}",
                f"Words: {matched_words}",
                f"Text: {colored_text[:100]}{'...' if len(text) > 100 else ''}",
                "-" * 80
            ])
        else:
            continue # Skip results with no matches
            output_lines.extend([
                f"Shift {shift:2d} | No matches",
                f"Text: {text[:100]}{'...' if len(text) > 100 else ''}",
                "-" * 80
            ])

    return "\n".join(output_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Caesar cipher encryption/decryption tool')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--text', help='Text to process')
    group.add_argument('-f', '--file', help='Input file path')

    parser.add_argument('-s', '--shift', type=int, help='Shift value for encryption/decryption')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt mode')
    parser.add_argument('-b', '--bruteforce', action='store_true', help='Bruteforce mode')
    parser.add_argument('-c', '--charset', default='en',
                        choices=['en', 'da', 'de'],
                        help='Character set to use (en=English, da=Danish, de=German)')
    parser.add_argument('--danish', action='store_true', help='Use Danish word analysis')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    parser.add_argument('-n', '--num-results', type=int, default=26,
                        help='Number of results to show in bruteforce mode (default: 26)')

    args = parser.parse_args()

    try:
        input_text = read_file(args.file) if args.file else args.text
        cipher = Caesar(input_text, args.charset)

        if args.bruteforce:
            results = cipher.bruteforce(args.danish)
            output = format_bruteforce_results(results, args.num_results)
        elif args.shift is not None:
            output = cipher.decrypt(args.shift) if args.decrypt else cipher.encrypt(args.shift)
        else:
            parser.print_help()
            exit(1)

        if args.output:
            # Remove color codes when writing to file
            output = output.replace(Colors.GREEN, '').replace(Colors.BLUE, '') \
                .replace(Colors.YELLOW, '').replace(Colors.END, '') \
                .replace(Colors.BOLD, '')
            write_file(args.output, output)
            print(f"Results written to {args.output}")
        else:
            print(output)

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)