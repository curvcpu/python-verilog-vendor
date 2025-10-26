"""System utilities"""

# can be imported as part of the pyutils package or just as directory imports, so we handle both cases
try:
    from utils.system.nprocs import get_nprocs
except ModuleNotFoundError:
    from .nprocs import get_nprocs
try:
    from utils.system.ulimits import (
        get_max_memory_kb,
        raise_recursion_limit,
        get_recursion_limit,
        get_stack_limit,
        raise_stack_limit
    )
except ModuleNotFoundError:
    from .ulimits import ( 
        get_max_memory_kb, 
        raise_recursion_limit,
        get_recursion_limit, 
        get_stack_limit, 
        raise_stack_limit
    ) 

__all__ = [
    "get_nprocs", 
    "get_max_memory_kb", 
    "raise_recursion_limit", 
    "get_recursion_limit", 
    "get_stack_limit", 
    "raise_stack_limit"
]