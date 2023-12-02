import os
import glob
import shutil
import sys
import subprocess
from pathlib import Path

from colorama import Fore
from typing import List
from git import Repo
from tabulate import tabulate

from colors import (
    colorize,
    GIT_STATUS_COLORS,
    LS_COLORS,
)
from trash import TRASH_DIR, initialize_trash_management


GIT_STATUS_VERBOSE = {
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


def super_git_status() -> str:
    """
    Returns string representing git status --short with colored files based on LS_COLORS
    """
    try:
        repo = Repo(".", search_parent_directories=True)

        if not repo.is_dirty(untracked_files=True):
            return ""

        git_status = repo.git.status("--short")

        file_states = [line.split() for line in git_status.split("\n") if line]

        # When too many files were received from repo.git.status (tabulate handles extremely long lists slowly)
        if len(file_states) > 1000:
            return (
                f"{Fore.RED}Super git status error: TooManyEntries ({len(file_states)})"
            )

        # Get staged files
        staged_files = {item.a_path for item in repo.index.diff("HEAD")}

        # Initialize a list to store the rows
        table_data = []

        for state, *_, filename in file_states:
            state_color = GIT_STATUS_COLORS.get(state, Fore.RESET)
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


def super_ls(args):
    """
    Executes ls with color and column options
    """
    try:
        return (
            subprocess.check_output(
                [shutil.which("ls"), "--color=always", "-C", *args],
                env={"LS_COLORS": LS_COLORS},
            )
            .decode()
            .strip()
        )

    except Exception as e:
        return f"{Fore.RED}{e}{Fore.RESET}"


def super_util(args: List[str]) -> int:
    git_status = super_git_status()
    ls = super_ls(args)

    if git_status != "":
        print(git_status, ls, sep="\n")

    else:
        print(ls)


def remove(args: List[str]):
    """
    Moves files and directories passed as arguments into ~/.trash-bin.
    If the file/directory already exists in .trash-bin, it appends a number to its name.

    Globbing is supported.

    Uses colorize function to print the names of the files that were successfully deleted

    @param args: list of files and directories to remove
    @param talkative: if True, prints status messages to stdout
    """
    if not args:
        print(f"{Fore.RED}No files or directories passed{Fore.RESET}", file=sys.stderr)
        return

    initialize_trash_management()

    ok_messages = []
    error_messages = []
    for arg in args:
        arg = os.path.expanduser(arg)
        arg = os.path.abspath(arg)
        files = glob.glob(arg, recursive=True)

        for file in map(Path, files):
            message = f"{Fore.GREEN} ✔ {colorize(file.name)}{Fore.RESET}"

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
                message = (
                    f"{Fore.RED} ✘ {colorize(file.name)}{Fore.RED}: {e}{Fore.RESET}"
                )
                error_messages.append(message)

        if not files:
            message = f"{Fore.RED} ✘ {arg}: Does not match any files or directories{Fore.RESET}"
            error_messages.append(message)

    print(*ok_messages, sep="\n", end="")
    print(*error_messages, sep="\n", end="", file=sys.stderr)


def start_in_new_session(
    process: str,
    args: List[str],
    quiet: bool = True,
    env=None,
) -> None:
    """
    Starts a process in a new session. If quiet os.execvpis True, it redirects stdout and stderr to /dev/null

    @param process: name of the process to start
    @param args: arguments to pass to the process
    @param quiet: if True, redirects stdout and stderr to /dev/null
    """
    stdout = subprocess.DEVNULL if quiet else None
    stderr = subprocess.DEVNULL if quiet else None

    subprocess.Popen(
        [process] + args, stdout=stdout, stderr=stderr, start_new_session=True, env=env
    )
