import os
import shutil
import sys
import time

from colorama import init, Fore
from typing import List

sys.path.append(os.path.expanduser("~/Config-Files/xonsh"))
from colors import colorize


TRASH = os.path.expanduser("~/.trash-bin")
""" Path to the directory where the files are moved when deleted """

DUMPLOG = os.path.expanduser("~/.dumplog.txt")
""" Path to the file where the information related to dumping is stored """

DELETED_FILE_AGE_LIMIT = 30
""" Number of days after which the file is considered dumpable """


# Initialize colorama module
init()

def get_size(entry: os.DirEntry) -> int:
    """Returns the size of the file/directory. If it's a directory, it sums up the sizes of all the files in it"""
    try:
        if entry.is_file():
            return entry.stat().st_size
        
        elif entry.is_symlink():
            return 1
        
        return sum(get_size(os.scandir(sub_entry)) for sub_entry in entry.path)

    except (PermissionError, FileNotFoundError):
        return 0


def get_dumpable_files(age_limit: int) -> List[os.DirEntry]:
    """
    Returns a list of files in .trash-bin directory that haven't been modified in given time
    @param age_limit: number of days after which the file is considered dumpable
    """
    dumpable_files = []
    for entry in os.scandir(TRASH):
        try:
            last_modification_time = entry.stat().st_mtime
            if (time.time() - last_modification_time) // (60 * 60 * 24) > age_limit:
                dumpable_files.append(entry)
        except FileNotFoundError:
            # In case of a broken symbolic link
            dumpable_files.append(entry)

    return dumpable_files


def dump_trash(to_dump: List[os.DirEntry]) -> int:
    """
    Permanently deletes all files in .trash-bin directory that haven't been modified in more
    than 30 days and returns the total size of the deleted files
    """
    error_messages = []
    total_size = 0

    for entry in to_dump:
        try:
            curr_size = get_size(entry)

            if entry.is_dir():
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)

            total_size += curr_size

        except Exception as e:
            message = f"{Fore.RED} ✘ {colorize(entry.path)}{Fore.RED}: {e}{Fore.RESET}"
            error_messages.append(message)

    print(*error_messages, sep="\n", end="\n", file=sys.stderr)

    return total_size


def ask_whether_to_dump() -> None:
    """
    Asks the user whether to dump the trash or not,
    only asks if there are files that can be dumped and if the user hasn't been asked in the last 7 days
    """
    if (
        0 and os.path.exists(DUMPLOG)
        and (time.time() - os.path.getmtime(DUMPLOG)) // (60 * 60 * 24) < 7
    ):
        return

    dumpable = sorted(
        get_dumpable_files(DELETED_FILE_AGE_LIMIT), key=lambda entry: entry.name
    )
    if not dumpable:
        return

    print(
        f"{Fore.GREEN}The following files have been in the trash for more than {DELETED_FILE_AGE_LIMIT} days:{Fore.RESET}",
        end="\n\n",
    )
    print(
        *[
            colorize(file.path).replace(os.path.expanduser("~/.trash-bin/"), "")
            for file in dumpable
        ],
        sep="\n",
        end="\n\n",
    )

    print(
        f"{Fore.GREEN}Do you wish to permanently delete them?"
        f"[{Fore.LIGHTGREEN_EX}y{Fore.GREEN}/{Fore.RED}n{Fore.GREEN}] {Fore.RESET}",
        end="",
    )

    try:
        answer = input()

    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}The files have not been dumped.{Fore.RESET}")
        return

    with open(DUMPLOG, "a") as f:
        if answer.lower() in ["y", "yes", "yeah", "yep, sure", "yep", "why not"]:
            freed_memory = dump_trash(dumpable)
            print(
                f"{Fore.GREEN}Successfully freed {Fore.CYAN}{freed_memory / 1024 / 1024:.2f}{Fore.GREEN} MB{Fore.RESET}"
            )

            f.write(f"{time.strftime('%d.%m.%Y')} User dumped trash\n")

        elif answer.lower() in ["n", "no", "nope", "nah", "no way", "nah, thanks"]:
            print(
                f"{Fore.GREEN}The files have not been dumped, you'll be reminded again in 7 days.{Fore.RESET}"
            )

            f.write(f"{time.strftime('%d.%m.%Y')} User declined to dump trash\n")

        else:
            print(
                f"{Fore.RED}Invalid input, the files have not been dumped.{Fore.RESET}"
            )
