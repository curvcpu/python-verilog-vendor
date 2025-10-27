"""ANSI color utilities"""

# can be imported as part of the utils package or just as directory imports, so we handle both cases
try:
    from utils.colors.ansi import AnsiColorsTool
except ModuleNotFoundError:
    from .ansi import AnsiColorsTool

__all__ = ["AnsiColorsTool"]
