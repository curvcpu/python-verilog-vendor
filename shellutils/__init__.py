"""Shell utilities"""

# can be imported as part of the utils package or just as directory imports, so we handle both cases
try:
    from utils.shellutils.which import Which
except ModuleNotFoundError:
    from .which import Which

__all__ = ["Which"]