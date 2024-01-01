import os
import shutil
import subprocess
from pathlib import Path

from tabulate import tabulate

from colors import (
    GIT_STATUS_COLORS,
    GIT_STATUS_COLORS_STAGED,
    LS_COLORS,
    Color,
    Style,
    colorize,
)

GIT_STATUS_VERBOSE: dict[str, str] = {
    "M": "Modified",
    "MM": "Modified after staged",
    "A": "Added",
    "D": "Deleted",
    "R": "Renamed",
    "C": "Copied",
    "U": "Unmerged",
    "??": "Untracked",
    "DU": "Unmerged, both deleted",
    "AU": "Unmerged, added by us",
    "UD": "Unmerged, deleted by them",
    "UA": "Unmerged, added by them",
    "DA": "Unmerged, deleted by us",
    "AA": "Unmerged, both added",
    "UU": "Unmerged, both modified",
    "AD": "Unmerged, added by us, deleted by them",
}
""" A dictionary mapping git status codes to verbose descriptions """


def super_git_status() -> str:
    """
    Returns a string containing git status in super colorful format

    Returns:
        str: git status
    """
    # Get root directory of the git repository
    git_revparse = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    )

    # When not in a git repository, return empty string
    if git_revparse.returncode != 0:
        return ""

    repo_root = Path(git_revparse.stdout.strip())

    # Get the git status in short format
    git_status = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )

    # When git status reports no changes, return empty string
    if git_status.stdout == "":
        return ""

    file_states = [line.split() for line in git_status.stdout.split("\n") if line]

    # When too many files were received from git status
    if len(file_states) > 1000:
        return f"{Color.RED}Super git status error: TooManyEntries ({len(file_states)})"

    # Get the staged files
    git_diff = subprocess.run(
        ["git", "diff", "--name-only", "--cached"], capture_output=True, text=True
    )
    staged_files = set(git_diff.stdout.splitlines())

    # Initialize a list to store the rows
    table_data: list[tuple[str, str, str]] = []

    for state, *_, filename in file_states:
        state_color = (
            GIT_STATUS_COLORS
            if filename not in staged_files
            else GIT_STATUS_COLORS_STAGED
        ).get(state, Style.DEFAULT)

        # Get the relative path to the file
        file_path = os.path.relpath(repo_root / filename, Path.cwd())

        verbose_state = GIT_STATUS_VERBOSE.get(state, "")

        # Append rows to the list
        table_data.append(
            (
                f"{state_color}{state}",
                f"{state_color}{verbose_state}",
                colorize(file_path),
            )
        )

    # Assuming tabulate is defined elsewhere
    return tabulate(table_data, tablefmt="plain") + "\n"


def super_ls(args: list[str]) -> str:
    """
    Returns a string containing ls in super colorful format

    Args:
        args (list[str]): arguments to pass to ls

    Returns:
        str: ls
    """
    try:
        return (
            subprocess.check_output(
                [
                    str(shutil.which("ls")),
                    "--color=always",
                    "-C",
                    *args,
                ],  # type: ignore
                env={"LS_COLORS": LS_COLORS},
                stderr=subprocess.PIPE,
            )
            .decode()
            .strip()
        )

    except subprocess.CalledProcessError as e:
        return f"{Color.RED}Command '{e.cmd}' returned status {e.returncode}. Output: {e.output}, Error: {e.stderr}{Style.DEFAULT}"

    except Exception as e:
        return f"{Color.RED}{e}{Style.DEFAULT}"


def super_util(args: list[str]) -> None:
    """
    Executes super git status and super ls

    Args:
        args (list[str]): arguments to pass to ls
    """
    git_status = super_git_status()
    ls = super_ls(args)

    if git_status != "":
        print(git_status, ls, sep="\n")

    else:
        print(ls)


def start_in_new_session(
    process: str,
    args: list[str],
    quiet: bool = True,
    env: dict[str, str] | None = None,
) -> None:
    """
    Starts a process in a new session

    Args:
        process (str): name of the process to start
        args (list[str]): arguments to pass to the process
        quiet (bool, optional): Whether to print the process' logs into console. Defaults to True.
        env (Optional[dict[str, str]], optional): Environment. Defaults to None.
    """
    stdout: int | None = subprocess.DEVNULL if quiet else None
    stderr: int | None = subprocess.DEVNULL if quiet else None

    subprocess.Popen(
        args=[process] + args,
        stdout=stdout,
        stderr=stderr,
        start_new_session=True,
        env=env,
    )


def get_size(path: Path) -> int:
    """
    Returns the size of the given file or directory in bytes

    Args:
        path (Path): The path to the file or directory

    Returns:
        int: The size of the file or directory in bytes
    """
    total = 0

    try:
        for dirpath, _, filenames in os.walk(path, followlinks=False):
            for f in filenames:
                fp = Path(dirpath) / f

                if not fp.is_symlink():
                    total += fp.stat().st_size
    except (PermissionError, FileNotFoundError):
        return 0

    return total


def seconds_to_days(seconds: float) -> float:
    """
    Converts seconds to days
    Args:
        seconds (float): The number of seconds to convert

    Returns:
        float: The number of days
    """
    return seconds / (60 * 60 * 24)


def bytes_to_megabytes(size_in_bytes: int) -> float:
    """
    Converts bytes to megabytes

    Args:
        size_in_bytes (int): The number of bytes to convert

    Returns:
        float: The number of megabytes
    """
    return size_in_bytes / 1024 / 1024
