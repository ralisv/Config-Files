# type: ignore
import os
import subprocess
import sys
from getpass import getuser
from pathlib import Path

sys.path.append((Path.home() / ".local" / "share" / "xonsh").as_posix())

from xonsh_utils.colors import (  # pylint: disable=import-error,import-outside-toplevel
    LS_COLORS,
    Color,
    Rainbowizer,
    Style,
    colorize_filename,
)
from xonsh_utils.trash import remove
from xonsh_utils.utils import super_git_status

env = __xonsh__.env  # pylint: disable=undefined-variable

# Configure xonsh behavior via environment variables
env["SHELL_TYPE"] = "prompt_toolkit"
env["AUTO_CD"] = True
env["CASE_SENSITIVE_COMPLETIONS"] = False
env["COMPLETION_IN_THREAD"] = True
env["COMPLETION_MODE"] = "default"
env["COMPLETION_QUERY_LIMIT"] = 10
env["COMPLETIONS_CONFIRM"] = False
env["COMPLETIONS_MENU_ROWS"] = 2
env["DYNAMIC_CWD_WIDTH"] = "50%"
env["DYNAMIC_CWD_ELISION_CHAR"] = "..."
env["ENABLE_ASYNC_PROMPT"] = True
env["FOREIGN_ALIASES_SUPPRESS_SKIP_MESSAGE"] = 1
env["INDENT"] = "   "
env["MULTILINE_PROMPT"] = " "
env["SUBSEQUENCE_PATH_COMPLETION"] = True
env["SUGGEST_COMMANDS"] = True
env["SUGGEST_MAX_NUM"] = 20
env["TITLE"] = "Xonsh"
env["XONSH_AUTOPAIR"] = True
env["XONSH_CACHE_DIR"] = "~"
env["XONSH_COLOR_STYLE"] = "paraiso-dark"
env["XONSH_HISTORY_MATCH_ANYWHERE"] = True
env["PROMPT_TOOLKIT_COLOR_DEPTH"] = "DEPTH_24_BIT"
env["LS_COLORS"] = LS_COLORS


def _s(args: list[str]):
    """Wrapper around lsd to show git status"""
    if not args:
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
    "man": "batman",
    "cdi": "zi",  # Interactive zoxide (fzf)
    "cd": "z",  # Use zoxide instead of cd
    "ls": "lsd",
    "du": "du -h",
    "df": "df -h",
    "grep": "grep --color=auto",
    "rm": remove,
    "rmp": "/usr/bin/env rm",
    "s": _s,
    "sl": "sl -e",
    "vlc": "setsid vlc",
    "okular": "setsid okular",
    "nix-shell": "nix-shell --log-format bar-with-logs",
}
aliases.update(my_aliases)  # pylint: disable=undefined-variable


# Style the terminal
def set_style() -> None:
    """
    Sets the color style of the terminal
    """
    from xonsh.tools import (  # pylint: disable=import-error,import-outside-toplevel
        register_custom_style,
    )

    my_style = {
        "Token.Operator": "#fffd00",
        "Token.PTK.CompletionMenu": "#000000",
        "Token.Literal.Number.Integer": "#44ffff",
        "Token.Literal.Number.Float": "#44ffff",
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
    env["XONSH_COLOR_STYLE"] = "my_style"


set_style()


def customize_autocompleter() -> None:
    """
    Customize the autocompleter
    """
    import prompt_toolkit.styles.defaults as defstyle  # pylint: disable=import-error,import-outside-toplevel

    defstyle.PROMPT_TOOLKIT_STYLE.append(("bottom-toolbar", "noreverse"))
    defstyle.PROMPT_TOOLKIT_STYLE.append(("completion-menu", "bg:#771977 #000000"))


customize_autocompleter()


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
        """
        Returns @git_info_raw, tries twice in case of IOError

        Returns:
            str: Branch name colored according to the state of the repository or empty
            string if not in git repository
        """
        for _ in range(2):
            try:
                return XonshPrompt.git_info_raw()
            except subprocess.CalledProcessError:
                return ""
            except (
                IOError
            ):  # Sometimes, bad file descriptor error is emitted, we want to try again
                pass

    @staticmethod
    def git_info_raw() -> str:
        """
        Returns the information about the git repository in the current directory

        Returns:
            str: Branch name colored according to the state of the repository or empty
            string if not in git repository
        """
        # Check if the current directory is a git repository
        git_rev_parse = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=False,
        )
        if git_rev_parse.returncode != 0:
            return ""

        # Get the name of the current branch
        git_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=False,
        )

        branch = git_branch.stdout.strip()

        # Check if the repository is dirty (has uncommitted changes)
        git_status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=False,
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
        exit_code = env["LAST_RETURN_CODE"]
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
        return Style.DEFAULT


env["PROMPT_FIELDS"]["git-info"] = XonshPrompt.git_info
env["PROMPT_FIELDS"]["last-exit-code-info"] = XonshPrompt.last_exit_code_info
env["PROMPT_FIELDS"]["path-info"] = XonshPrompt.path_info
env["PROMPT_FIELDS"]["reset"] = XonshPrompt.reset
env["PROMPT_FIELDS"]["rainbow-user"] = lambda: XonshPrompt.dye(getuser())
env["PROMPT_FIELDS"]["end"] = lambda: XonshPrompt.dye("\n λ ")
env["PROMPT_FIELDS"]["separator"] = lambda: XonshPrompt.dye(".")

env["PROMPT"] = (
    "{rainbow-user}{separator}{path-info}{git-info}{last-exit-code-info}{end}{reset}"
)
