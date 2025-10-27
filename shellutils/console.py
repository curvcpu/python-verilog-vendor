import shutil

import os, sys, shutil

def _tty_width_height() -> tuple[int, int]:
    """
    Get the width and height of the console. If the console is not a terminal,
    return the fallback width and height.

    Returns:
        A tuple of the width and height of the console.  On failure, returns 80x24.
    """

    # 1) real TTY on any std stream
    for s in (sys.stdout, sys.stderr, sys.stdin):
        try:
            if s.isatty():
                return os.get_terminal_size(s.fileno()).columns, os.get_terminal_size(s.fileno()).lines
        except (OSError, ValueError, AttributeError):
            pass

    # 2) controlling TTY directly (POSIX)
    try:
        import fcntl, termios, struct
        with open("/dev/tty") as t:
            rows, cols, *_ = struct.unpack("hhhh", fcntl.ioctl(t, termios.TIOCGWINSZ, b"\0"*8))
            if cols:
                return rows,cols
    except Exception:
        pass

    # 3) last resort (does NOT trust env vars)
    return shutil.get_terminal_size(fallback=(80, 24)).columns, shutil.get_terminal_size(fallback=(80, 24)).lines

def get_console_width() -> int:
    print(f"get_console_width: {_tty_width_height()[0]}")
    return _tty_width_height()[0]

def get_console_height() -> int:
    return _tty_width_height()[1]