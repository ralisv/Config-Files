import os
import shutil
import sys
import time
from pathlib import Path

from colorama import Fore
from typing import List

from colors import colorize


TRASH_DIR = Path.home() / ".trash-bin"
""" Path to the directory where the files are moved when deleted """

DUMPLOG = Path.home() / ".dump.log"
""" Path to the file where the information related to dumping is stored """

DELETED_FILE_AGE_LIMIT = 30
""" Number of days after which the file is considered dumpable """


def get_days(seconds: float) -> float:
    return seconds / (60 * 60 * 24)


def get_size(file_path: Path) -> int:
    """Returns the size of the file/directory. If it's a directory, it sums up the sizes of all the files in it"""
    try:
        if file_path.is_file():
            return file_path.stat().st_size

        elif file_path.is_symlink():
            return 1

        return sum(get_size(sub_entry) for sub_entry in os.scandir(file_path.path))

    except (PermissionError, FileNotFoundError):
        return 0


def get_dumpable_files(age_limit: int) -> List[Path]:
    """
    Returns a list of files in .trash-bin directory that haven't been modified in given time
    @param age_limit: number of days after which the file is considered dumpable
    """
    dumpable_files: List[Path] = []
    for trashed_file in TRASH_DIR.iterdir():
        try:
            last_modification_time = trashed_file.stat().st_mtime
            if (time.time() - get_days(last_modification_time)) > age_limit:
                dumpable_files.append(trashed_file)
        except FileNotFoundError:
            # In case of a broken symbolic link
            dumpable_files.append(trashed_file)

    return dumpable_files


def dump(files: List[Path]) -> int:
    """
    Permanently deletes all files in .trash-bin directory that haven't been modified in more
    than 30 days and returns the total size of the deleted files
    """
    error_messages = []
    total_size = 0

    for file_to_dump in files:
        try:
            curr_size = get_size(file_to_dump)

            if file_to_dump.is_dir():
                shutil.rmtree(file_to_dump.path)
            else:
                file_to_dump.unlink()

            total_size += curr_size

        except Exception as e:
            message = f"{Fore.RED} ✘ {colorize(file_to_dump.path)}{Fore.RED}: {e}{Fore.RESET}"
            error_messages.append(message)

    print(*error_messages, sep="\n", end="\n", file=sys.stderr)

    return total_size


def initialize_trash_management() -> None:
    """
    Creates the necessary files for trash management in the home directory,
    does nothing if those files already exist.
    """
    if not TRASH_DIR.exists():
        print(f"{Fore.GREEN}Creating {TRASH_DIR} file for trash management")
        TRASH_DIR.mkdir()

    if not DUMPLOG.exists():
        print(f"{Fore.GREEN}Creating {DUMPLOG} file for trash management")
        DUMPLOG.touch(mode=777)


def ask_whether_to_dump() -> None:
    """
    Verifies that trash management is functional.

    Asks the user whether to dump the trash or not,
    only asks if there are files that can be dumped and if the user hasn't been asked in the last 7 days
    """
    initialize_trash_management()

    if DUMPLOG.exists() and get_days(time.time() - DUMPLOG.stat().st_mtime) < 30:
        return

    dumpable = sorted(
        get_dumpable_files(DELETED_FILE_AGE_LIMIT), key=lambda entry: entry.name
    )
    if not dumpable:
        return

    print(
        f"{Fore.GREEN}The following files have been in the trash for more than"
        f"{DELETED_FILE_AGE_LIMIT} days:{Fore.RESET}",
        end="\n\n",
    )
    print(
        *[colorize(file).replace(str(TRASH_DIR) + "/", "") for file in dumpable],
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

    with DUMPLOG.open("a") as dumplog:
        if answer.lower() in ["y", "yes", "yeah", "yep, sure", "yep", "why not"]:
            freed_memory = dump(dumpable)
            print(
                f"{Fore.GREEN}Successfully freed {Fore.CYAN}{freed_memory / 1024 / 1024:.2f}{Fore.GREEN} MB{Fore.RESET}"
            )

            dumplog.write(f"{time.strftime('%d.%m.%Y')} User dumped trash\n")

        elif answer.lower() in ["n", "no", "nope", "nah", "no way", "nah, thanks"]:
            print(
                f"{Fore.GREEN}The files have not been dumped, you'll be reminded again in 7 days.{Fore.RESET}"
            )

            dumplog.write(f"{time.strftime('%d.%m.%Y')} User declined to dump trash\n")

        else:
            print(
                f"{Fore.RED}Invalid input, the files have not been dumped.{Fore.RESET}"
            )
