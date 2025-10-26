"""Unit tests for system module."""

from utils.system import (   # type: ignore
    get_nprocs, 
    get_max_memory_kb, 
    raise_recursion_limit, 
    get_recursion_limit, 
    get_stack_limit,
    raise_stack_limit
 )
import sys
import math
import resource
from typing import Tuple, Union

Num = Union[int, float]

class TestSystem:
    """Tests for the system module."""

    def test_get_nprocs(self):
        """Test that get_nprocs returns the number of effective CPUs."""
        nprocs = get_nprocs()
        assert nprocs > 0

    def test_get_max_memory_kb(self):
        """Test that get_max_memory_kb returns the maximum memory usage in kilobytes."""
        max_memory_kb = get_max_memory_kb()
        assert max_memory_kb > 0

    def test_raise_recursion_limit(self):
        """Test that set_recursion_limit returns the new recursion limit."""
        recursion_limit = raise_recursion_limit(10_000)
        assert recursion_limit > 1000

    def test_raise_stack_limit(self):
        """Test that set_stack_limit returns the new stack limit."""
        stack_limit = raise_stack_limit(512*1024*1024)
        assert stack_limit[0] > 0
        assert stack_limit[1] > stack_limit[0]

    def test_get_recursion_limit(self):
        """Test that get_recursion_limit returns the current recursion limit."""
        recursion_limit = get_recursion_limit()
        assert recursion_limit > 1000

    def test_get_stack_limit(self):
        """Test that get_stack_limit returns the current stack limit."""
        stack_limit = get_stack_limit()
        assert stack_limit[0] > 0
        assert stack_limit[1] > stack_limit[0]