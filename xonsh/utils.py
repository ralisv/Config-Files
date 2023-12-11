import os
import shutil
import subprocess
from pathlib import Path

from git import Repo
from tabulate import tabulate

from colors import (
    Color,
    colorize,
    GIT_STATUS_COLORS,
    LS_COLORS,
)


GIT_STATUS_VERBOSE: dict[str, str] = {
    "M": "Modified",
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
}
""" A dictionary mapping git status codes to verbose descriptions """


def super_git_status() -> str:
    """
    Returns a string containing git status in super colorful format

    Returns:
        str: git status
    """
    try:
        repo = Repo(".", search_parent_directories=True)

        if not repo.is_dirty(untracked_files=True):
            return ""

        git_status = repo.git.status("--short")

        file_states = [line.split() for line in git_status.split("\n") if line]

        # When too many files were received from repo.git.status (tabulate handles extremely long lists slowly)
        if len(file_states) > 1000:
            return f"{Color.RED}Super git status error: TooManyEntries ({len(file_states)})"

        # Get staged files
        staged_files: set[str] = {item.a_path for item in repo.index.diff("HEAD")}  # type: ignore

        # Initialize a list to store the rows
        table_data: list[tuple[str, str, str]] = []

        for state, *_, filename in file_states:
            state_color = GIT_STATUS_COLORS.get(state, Color.DEFAULT)
            if filename in staged_files:
                state_color = GIT_STATUS_COLORS["STAGED"]

            verbose_state = GIT_STATUS_VERBOSE.get(state, "")
            colorized_file = colorize(filename)

            # Append rows to the list
            table_data.append(
                (
                    f"{state_color}{state}",
                    f"{state_color}{verbose_state}",
                    colorized_file,
                )
            )

        # Tabulate data
        return tabulate(table_data, tablefmt="plain") + "\n"

    except Exception:
        return ""


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
                [shutil.which("ls"), "--color=always", "-C", *args],  # type: ignore
                env={"LS_COLORS": LS_COLORS},
            )
            .decode()
            .strip()
        )

    except Exception as e:
        return f"{Color.RED}{e}{Color.DEFAULT}"


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
