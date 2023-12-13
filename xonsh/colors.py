import colorsys
from enum import Enum
from pathlib import Path
from stat import S_IXUSR
from typing import List

LS_COLORS = (Path.home() / "Config-Files" / "ls-colors.txt").open().read()
""" The contents of the LS_COLORS environment variable """

LS_COLORS_PARSED = dict(
    map(lambda assignment: assignment.split(sep="="), LS_COLORS.split(sep=":"))
)
"""
LS_COLORS parsed into a dictionary where the keys are file types and the values are color codes
"""


class Style(Enum):
    """
    An enumeration of text styles
    """

    NORMAL = 0
    BOLD = 1
    UNDERLINED = 4
    FLASHING_TEXT = 5
    REVERSE_FIELD = 7


class Color:
    """
    A static class containing ANSI escape sequences for various colors and text effects
    """

    @staticmethod
    def bit24(red: int, green: int, blue: int, /, style: Style = Style.NORMAL) -> str:
        """
        Returns the ANSI escape sequence for the given 24-bit color and text style

        Args:
            r (int): Red component of the color
            g (int): Green component of the color
            b (int): Blue component of the color
            style (Style): Text style

        Returns:
            str: The ANSI escape sequence for the given 24-bit color and text style
        """
        return f"\033[{style.value};38;2;{red};{green};{blue}m"

    AMBER = bit24(255, 191, 0)
    AQUA = bit24(0, 255, 255)
    ARCTIC_BLUE = bit24(138, 180, 248)
    ASH = bit24(178, 190, 181)
    AZURE = bit24(0, 127, 255)
    BEIGE = bit24(245, 245, 220)
    BLACK = bit24(0, 0, 0)
    BRONZE = bit24(205, 127, 50)
    BROWN = bit24(165, 42, 42)
    BRUNETTE = bit24(101, 67, 33)
    BURGUNDY = bit24(128, 0, 32)
    CHARCOAL = bit24(54, 69, 79)
    CHERRY_RED = bit24(247, 50, 50)
    COFFEE_BROWN = bit24(111, 78, 55)
    CORAL = bit24(255, 127, 80)
    CREAM = bit24(255, 253, 208)
    CRIMSON = bit24(220, 20, 60)
    CYAN = bit24(0, 255, 255)
    DARK_GREEN = bit24(0, 100, 0)
    DEFAULT = "\033[0m"
    EMERALD = bit24(80, 200, 120)
    FUCHSIA = bit24(255, 0, 255)
    GARNET = bit24(165, 11, 94)
    GRAPE_VINE = bit24(111, 45, 168)
    GREEN = bit24(0, 128, 0)
    GREY = bit24(128, 128, 128)
    INDIGO = bit24(75, 0, 130)
    IVORY = bit24(255, 255, 240)
    JET_BLACK = bit24(52, 52, 52)
    LAVENDER = bit24(230, 230, 250)
    LEMON_YELLOW = bit24(255, 250, 205)
    LILAC = bit24(200, 162, 200)
    LIME_GREEN = bit24(50, 205, 50)
    MAGENTA = bit24(255, 0, 255)
    MAROON = bit24(128, 0, 0)
    MAUVE = bit24(224, 176, 255)
    MINT = bit24(170, 240, 209)
    MOCHA = bit24(192, 141, 111)
    MUSTARD = bit24(227, 179, 50)
    NAVY_BLUE = bit24(0, 0, 128)
    OLIVE = bit24(128, 128, 0)
    ORANGE = bit24(255, 165, 0)
    PEACH = bit24(255, 218, 185)
    PEARL = bit24(234, 224, 200)
    PINK = bit24(255, 0, 255)
    PISTA_GREEN = bit24(136, 200, 162)
    PURPLE = bit24(128, 0, 128)
    RED = bit24(255, 0, 0)
    ROSEWOOD = bit24(101, 0, 11)
    RUBY = bit24(224, 17, 95)
    RUST = bit24(183, 65, 14)
    SAFFRON = bit24(244, 196, 48)
    SALMON = bit24(250, 128, 114)
    SAPPHIRE = bit24(15, 82, 186)
    SEA_GREEN = bit24(46, 139, 87)
    SILVER = bit24(192, 192, 192)
    SKY_BLUE = bit24(135, 206, 235)
    TAN = bit24(210, 180, 140)
    TANGERINE = bit24(255, 140, 0)
    TEAL = bit24(0, 128, 128)
    TURQUOISE = bit24(64, 224, 208)
    UMBER = bit24(99, 81, 71)
    VIOLET = bit24(238, 130, 238)
    WHITE = bit24(255, 255, 255)
    YELLOW = bit24(255, 255, 0)


GIT_STATUS_COLORS = {
    "??": Color.YELLOW,
    "M": Color.ARCTIC_BLUE,
    "A": Color.GREEN,
    "D": Color.RED,
    "R": Color.ORANGE,
    "C": Color.PURPLE,
    "U": Color.MAROON,
    "DU": Color.CORAL,
    "AU": Color.SAFFRON,
    "UD": Color.BROWN,
    "UA": Color.TEAL,
    "DA": Color.TURQUOISE,
    "AA": Color.LAVENDER,
    "UU": Color.GRAPE_VINE,
}
""" A dictionary mapping git status codes to colors """

GIT_STATUS_COLORS_STAGED = {
    "??": Color.LEMON_YELLOW,
    "M": Color.SKY_BLUE,
    "MM": Color.VIOLET,
    "A": Color.LIME_GREEN,
    "D": Color.SALMON,
    "R": Color.ORANGE,
    "C": Color.PEACH,
    "U": Color.PINK,
    "DU": Color.CORAL,
    "AU": Color.SAFFRON,
    "UD": Color.TAN,
    "UA": Color.AQUA,
    "DA": Color.TURQUOISE,
    "AA": Color.VIOLET,
    "UU": Color.LAVENDER,
}
""" A dictionary mapping git status codes to colors for staged files """


def get_file_color(path: Path) -> str:
    """
    Returns the color escape sequence for the given file based on LS_COLORS variable

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

    # If the file is a character (unbuffered) special file, get the character
    # color
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
