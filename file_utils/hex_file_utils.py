#! /usr/bin/env python3

import os
import re
import tempfile
from typing import List

def read_hex_file(hex_file_path:str)->list[str]:
    """
    Reads an intel hex file and returns a list of each 32-bit word in order.
    Skips blank lines and address lines.
    """

    # regex to match 32-bit word in hex format
    hex_word_regex = r"^[0-9A-Fa-f]{8}$"

    current_addr = 0
    words:List[str] = []
    with open(hex_file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            line_words = line.split()
            for word in line_words:
                word = word.strip()
                if word.startswith("@"):
                    current_addr = int(word[1:], 16) // 4 # addresses are in bytes, so convert to word addresses
                    if len(words) < current_addr:
                        words.extend("00000000" * (current_addr - len(words)))
                else:
                    if re.match(hex_word_regex, word):
                        words.append(word)
                    else:
                        raise ValueError(f"Invalid hex word: {word}")                    
    return words

def read_hex_file_as_ints(hex_file_path:str)->list[int]:
    """
    Same as read_hex_file, but returns a list of integers instead of strings.

    Returns a list of 32-bit integer words.
    """
    words = read_hex_file(hex_file_path)
    return [int(word, 16) for word in words]


def test_read_hex_file():
    test_hex_file = """
@0
00000000 00000001 00000002 00000003
@4
00000004 00000005
00000006
00000007
@8
00000008
00000009
0000000A
0000000B
0000000C
0000000D
0000000E
0000000F
"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".hex") as temp_file:
        temp_file.write(test_hex_file.encode())
        temp_file_path = temp_file.name
    try:
        words = read_hex_file(temp_file_path)
        assert len(words) == 16
        assert words[0] == "00000000"
        assert words[1] == "00000001"
        assert words[2] == "00000002"
        assert words[3] == "00000003"
        assert words[4] == "00000004"
        assert words[5] == "00000005"
        assert words[6] == "00000006"
        assert words[7] == "00000007"
        assert words[8] == "00000008"
        assert words[9] == "00000009"
        assert words[10] == "0000000A"
        assert words[11] == "0000000B"
        assert words[12] == "0000000C"
        assert words[13] == "0000000D"
        assert words[14] == "0000000E"
        assert words[15] == "0000000F"
    finally:
        os.unlink(temp_file_path)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".hex") as temp_file:
        temp_file.write(test_hex_file.encode())
        temp_file_path = temp_file.name
    try:
        words = read_hex_file_as_ints(temp_file_path)
        assert len(words) == 16
        assert words[0] == 0x00000000
        assert words[1] == 0x00000001
        assert words[2] == 0x00000002
        assert words[3] == 0x00000003
        assert words[4] == 0x00000004
        assert words[5] == 0x00000005
        assert words[6] == 0x00000006
        assert words[7] == 0x00000007
        assert words[8] == 0x00000008
        assert words[9] == 0x00000009
        assert words[10] == 0x0000000A
        assert words[11] == 0x0000000B
        assert words[12] == 0x0000000C
        assert words[13] == 0x0000000D
        assert words[14] == 0x0000000E
        assert words[15] == 0x0000000F
    finally:
        os.unlink(temp_file_path)

    print("✅ test_read_hex_file passed")

if __name__ == "__main__":
    test_read_hex_file()