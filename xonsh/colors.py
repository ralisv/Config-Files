import os
import stat


LS_COLORS = open(f"{os.path.expanduser('~')}/Config-Files/ls-colors.txt").read()
""" The contents of the LS_COLORS environment variable """

LS_COLORS_PARSED = dict(
    map(lambda assignment: assignment.split(sep="="), LS_COLORS.split(sep=":"))
)
""" LS_COLORS parsed into a dictionary where the keys are file types and the values are color codes """


def get_file_color(path: str) -> str:
    _, ext = os.path.splitext(path)
    ext = f"*{ext}"

    color = None

    if os.path.isfile(path) and ext in LS_COLORS_PARSED:
        color = LS_COLORS_PARSED[ext]

    # If the file is a directory, get the directory color
    elif os.path.isdir(path):
        color = LS_COLORS_PARSED.get("di")

    # If the file is a symbolic link, get the link color
    elif os.path.islink(path):
        color = LS_COLORS_PARSED.get("ln")

    # If the file is a fifo pipe, get the pipe color
    elif os.path.exists(path) and stat.S_ISFIFO(os.stat(path).st_mode):
        color = LS_COLORS_PARSED.get("pi")

    # If the file is a socket, get the socket color
    elif os.path.exists(path) and stat.S_ISSOCK(os.stat(path).st_mode):
        color = LS_COLORS_PARSED.get("so")

    # If the file is a block (buffered) special file, get the block color
    elif os.path.exists(path) and stat.S_ISBLK(os.stat(path).st_mode):
        color = LS_COLORS_PARSED.get("bd")

    # If the file is a character (unbuffered) special file, get the character color
    elif os.path.exists(path) and stat.S_ISCHR(os.stat(path).st_mode):
        color = LS_COLORS_PARSED.get("cd")

    # If the file is a symbolic link and orphaned, get the orphan color
    elif os.path.islink(path) and not os.path.exists(os.readlink(path)):
        color = LS_COLORS_PARSED.get("or")

    # If the file is a regular file and an executable
    elif os.path.isfile(path) and os.access(path, os.X_OK):
        color = LS_COLORS_PARSED.get("ex")

    if color is None:
        color = LS_COLORS_PARSED.get("rs")

    # Return the filename enclosed in the color escape sequence
    # The "\033[0m" sequence at the end resets the color back to the default
    return f"\033[{color}m"


def colorize(filename: str, color: str = "") -> str:
    """
    Returns the filename enclosed in the color escape sequence based on LS_COLORS
    It is required that at least rs (reset) color is defined in LS_COLORS, as it is
    used as a fallback when color for the file type is not defined
    """

    # Return the filename enclosed in the color escape sequence
    # The "\033[0m" sequence at the end resets the color back to the default
    return f"{get_file_color(filename) if not color else color}{filename}\033[0m"
