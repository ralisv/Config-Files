import colorsys
from dataclasses import dataclass
from pathlib import Path
from stat import S_IXUSR

LS_COLORS_DIRECTORY = Path.home() / ".config" / "ls-colors"
LS_COLORS = (LS_COLORS_DIRECTORY / "ls-colors.txt").open().read()
""" The contents of the LS_COLORS environment variable """

LS_COLORS_PARSED = dict(
    map(lambda assignment: assignment.split(sep="="), LS_COLORS.split(sep=":"))
)
"""
LS_COLORS parsed into a dictionary where the keys are file types and the values are color codes
"""


class Style:
    """
    An enumeration of text styles using ANSI escape sequences.

    The usage can be as follows:
    print(f"{Style.BOLD}Hello, world!{Style.DEFAULT}")
    """

    DEFAULT = "\033[0m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    SLOW_BLINK = "\033[5m"
    RAPID_BLINK = "\033[6m"
    REVERSE = "\033[7m"
    CONCEAL = "\033[8m"
    STRIKE_THROUGH = "\033[9m"


@dataclass(frozen=True)
class AnsiColorCode:
    """
    A class representing an ANSI color code
    """

    rgb_red: int
    rgb_green: int
    rgb_blue: int
    bg: bool = False

    def __str__(self) -> str:
        return f"\033[{48 if self.bg else 38};2;{self.rgb_red};{self.rgb_green};{self.rgb_blue}m"

    @property
    def background(self) -> "AnsiColorCode":
        return AnsiColorCode(self.rgb_red, self.rgb_green, self.rgb_blue, True)

    def wrap(self, string: str) -> str:
        return f"{self}{string}{Style.DEFAULT}"


class Color:
    """
    A static class containing ANSI escape sequences for various colors and text effects

    Recommended usage is to wrap colors provided by this class inside f strings like this:
    print(f"{Color.RED}Hello, world!{Style.DEFAULT}")
    """

    AMBER = AnsiColorCode(255, 191, 0)
    AQUA = AnsiColorCode(0, 255, 255)
    ARCTIC_BLUE = AnsiColorCode(138, 180, 248)
    ASH = AnsiColorCode(178, 190, 181)
    AZURE = AnsiColorCode(0, 127, 255)
    BEIGE = AnsiColorCode(245, 245, 220)
    BLACK = AnsiColorCode(0, 0, 0)
    BRONZE = AnsiColorCode(205, 127, 50)
    BROWN = AnsiColorCode(165, 42, 42)
    BRUNETTE = AnsiColorCode(101, 67, 33)
    BURGUNDY = AnsiColorCode(128, 0, 32)
    CHARCOAL = AnsiColorCode(54, 69, 79)
    CHERRY_RED = AnsiColorCode(247, 50, 50)
    COFFEE_BROWN = AnsiColorCode(111, 78, 55)
    CORAL = AnsiColorCode(255, 127, 80)
    CREAM = AnsiColorCode(255, 253, 208)
    CRIMSON = AnsiColorCode(220, 20, 60)
    CYAN = AnsiColorCode(0, 255, 255)
    DARK_GREEN = AnsiColorCode(0, 100, 0)
    EMERALD = AnsiColorCode(80, 200, 120)
    FUCHSIA = AnsiColorCode(255, 0, 255)
    GARNET = AnsiColorCode(165, 11, 94)
    GRAPE_VINE = AnsiColorCode(111, 45, 168)
    GREEN = AnsiColorCode(0, 128, 0)
    GREY = AnsiColorCode(128, 128, 128)
    INDIGO = AnsiColorCode(75, 0, 130)
    IVORY = AnsiColorCode(255, 255, 240)
    JET_BLACK = AnsiColorCode(52, 52, 52)
    LAVENDER = AnsiColorCode(230, 230, 250)
    LEMON_YELLOW = AnsiColorCode(255, 250, 205)
    LILAC = AnsiColorCode(200, 162, 200)
    LIME_GREEN = AnsiColorCode(50, 205, 50)
    MAGENTA = AnsiColorCode(255, 0, 255)
    MAROON = AnsiColorCode(128, 0, 0)
    MAUVE = AnsiColorCode(224, 176, 255)
    MINT = AnsiColorCode(170, 240, 209)
    MOCHA = AnsiColorCode(192, 141, 111)
    MUSTARD = AnsiColorCode(227, 179, 50)
    NAVY_BLUE = AnsiColorCode(0, 0, 128)
    OLIVE = AnsiColorCode(128, 128, 0)
    ORANGE = AnsiColorCode(255, 165, 0)
    PEACH = AnsiColorCode(255, 218, 185)
    PEARL = AnsiColorCode(234, 224, 200)
    PINK = AnsiColorCode(255, 0, 255)
    PISTA_GREEN = AnsiColorCode(136, 200, 162)
    PURPLE = AnsiColorCode(128, 0, 128)
    RED = AnsiColorCode(255, 0, 0)
    ROSEWOOD = AnsiColorCode(101, 0, 11)
    RUBY = AnsiColorCode(224, 17, 95)
    RUST = AnsiColorCode(183, 65, 14)
    SAFFRON = AnsiColorCode(244, 196, 48)
    SALMON = AnsiColorCode(250, 128, 114)
    SAPPHIRE = AnsiColorCode(15, 82, 186)
    SEA_GREEN = AnsiColorCode(46, 139, 87)
    SILVER = AnsiColorCode(192, 192, 192)
    SKY_BLUE = AnsiColorCode(135, 206, 235)
    TAN = AnsiColorCode(210, 180, 140)
    TANGERINE = AnsiColorCode(255, 140, 0)
    TEAL = AnsiColorCode(0, 128, 128)
    TURQUOISE = AnsiColorCode(64, 224, 208)
    UMBER = AnsiColorCode(99, 81, 71)
    VIOLET = AnsiColorCode(238, 130, 238)
    WHITE = AnsiColorCode(255, 255, 255)
    YELLOW = AnsiColorCode(255, 255, 0)

    def __iter__(self):
        """Iterates through all known colors"""
        return self.__class__.__dict__.values().__iter__()


GIT_STATUS_COLORS = {
    "??": Color.YELLOW,
    "M": Color.AZURE,
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
    "AD": Color.MAGENTA,
}
""" A dictionary mapping git status codes to colors """

GIT_STATUS_COLORS_STAGED = {
    "??": Color.LEMON_YELLOW,
    "M": Color.AQUA,
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
    "AD": Color.RUST,
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


def colorize_filename(filename: str, color: AnsiColorCode | None = None) -> str:
    """
    Returns the given filename enclosed in the color escape sequence

    Args:
        filename (str): The filename to colorize
        color (str, optional): Color in which the filename will be enclosed.
            If None, the color will be determined based on the file type. Defaults to None.

    Returns:
        str: The colorized filename
    """
    return f"{get_file_color(Path(filename)) if color is None else color}{filename}{Style.DEFAULT}"


class Rainbowizer:
    """
    A class that can be used to colorize text in a rainbow pattern

    Consecutive calls to the rainbowize method will return the same string with each character
    enclosed in a different color escape sequence

    The class also implements iterator that yields AnsiCodes in a cycle indefinitely
    """

    DEFAULT_RAINBOW_RESOLUTION = 256
    """ The default number of colors in the rainbow """

    rainbow_colors: list[AnsiColorCode]
    """ A list of colors in the rainbow """

    rainbow_index: int
    """ The index of the current color in the rainbow """

    def __init__(
        self,
        resolution: int = DEFAULT_RAINBOW_RESOLUTION,
        initial_index: int = 0,
        lightness: float = 0.5,
        saturation: float = 0.85,
    ) -> None:
        """
        Initializes the Rainbowizer object with the given resolution

        Args:
            resolution (int, optional): The number of colors in the rainbow. Defaults to DEFAULT_RAINBOW_RESOLUTION.
            initial_index (int, optional): The index of the initial color in the rainbow. Defaults to 0.
            lightness (float, optional): How light the colors should be. Defaults to 0.5.
            saturation (float, optional): How saturated the colors should be. Defaults to 0.85.
        """
        self.rainbow_colors = Rainbowizer.generate_rainbow_colors(
            resolution, lightness, saturation
        )
        self.rainbow_index = initial_index

    def rainbowize(self, string: str) -> str:
        """
        Returns the given string with each character enclosed in a different color escape sequence

        Args:
            string (str): The string to colorize

        Returns:
            str: The colorized string
        """
        result: list[str] = []
        for char, color in zip(string, self):
            result.append(color.wrap(char))

        return "".join(result)

    @staticmethod
    def generate_rainbow_colors(
        resolution: int,
        lightness: float,
        saturation: float,
    ) -> list[AnsiColorCode]:
        """
        Generates a list of colors in the rainbow

        Args:
            resolution (int): The number of colors in the rainbow
            lightness (float, optional): How light the colors should be. Defaults to 0.8.
            saturation (float, optional): How saturated the colors should be. Defaults to 1.0.

        Returns:
            list[str]: A list of colors in the rainbow
        """
        colors: list[AnsiColorCode] = []
        for i in range(resolution):
            hue = i / resolution

            r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
            hex_color = AnsiColorCode(int(r * 255), int(g * 255), int(b * 255))
            colors.append(hex_color)
        return colors

    def __iter__(self):
        return self

    def __next__(self) -> AnsiColorCode:
        next_color = self.rainbow_colors[self.rainbow_index % len(self.rainbow_colors)]
        self.rainbow_index += 1
        return next_color
