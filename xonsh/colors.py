from stat import S_IXUSR
from typing import List
from pathlib import Path
import colorsys


LS_COLORS = (Path.home() / "Config-Files" / "ls-colors.txt").open().read()
""" The contents of the LS_COLORS environment variable """

LS_COLORS_PARSED = dict(
    map(lambda assignment: assignment.split(sep="="), LS_COLORS.split(sep=":"))
)
"""
LS_COLORS parsed into a dictionary where the keys are file types and the values are color codes
"""


class Color:
    """
    A static class containing ANSI escape sequences for various colors and text effects
    """

    DEFAULT = "\033[0m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    UNDERLINED = "\033[4m"
    FLASHING_TEXT = "\033[5m"
    REVERSE_FIELD = "\033[7m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    ORANGE = "\033[33m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    GREY = "\033[37m"
    BLACK = "\033[40m"
    PINK = "\033[1;38;255;34;187m"
    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    LIGHT_MAGENTA = "\033[95m"
    LIGHT_CYAN = "\033[96m"
    LIGHT_WHITE = "\033[97m"


GIT_STATUS_COLORS = {
    "STAGED": Color.LIGHT_GREEN,
    "??": Color.YELLOW,
    "M": Color.BLUE,
    "A": Color.GREEN,
    "D": Color.RED,
    "R": Color.GREEN,
    "C": Color.GREEN,
    "U": Color.RED,
    "DU": Color.RED,
    "AU": Color.RED,
    "UD": Color.RED,
    "UA": Color.RED,
    "DA": Color.RED,
    "AA": Color.RED,
    "UU": Color.RED,
}
""" A dictionary mapping git status codes to colors """


def get_file_color(path: Path) -> str:
    """Returns the color escape sequence for the given file based on LS_COLORS variable

    Args:
        path (Path): The path to the file

    Returns:
        str: The color escape sequence for the given file
    """
    ext = f"*{path.suffix}"

    color = None

    if path.is_file() and ext in LS_COLORS_PARSED:
        color = LS_COLORS_PARSED[ext]

    # If the file is a directory, get the directory color
    if path.is_dir():
        color = LS_COLORS_PARSED.get("di")

    # If the file is a symbolic link, get the link color
    elif path.is_symlink():
        color = LS_COLORS_PARSED.get("ln")

    # If the file is a fifo pipe, get the pipe color
    elif path.exists() and path.is_fifo():
        color = LS_COLORS_PARSED.get("pi")

    # If the file is a socket, get the socket color
    elif path.exists() and path.is_socket():
        color = LS_COLORS_PARSED.get("so")

    # If the file is a block (buffered) special file, get the block color
    elif path.exists() and path.is_block_device():
        color = LS_COLORS_PARSED.get("bd")

    # If the file is a character (unbuffered) special file, get the character color
    elif path.exists() and path.is_char_device():
        color = LS_COLORS_PARSED.get("cd")

    # If the file is a symbolic link and orphaned, get the orphan color
    elif path.is_symlink() and not path.resolve() == path:
        color = LS_COLORS_PARSED.get("or")

    # If the file is a regular file and an executable
    elif path.is_file() and path.stat().st_mode & S_IXUSR:
        color = LS_COLORS_PARSED.get("ex")

    if color is None:
        color = LS_COLORS_PARSED.get("rs")

    return f"\033[{color}m"


def colorize(filename: str, color: str | None = None) -> str:
    """
    Returns the given filename enclosed in the color escape sequence

    Args:
        filename (str): The filename to colorize
        color (str, optional): Color in which the filename will be enclosed.
            If None, the color will be determined based on the file type. Defaults to None.

    Returns:
        str: The colorized filename
    """

    # Return the filename enclosed in the color escape sequence
    # The "\033[0m" sequence at the end resets the color back to the default
    return (
        f"{get_file_color(Path(filename)) if color is None else color}{filename}\033[0m"
    )


class Rainbowizer:
    """
    A class that can be used to colorize text in a rainbow pattern

    Consecutive calls to the rainbowize method will return the same string with each character
    enclosed in a different color escape sequence
    """

    DEFAULT_RAINBOW_RESOLUTION = 256
    """ The default number of colors in the rainbow """

    rainbow_colors: List[str]
    """ A list of colors in the rainbow """

    rainbow_index: int
    """ The index of the current color in the rainbow """

    def __init__(
        self,
        resolution: int = DEFAULT_RAINBOW_RESOLUTION,
        initial_index: int = 0,
    ) -> None:
        """
        Initializes the Rainbowizer object with the given resolution

        Args:
            resolution (int, optional): The number of colors in the rainbow. Defaults to DEFAULT_RAINBOW_RESOLUTION.
        """
        self.rainbow_colors = self.generate_rainbow_colors(resolution)
        self.rainbow_index = initial_index

    def rainbowize(self, string: str) -> str:
        """
        Returns the given string with each character enclosed in a different color escape sequence

        Args:
            string (str): The string to colorize

        Returns:
            str: The colorized string
        """
        result: List[str] = []
        for char in string:
            result.append(
                f"{self.rainbow_colors[self.rainbow_index % len(self.rainbow_colors)]}{char}"
            )
            self.rainbow_index += 1
        return "".join(result)

    @staticmethod
    def generate_rainbow_colors(
        resolution: int,
        *,
        lightness: float = 0.8,
        saturation: float = 1.0,
    ) -> List[str]:
        """
        Generates a list of colors in the rainbow

        Args:
            resolution (int): The number of colors in the rainbow
            lightness (float, optional): How light the colors should be. Defaults to 0.8.
            saturation (float, optional): How saturated the colors should be. Defaults to 1.0.

        Returns:
            List[str]: A list of colors in the rainbow
        """
        colors: List[str] = []
        for i in range(resolution):
            hue = i / resolution
            lightness = 0.8
            saturation = 1.0
            r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
            hex_color = f"\033[38;2;{int(r * 255)};{int(g * 255)};{int(b * 255)}m"
            colors.append(hex_color)
        return colors
