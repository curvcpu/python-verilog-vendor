import sys
import math
import resource
from typing import Tuple, Union

Num = Union[int, float]

def _norm(v: int) -> Num:
    return math.inf if v == resource.RLIM_INFINITY else v

def raise_recursion_limit(limit: int = 10_000) -> int:
    """
    Try to raise Python's recursion limit, returning the new limit.
    Returns:
        int: The previous recursion limit
    """
    sys.setrecursionlimit(limit)  # default is ~1000
    return sys.getrecursionlimit()

def get_recursion_limit() -> int:
    """
    Get the current Python recursion limit.
    Returns:
        int: The current recursion limit
    """
    return sys.getrecursionlimit()

def raise_stack_limit(limit: int = 512 * 1024 * 1024) -> Tuple[Num, Num]:
    """
    Try to raise the C library's stack limit, returning the new limit.
    Returns:
        The new soft and hard stack limits
    """
    _soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    new_soft = limit if hard == resource.RLIM_INFINITY else min(limit, hard)
    resource.setrlimit(resource.RLIMIT_STACK, (new_soft, hard))
    s2, h2 = resource.getrlimit(resource.RLIMIT_STACK)
    return _norm(s2), _norm(h2)

def get_stack_limit() -> Tuple[Num, Num]:
    """
    Get the current C library stack limit.
    Returns:
        The current soft and hard stack limits
    """
    soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    return _norm(soft), _norm(hard)

def get_max_memory_kb() -> int:
    """
    Get the maximum memory usage of the current process.
    Returns:
        int: The maximum memory usage in kilobytes
    """
    ru = resource.getrusage(resource.RUSAGE_SELF)
    n = ru.ru_maxrss
    if sys.platform.startswith("linux"):
        return n                  # kb
    elif sys.platform == "darwin":
        return n / 1024           # in bytes
    else:
        return n / 1024           # most BSDs report kB