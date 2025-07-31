import json
from string import ascii_lowercase

from constants import athabaskan_char_map


def pp(data):
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))


def convert_to_eid(s: str) -> str:
    s = s.lower().strip()
    chars = []
    for char in s:
        if char in athabaskan_char_map:
            chars.append(athabaskan_char_map[char])
        elif char in ascii_lowercase:
            chars.append(char)
    return "".join(chars)
