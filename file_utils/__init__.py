"""File system utilities"""

# can be imported as part of the pyutils package or just as directory imports, so we handle both cases
try:
    from utils.file_utils.fs_utils import find_path_by_leaf # type: ignore
    from utils.file_utils.repo_utils import get_git_repo_root # type: ignore
    from utils.file_utils.hex_file_utils import read_hex_file, read_hex_file_as_ints # type: ignore
except ModuleNotFoundError:
    from .fs_utils import find_path_by_leaf # type: ignore
    from .repo_utils import get_git_repo_root # type: ignore
    from .hex_file_utils import read_hex_file, read_hex_file_as_ints # type: ignore

__all__ = ["find_path_by_leaf", "get_git_repo_root", "read_hex_file", "read_hex_file_as_ints"]