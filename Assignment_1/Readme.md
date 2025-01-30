# Simple Cipher Tools

A collection of command-line tools for encrypting and decrypting text using Caesar and Vigenère ciphers. Supports multiple character sets including English and Danish
Made for a school assignment in the class "Data Security"

## Files
- `caesar.py`: Implementation of Caesar cipher with bruteforce capabilities
- `vigenere.py`: Implementation of Vigenère cipher
- `helpers.py`: Utility functions and character set definitions

## Features
- Multiple character sets (English, Danish)
- File input/output support
- Enhanced bruteforce analysis for Caesar cipher
- Danish word frequency analysis
- Visual frequency display in bruteforce mode
- Colorized output for bruteforce results

## Usage Examples

### Caesar Cipher

Basic encryption:
```bash
python caesar.py -t "hello world" -s 3
```

Using Danish charset:
```bash
python caesar.py -t "hej med dig" -s 3 -c da
```

Decrypt text from file:
```bash
python caesar.py -f dkexit_message.txt -s 7 -d -o decrypted.txt
```

Bruteforce with Danish word analysis:
```bash
python caesar.py -f dkexit_message.txt -b --danish

# Show more results (default is 5)
python caesar.py -f dkexit_message.txt -b --danish -n 10
```

Example bruteforce output:
```
Bruteforce Analysis Results:
================================================================================
Shift  7 | Matches:  4 ████████████████████
Words: jeg, til, med, kan
Text: jeg går til fodbold hver tirsdag aften og jeg kan godt lide kaffe
--------------------------------------------------------------------------------
```

### Vigenère Cipher

Basic encryption:
```bash
python vigenere.py -t "THEY DRINK THE TEA" -k DUH -c en
```

Using Danish charset:
```bash
python vigenere.py -t "hej med dig" -k hemmelig -c da
```

Decrypt from file, using the example from: http://dkexit.eu/courses/websec/sec1/
```bash
python vigenere.py -f dkexit_vigmessage.txt -k DUH -d -o decrypted_vig.txt
```

## Command Line Options

### Caesar Cipher
- `-t, --text`: Text to process
- `-f, --file`: Input file path
- `-s, --shift`: Shift value for encryption/decryption
- `-d, --decrypt`: Decrypt mode
- `-b, --bruteforce`: Bruteforce mode
- `-c, --charset`: Character set (en/da/de)
- `--danish`: Use Danish word analysis
- `-o, --output`: Output file path
- `-n, --num-results`: Number of results to show in bruteforce mode (default: 5)

### Vigenère Cipher
- `-t, --text`: Text to process
- `-f, --file`: Input file path
- `-k, --key`: Encryption/decryption key
- `-d, --decrypt`: Decrypt mode
- `-c, --charset`: Character set (en/da/de)
- `-o, --output`: Output file path

## Character Sets
Available character sets:
- English (en): a-z
- Danish (da): a-z + æøå

## Error Handling
- Comprehensive error handling for file operations
- Input validation for character sets and command-line arguments
- Clear error messages for troubleshooting