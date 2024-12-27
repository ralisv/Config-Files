# type: ignore
import os
import subprocess
import sys
from getpass import getuser
from pathlib import Path

sys.path.append((Path.home() / ".local" / "share" / "xonsh").as_posix())
from xonsh_utils.colors import (  # pylint: disable=import-error
    LS_COLORS,
    Color,
    Rainbowizer,
    Style,
    colorize_filename,
)
from xonsh_utils.trash import remove
from xonsh_utils.utils import super_git_status

# To silence IDE for further complains about nonexistence of this variable
__xonsh__ = __xonsh__

__xonsh__.env["PATH"].append(str(Path.home() / ".local" / "bin"))
__xonsh__.env["PATH"].append(str(Path.home() / ".dotnet" / "tools"))

# Select between readline and prompt_toolkit
__xonsh__.env["SHELL_TYPE"] = "prompt_toolkit"


# Silence the deprecation warning caused by bug inside of prompt-toolkit library
def filter_warnings() -> None:
    """
    Filters out the deprecation warnings
    """
    import warnings

    warnings.filterwarnings("ignore", category=DeprecationWarning)


filter_warnings()

# Configure xonsh behavior via environment variables
__xonsh__.env["AUTO_CD"] = True
__xonsh__.env["CASE_SENSITIVE_COMPLETIONS"] = False
__xonsh__.env["COMPLETION_IN_THREAD"] = True
__xonsh__.env["COMPLETION_MODE"] = "default"
__xonsh__.env["COMPLETION_QUERY_LIMIT"] = 10
__xonsh__.env["COMPLETIONS_CONFIRM"] = False
__xonsh__.env["COMPLETIONS_MENU_ROWS"] = 2
__xonsh__.env["DYNAMIC_CWD_WIDTH"] = "50%"
__xonsh__.env["DYNAMIC_CWD_ELISION_CHAR"] = "..."
__xonsh__.env["ENABLE_ASYNC_PROMPT"] = True
__xonsh__.env["FOREIGN_ALIASES_SUPPRESS_SKIP_MESSAGE"] = 1
__xonsh__.env["INDENT"] = "   "
__xonsh__.env["MULTILINE_PROMPT"] = " "
__xonsh__.env["SUBSEQUENCE_PATH_COMPLETION"] = True
__xonsh__.env["SUGGEST_COMMANDS"] = True
__xonsh__.env["SUGGEST_MAX_NUM"] = 20
__xonsh__.env["TITLE"] = "Xonsh"
__xonsh__.env["XONSH_AUTOPAIR"] = True
__xonsh__.env["XONSH_CACHE_DIR"] = "~"
__xonsh__.env["XONSH_COLOR_STYLE"] = "paraiso-dark"
__xonsh__.env["XONSH_HISTORY_MATCH_ANYWHERE"] = True
__xonsh__.env["PROMPT_TOOLKIT_COLOR_DEPTH"] = "DEPTH_24_BIT"

__xonsh__.env["BAT_STYLE"] = "grid,changes,header-filename,header-filesize,numbers"


def _s(args):
    git_status = super_git_status()
    if git_status.strip():
        print(git_status)

    subprocess.run(
        ["/usr/bin/env", "lsd", "--color=always", *args],
        env={"LS_COLORS": LS_COLORS, "PATH": os.environ.get("PATH")},
        capture_output=False,
        check=True,
    )


my_aliases = {
    "battery-info": "upower -i /org/freedesktop/UPower/devices/battery_BAT0",
    "cat": "bat",
    "cdi": "zi",  # Interactive zoxide (fzf)
    "cd": "z",  # Use zoxide instead of cd
    "du": "du -h",
    "fc-list": "fc-list --format='%{family}'\n",
    "grep": "grep --color=auto",
    "ls": "lsd --color=auto",
    "pip": "python -m pip",
    "R": "R --no-save -q",
    "rm": remove,
    "rmp": "/usr/bin/env rm",
    "s": _s,
    "sl": "sl -e",
    "stackusage": "colour-valgrind --tool=drd --show-stack-usage=yes",
    "valgrind": "colour-valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all --track-origins=yes --show-reachable=yes --track-fds=yes -s",
    "vlc": "setsid vlc",
    "okular": "setsid okular",
    "nix-shell": "nix-shell --log-format bar-with-logs",
    "home-manager": "home-manager --log-level debug",
}
aliases.update(my_aliases)


# Style the terminal
def set_style() -> None:
    """
    Sets the color style of the terminal
    """
    from xonsh.tools import register_custom_style

    my_style = {
        "Token.Operator": "#fffd00",
        "Token.PTK.CompletionMenu": "#000000",
        "Token.Literal.Number.Integer": "#44ffff",
        "Token.Literal.Number.Float": "#44ffff",
        # Foreground colors
        "BLACK": "#333333",
        "RED": "#ff1111",
        "GREEN": "#11ff11",
        "YELLOW": "#ffff11",
        "BLUE": "#1111ff",
        "MAGENTA": "#ff11ff",
        "CYAN": "#11ccff",
        "WHITE": "#eeeeee",
        "INTENSE_BLACK": "#222222",
        "INTENSE_RED": "#ff0000",
        "INTENSE_GREEN": "#00ff00",
        "INTENSE_YELLOW": "#ffff00",
        "INTENSE_BLUE": "#0000ff",
        "INTENSE_MAGENTA": "#ff00ff",
        "INTENSE_CYAN": "#00ddff",
        "INTENSE_WHITE": "#ffffff",
        # Background colors
        "BACKGROUND_BLACK": "#111111",
        "BACKGROUND_RED": "#ff1111",
        "BACKGROUND_GREEN": "#11ff11",
        "BACKGROUND_YELLOW": "#ffff11",
        "BACKGROUND_BLUE": "#1111ff",
        "BACKGROUND_MAGENTA": "#ff11ff",
        "BACKGROUND_CYAN": "#11ccff",
        "BACKGROUND_WHITE": "#eeeeee",
        "BACKGROUND_INTENSE_BLACK": "#000000",
        "BACKGROUND_INTENSE_RED": "#ff0000",
        "BACKGROUND_INTENSE_GREEN": "#00ff00",
        "BACKGROUND_INTENSE_YELLOW": "#ffff00",
        "BACKGROUND_INTENSE_BLUE": "#0000ff",
        "BACKGROUND_INTENSE_MAGENTA": "#ff00ff",
        "BACKGROUND_INTENSE_CYAN": "#00ddff",
        "BACKGROUND_INTENSE_WHITE": "#ffffff",
    }

    register_custom_style("my_style", my_style, base="paraiso-dark")
    __xonsh__.env["XONSH_COLOR_STYLE"] = "my_style"


set_style()


def customize_autocompleter() -> None:
    """
    Customize the autocompleter
    """
    import prompt_toolkit.styles.defaults as defstyle

    defstyle.PROMPT_TOOLKIT_STYLE.append(("bottom-toolbar", "noreverse"))
    defstyle.PROMPT_TOOLKIT_STYLE.append(("completion-menu", "bg:#771977 #000000"))


customize_autocompleter()

__xonsh__.env["LS_COLORS"] = LS_COLORS
__xonsh__.env["EZA_COLORS"] = LS_COLORS


class XonshPrompt:
    """
    A class that encapsulates the logic for customizing the xonsh prompt

    Assign a dye parameter a function that takes a string and returns a colored string to
    dye prompt in your favourite colors
    """

    rainbowizer = Rainbowizer(512, 425, lightness=0.55)

    dye = rainbowizer.rainbowize

    @staticmethod
    def enclose_in_brackets(text: str) -> str:
        """
        Encloses the text in brackets

        Args:
            text (str): The text to be enclosed

        Returns:
            str: The enclosed text
        """
        return f"{XonshPrompt.dye('[')}{text}{XonshPrompt.dye(']')}{Style.DEFAULT}"

    @staticmethod
    def git_info() -> str:
        try:
            return XonshPrompt.git_info_raw()
        except Exception:
            return ""

    @staticmethod
    def git_info_raw() -> str:
        """s
        Returns the information about the git repository in the current directory

        Returns:
            str: Branch name colored according to the state of the repository or empty string if not in git repository
        """
        # Check if the current directory is a git repository
        git_rev_parse = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
        )
        if git_rev_parse.returncode != 0:
            return ""

        # Get the name of the current branch
        git_branch = subprocess.run(
            ["git", "branch", "--show-current"], capture_output=True, text=True
        )
        branch = git_branch.stdout.strip()

        # Check if the repository is dirty (has uncommitted changes)
        git_status = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True
        )
        is_dirty = bool(git_status.stdout)

        # Determine the color based on the state of the repository
        color = Color.SALMON if is_dirty else Color.LIME_GREEN

        # Assuming XonshPrompt.enclose_in_brackets and Color are defined elsewhere
        return XonshPrompt.enclose_in_brackets(f"{color}{branch}")

    @staticmethod
    def path_info() -> str:
        """
        Returns the information about the current working directory

        Returns:
            str: The current working directory colored based on LS_COLORS
        """
        return XonshPrompt.enclose_in_brackets(
            f"{colorize_filename(str(Path.cwd())).replace(str(Path.home()), '~')}"
        )

    @staticmethod
    def last_exit_code_info() -> str:
        """
        Returns the information about the last exit code

        Returns:
            str: The last exit code colored red if not zero or empty string if zero
        """
        exit_code = __xonsh__.env["LAST_RETURN_CODE"]
        return (
            XonshPrompt.enclose_in_brackets(f"{Color.RED}{exit_code}")
            if exit_code != 0
            else ""
        )

    @staticmethod
    def reset() -> str:
        """
        Returns the reset color

        Returns:
            str: The reset color
        """
        # If the deprecation warnings about event loop appear ever again, uncomment the following line
        # warnings.filterwarnings("ignore", category=DeprecationWarning)
        return Style.DEFAULT


__xonsh__.env["PROMPT_FIELDS"]["git-info"] = XonshPrompt.git_info
__xonsh__.env["PROMPT_FIELDS"]["last-exit-code-info"] = XonshPrompt.last_exit_code_info
__xonsh__.env["PROMPT_FIELDS"]["path-info"] = XonshPrompt.path_info
__xonsh__.env["PROMPT_FIELDS"]["reset"] = XonshPrompt.reset
__xonsh__.env["PROMPT_FIELDS"]["rainbow-user"] = lambda: XonshPrompt.dye(getuser())
__xonsh__.env["PROMPT_FIELDS"]["end"] = lambda: XonshPrompt.dye("\n λ ")
__xonsh__.env["PROMPT_FIELDS"]["separator"] = lambda: XonshPrompt.dye(".")

__xonsh__.env["PROMPT"] = (
    "{rainbow-user}{separator}{path-info}{git-info}{last-exit-code-info}{end}{reset}"
)


# Colorful manpages if using less as MANPAGER
__xonsh__.env["LESS_TERMCAP_mb"] = "\033[1;32m"
__xonsh__.env["LESS_TERMCAP_md"] = "\033[38;2;255;180;50m"
__xonsh__.env["LESS_TERMCAP_me"] = "\033[0m"
__xonsh__.env["LESS_TERMCAP_se"] = "\033[0m"
__xonsh__.env["LESS_TERMCAP_so"] = "\033[38;2;255;255;50m"
__xonsh__.env["LESS_TERMCAP_ue"] = "\033[0m"
__xonsh__.env["LESS_TERMCAP_us"] = "\033[38;2;255;100;50m"

# Use bat as manpager
__xonsh__.env["MANPAGER"] = "sh -c 'col -bx | bat -l man --plain'"

# Option passed to man's formatter, removes undesiColor.RED characters from output
__xonsh__.env["MANROFFOPT"] = "-c"

# Ask about dumping trash
# ask_whether_to_dump()

# Setup zoxide
execx(
    subprocess.run(
        ["zoxide", "init", "xonsh"], capture_output=True, text=True, check=True
    ).stdout,
    "exec",
    __xonsh__.ctx,
    filename="zoxide",
)
