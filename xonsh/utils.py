import os
import glob
import shutil
import sys
import subprocess

from colorama import Fore, init
from typing import List
from git import Repo
from tabulate import tabulate

sys.path.append(os.path.expanduser("~/Config-Files/xonsh"))
from colors import (
    colorize,
    get_file_color,
    GIT_STATUS_COLORS,
    LS_COLORS,
)

# Initialize colorama module
init()

STATUS_GOOD = 0
STATUS_LITTLE_ERROR = 1
STATUS_NO_ENTRIES = 2
STATUS_BIG_ERROR = 3


TRASH = os.path.expanduser("~/.trash-bin")
""" Path to the directory where the files are moved when deleted """

DUMPLOG = os.path.expanduser("~/.dumplog.txt")
""" Path to the file where the information related to dumping is stored """

DELETED_FILE_AGE_LIMIT = 30
""" Number of days after which the file is considered dumpable """

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

        for state, *_, file in file_states:
            state_color = GIT_STATUS_COLORS.get(state, Fore.RESET)
            if file in staged_files:
                state_color = GIT_STATUS_COLORS["STAGED"]

            verbose_state = GIT_STATUS_VERBOSE.get(state, "")
            colorized_file = colorize(
                file,
                get_file_color(os.path.join(repo.working_tree_dir, file)),
            )

            # Append rows to the list
            table_data.append(
                [
                    f"{state_color}{state}",
                    f"{state_color}{verbose_state}",
                    colorized_file,
                ]
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


def remove(args: List[str]) -> int:
    """
    Moves files and directories passed as arguments into ~/.trash-bin.
    If the file/directory already exists in .trash-bin, it appends a number to its name.

    Globbing is supported.

    Uses colorize function to print the names of the files that were successfully deleted

    @param args: list of files and directories to remove
    @param talkative: if True, prints status messages to stdout
    """
    status = STATUS_GOOD
    if not args:
        print(f"{Fore.RED}No files or directories passed{Fore.RESET}", file=sys.stderr)
        return STATUS_NO_ENTRIES

    if not os.path.exists(TRASH):
        os.mkdir(TRASH)

    ok_messages = []
    error_messages = []

    for arg in args:
        arg = os.path.expanduser(arg)
        arg = os.path.abspath(arg)
        files = glob.glob(arg)

        for file in files:
            file_name = os.path.basename(file)
            message = (
                f"{Fore.GREEN} ✔ {colorize(os.path.basename(file_name))}{Fore.RESET}"
            )

            if os.path.exists(os.path.join(TRASH, file_name)):
                i = 1
                while os.path.exists(os.path.join(TRASH, f"{file_name}_{i}")):
                    i += 1
                file_name = f"{file_name}_{i}"

            try:
                shutil.move(file, os.path.join(TRASH, file_name))
                ok_messages.append(message)

            except Exception as e:
                message = f"{Fore.RED} ✘ {colorize(os.path.basename(file))}{Fore.RED}: {e}{Fore.RESET}"
                error_messages.append(message)

                status = STATUS_LITTLE_ERROR

        if not files:
            status = STATUS_LITTLE_ERROR
            message = f"{Fore.RED} ✘ {arg}: Does not match any files or directories{Fore.RESET}"
            error_messages.append(message)

    print(*ok_messages, sep="\n", end="")
    print(*error_messages, sep="\n", end="", file=sys.stderr)

    return status


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
