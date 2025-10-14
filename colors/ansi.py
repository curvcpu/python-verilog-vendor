import sys
from typing import Optional
from enum import Enum

"""
This is a safe string coloring tool that will omit colors in pipes (by default), and 
lets you operate on the string normally even after a color has been applied.

Usage:

    ansi = AnsiColorsTool()

    print(f"{ansi.br_blue}Hello, World!{ansi.reset}")

    # or just wrap the string

    print(ansi.br_green("Hello, World!"))

    # you can also make strings that are color tagged but still behave like normal strings:

    s = "abc"
    t = "def"
    s = ansi.colorize_string(s, "green")
    t = ansi.colorize_string(t, "blue")
    assert len(s) == 3       # will pass because 'abc' is the string
    assert s[-1] == "c"      # will pass because slice operator works on the string
    assert t[0:3] == "def"   # will pass because 'def' is the string
    assert len(s+t) == 6     # will pass because 'abcdef' is the string

    # only upon print will the ansi escape sequences be applied
    print(s)                 # will print 'abc' in green because the string is color tagged
    print(t)                 # will print 'def' in blue because the string is color tagged
    print(s + t)             # will print 'abcdef' as 'abc' in green and 'def' in blue because the strings are color tagged

"""

class AnsiColorsTool:
    class EnableState(Enum):
        ENABLED = "enabled"
        DISABLED = "disabled"
        AUTO = "auto"

    def __init__(self, enable_state: EnableState = EnableState.AUTO):
        self.enable_state = enable_state
        self.colors = self._get_colors_dict()
        self.key_synonyms = self._get_key_synonyms()

        if (enable_state==AnsiColorsTool.EnableState.DISABLED 
            or (enable_state==AnsiColorsTool.EnableState.AUTO and not sys.stdout.isatty())):
            self.colors = {key: "" for key in self.colors}

    def _get_key_synonyms(self) -> dict[str, str]:
        return {
            "y": "yellow",
            "g": "green",
            "r": "red",
            "b": "blue",
            "c": "cyan",
            "m": "magenta",
            "w": "white",
            "bryellow": "bright_yellow",
            "br_yellow": "bright_yellow",
            "brblue": "bright_blue",
            "br_blue": "bright_blue",
            "brgreen": "bright_green",
            "br_green": "bright_green",
            "brred": "bright_red",
            "br_red": "bright_red",
            "drkyellow": "dark_yellow",
            "drk_yellow": "dark_yellow",
            "drkmagenta": "dark_magenta",
            "drk_magenta": "dark_magenta",
            "drkcyan": "dark_cyan",
            "drk_cyan": "dark_cyan",
            "drkblue": "dark_blue",
            "drk_blue": "dark_blue",
            "bkggreen": "bkg_green",
            "bkgred": "bkg_red",
            "bkgblue": "bkg_blue",
            "bkgwhite": "bkg_white",
        }

    def _get_colors_dict(self) -> dict[str, str]:
        return {
                "yellow":         "\033[93m",
                "bright_yellow":  "\033[93;1m",
                "dark_yellow":    "\033[33m",
                "green":          "\033[92m",
                "bright_green":   "\033[92;1m",
                "dark_green":     "\033[32m",
                "red":            "\033[91m",
                "bright_red":     "\033[91;1m",
                "dark_red":       "\033[31m",
                "blue":           "\033[94m",
                "bright_blue":    "\033[94;1m",
                "dark_blue":      "\033[34m",
                "cyan":           "\033[96m",
                "bright_cyan":    "\033[96;1m",
                "dark_cyan":      "\033[36m",
                "magenta":        "\033[95m",
                "bright_magenta": "\033[95;1m",
                "dark_magenta":   "\033[35m",
                "white":          "\033[97m",
                "bold":           "\033[1m",
                "underline":      "\033[4m",
                "reverse":        "\033[7m",
                "hidden":         "\033[8m",
                "reset":          "\033[0m",
                "bkg_white":      "\033[47m",
                "bkg_green":      "\033[42m",
                "bkg_red":        "\033[41m",
                "bkg_blue":       "\033[44m"
            }

    def __getitem__(self, key: str):
        value = self._resolve_color_key(key)
        return AnsiColorsTool._ColorProxy(self, value)

    def __getattr__(self, name: str):
        # Called only if regular attribute lookup fails; return a callable/str proxy
        value = self._resolve_color_key(name)
        return AnsiColorsTool._ColorProxy(self, value)

    def _resolve_color_key(self, key: str) -> Optional[str]:
        # Exact match first
        lower_key = key.lower()
        if lower_key in self.colors:
            return self.colors[lower_key]
        # Unique prefix match
        matches = [name for name in self.colors.keys() if name.lower().startswith(lower_key)]
        if len(matches) == 1:
            return self.colors[matches[0]]
        # Synonym match
        matches = [name for name in self.key_synonyms.keys() if name.lower().startswith(lower_key)]
        if len(matches) == 1:
            return self.colors[self.key_synonyms[matches[0]]]
        # None or ambiguous
        return None

    class _ColorProxy:
        def __init__(self, owner: "AnsiColorsTool", resolved_color: Optional[str] = None):
            self._owner = owner
            self._resolved_color = resolved_color

        def __getattr__(self, name: str):
            color = self._owner._resolve_color_key(name)
            return AnsiColorsTool._ColorProxy(self._owner, color)

        def __call__(self, string: str, color: Optional[str] = None) -> str:
            chosen = self._resolved_color
            if color is not None:
                chosen = self._owner._resolve_color_key(color)
            if chosen is None:
                return string
            return f"{chosen}{string}{self._owner.colors['reset']}"

        def __str__(self) -> str:
            return self._resolved_color or ""

        def __repr__(self) -> str:
            return f"_ColorProxy({repr(self._resolved_color)})"

        def __format__(self, format_spec: str) -> str:
            return format(str(self), format_spec)

    class ColoredString(str):
        """A string-like object that stores plain text and color spans.
        Color codes are only applied when converting to str/printing.
        """
        def __new__(cls, owner: "AnsiColorsTool", text: str, spans: Optional[list[tuple[int, int, str]]] = None):
            obj = str.__new__(cls, text)
            obj._owner = owner
            obj._spans = spans or []  # list of (start, end, color_code)
            return obj

        # Internal helper to get the underlying plain string value
        def _plain(self) -> str:
            return str.__str__(self)

        def __str__(self) -> str:
            plain = self._plain()
            if not self._spans:
                return plain
            # Build colored output applying spans with resets
            parts: list[str] = []
            pos = 0
            for (start, end, code) in sorted(self._spans, key=lambda s: s[0]):
                # append uncolored gap
                if pos < start:
                    parts.append(plain[pos:start])
                # append colored segment
                segment = plain[start:end]
                if code:
                    parts.append(f"{code}{segment}{self._owner.colors['reset']}")
                else:
                    parts.append(segment)
                pos = end
            # append remaining tail
            if pos < len(plain):
                parts.append(plain[pos:])
            return "".join(parts)

        def __add__(self, other):
            # Concatenate, preserving this color spans and other's spans (if any)
            if isinstance(other, AnsiColorsTool.ColoredString):
                left_text = self._plain()
                right_text = other._plain()
                new_text = left_text + right_text
                offset = len(left_text)
                new_spans = list(self._spans) + [(s+offset, e+offset, c) for (s, e, c) in other._spans]
                return AnsiColorsTool.ColoredString(self._owner, new_text, new_spans)
            else:
                right_text = other
                new_text = self._plain() + right_text
                new_spans = list(self._spans)
                return AnsiColorsTool.ColoredString(self._owner, new_text, new_spans)

        def __radd__(self, other):
            # Support str + ColoredString
            left_text = other
            new_text = left_text + self._plain()
            # Shift existing spans by length of left text
            offset = len(left_text)
            new_spans = [(s+offset, e+offset, c) for (s, e, c) in self._spans]
            return AnsiColorsTool.ColoredString(self._owner, new_text, new_spans)

        def __getitem__(self, key):
            plain = self._plain()
            if isinstance(key, slice):
                sliced_text = plain[key]
                start = key.start or 0
                stop = key.stop if key.stop is not None else len(plain)
                if start < 0:
                    start += len(plain)
                if stop < 0:
                    stop += len(plain)
                start = max(0, start)
                stop = max(start, min(len(plain), stop))
                # Clip spans to slice range and rebase to 0
                new_spans: list[tuple[int, int, str]] = []
                for (s, e, c) in self._spans:
                    cs = max(s, start)
                    ce = min(e, stop)
                    if cs < ce:
                        new_spans.append((cs - start, ce - start, c))
                return AnsiColorsTool.ColoredString(self._owner, sliced_text, new_spans)
            else:
                # Single char
                idx = key
                if idx < 0:
                    idx += len(plain)
                ch = plain[idx]
                # Determine if index lies in any span
                color_code: Optional[str] = None
                for (s, e, c) in self._spans:
                    if s <= idx < e:
                        color_code = c
                        break
                return AnsiColorsTool.ColoredString(self._owner, ch, [(0, 1, color_code)] if color_code is not None else [])

    def colorize_string(self, string: str, color: str) -> "AnsiColorsTool.ColoredString":
        code = self._resolve_color_key(color)
        length = len(string)
        spans = [] if code is None else [(0, length, code)]
        return AnsiColorsTool.ColoredString(self, string, spans)

    def wrap(self) -> "AnsiColorsTool._ColorProxy":
        # Backward compatibility: still allow ansi.wrap.br_green("text")
        return AnsiColorsTool._ColorProxy(self)