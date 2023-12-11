import os
import glob
import shutil
import sys
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
from trash import TRASH_DIR, initialize_trash_management


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


def remove(args: list[str]) -> None:
    """
    Moves files to trash directory

    Args:
        args (list[str]): files to remove
    """
    if not args:
        print(
            f"{Color.RED}No files or directories passed{Color.DEFAULT}", file=sys.stderr
        )
        return

    initialize_trash_management()

    ok_messages: list[str] = []
    error_messages: list[str] = []
    for arg in args:
        arg = os.path.expanduser(arg)
        arg = os.path.abspath(arg)
        files: list[str] = glob.glob(arg, recursive=True)

        for file in map(Path, files):
            message = f"{Color.GREEN} ✔ {colorize(file.name)}{Color.DEFAULT}"

            trashed_file = Path(TRASH_DIR) / file.name
            if trashed_file.exists():
                # If file with such name already exists in trash, rename it
                i = 1
                while (TRASH_DIR / f"{file.name}_{i}").exists():
                    i += 1

                trashed_file = TRASH_DIR / f"{file.name}_{i}"

            try:
                # shutil.move works across different file systems, Path.rename does not
                shutil.move(str(file), str(trashed_file))
                ok_messages.append(message)

            except Exception as e:
                message = f"{Color.RED} ✘ {colorize(file.name)}{Color.RED}: {e}{Color.DEFAULT}"
                error_messages.append(message)

        if not files:
            message = f"{Color.RED} ✘ {arg}: Does not match any files or directories{Color.DEFAULT}"
            error_messages.append(message)

    print(*ok_messages, sep="\n", end="")
    print(*error_messages, sep="\n", end="", file=sys.stderr)


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
