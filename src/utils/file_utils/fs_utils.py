import os

def find_path_by_leaf(root_dir: str, leaf_path: str) -> str|None:
    """
    Recursively traverses through the directory tree from a given
    root directory until it finds a given partial terminal path
    e.g., `generated/current/.curv.env`.  

    Args:
        root_dir: the root directory to start the traversal from.
        leaf_path: the partial path to the leaf to find, e.g., `generated/current/.curv.env`.
    
    Returns:
    The returned path is the full path to the leaf. None if the path is not found.
    """

    if not root_dir or not leaf_path:
        return None

    # If an absolute path was provided and it exists, return it directly.
    if os.path.isabs(leaf_path) and os.path.exists(leaf_path):
        return os.path.abspath(leaf_path)

    # Normalize the partial leaf path (strip any leading separators).
    rel_leaf = leaf_path.lstrip(os.sep)

    # Quick check: does the path exist directly under the given root?
    direct_candidate = os.path.join(root_dir, rel_leaf)
    if os.path.exists(direct_candidate):
        return os.path.abspath(direct_candidate)

    # Traversal: for each directory, check if joining the partial path exists.
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        candidate = os.path.join(dirpath, rel_leaf)
        if os.path.exists(candidate):
            return os.path.abspath(candidate)

    return None
