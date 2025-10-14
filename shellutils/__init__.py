"""Shell utilities"""

# can be imported as part of the pyutils package or just as directory imports, so we handle both cases
try:
    from utils.shellutils.which import Which # type: ignore
except ModuleNotFoundError:
    from .which import Which # type: ignore

__all__ = ["Which"]