import os
import subprocess
from typing import Optional
from pathlib import Path

def get_git_repo_root(cwd: Optional[str] = os.getcwd()) -> Optional[str]:
    """
    Returns the absolute path to the root of the git repository we are in, 
    or None if this dir is not in a git repo.
    """
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        check=True,
        capture_output=True,
        cwd=cwd
    )
    exit_code = result.returncode
    if exit_code != 0:
        return None
    else:
        return result.stdout.strip()

def is_path_writeable(path: str | Path) -> bool:
    """
    Check if a file path is writeable.
    
    Parameters:
    -----------
    path : str
        Abs or relative path to the file path to check
        
    Returns:
    --------
    bool
        True if the file path is writeable, False otherwise
    """
    try:
        # Check if the directory exists
        directory = os.path.dirname(path)
        if directory == '':
            directory = '.'  # Current directory
        
        if not os.path.exists(directory) or not os.path.isdir(directory):
            return False
    except (IOError, PermissionError):
        return False
    return True

# make relative-to-repo-root paths into absolute paths
def make_repo_root_relpath_into_abs(rel_to_repo_root_path:str | Path, repo_root_abspath: Optional[str] = get_git_repo_root()) -> str:
    if os.path.isabs(rel_to_repo_root_path) or repo_root_abspath is None:
        # just absolutize the path we were given if it's already absolute or we don't have a repo root
        return str(Path(rel_to_repo_root_path).absolute())
    else:
        return str((Path(repo_root_abspath) / rel_to_repo_root_path).absolute())
