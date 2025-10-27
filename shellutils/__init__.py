"""Shell utilities"""

# can be imported as part of the pyutils package or just as directory imports, so we handle both cases
try:
    from utils.shellutils.which import Which
    from utils.shellutils.delta import print_delta
    from utils.shellutils.console import get_console_width, get_console_height
except ModuleNotFoundError:
    from .which import Which
    from .delta import print_delta
    from .console import get_console_width, get_console_height

__all__ = [
    "Which", 
    "print_delta", 
    "get_console_width", 
    "get_console_height"
]