import json
import re

from constants import athabaskan_char_map

pattern = re.compile(r"[a-z]+")


def pp(data):
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))


def convert_to_eid(text: str) -> str:
    text = text.lower().strip()
    for char, replacement in athabaskan_char_map.items():
        text = text.replace(char, replacement)
    parts = re.findall(pattern, text)
    if not parts:
        return ""
    return "".join(parts)
