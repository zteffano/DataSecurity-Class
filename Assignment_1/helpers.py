import string


class CharSets:
    """Available character sets for encryption/decryption"""
    ENGLISH = string.ascii_lowercase
    DANISH = string.ascii_lowercase + "æøå"

    @classmethod
    def get_charset(cls, name):
        charset_map = {
            'en': cls.ENGLISH,
            'da': cls.DANISH,
        }
        return charset_map.get(name.lower(), cls.ENGLISH)

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'


def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file: {filename}")
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")


def write_file(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        raise Exception(f"Error writing to file: {str(e)}")