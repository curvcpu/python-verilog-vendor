"""ANSI color utilities"""

# can be imported as part of the pyutils package or just as directory imports, so we handle both cases
try:
    from utils.colors.ansi import AnsiColorsTool # type: ignore
except ModuleNotFoundError:
    from .ansi import AnsiColorsTool # type: ignore

__all__ = ["AnsiColorsTool"]
