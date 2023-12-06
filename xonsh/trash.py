import os
import shutil
import sys
import time
from pathlib import Path

from typing import List

from colors import colorize, Color


TRASH_DIR = Path.home() / ".trash-bin"
""" Path to the directory where the files are moved when deleted """

DUMPLOG = Path.home() / ".dump.log"
""" Path to the file where the information related to dumping is stored """

DELETED_FILE_AGE_LIMIT = 30
""" Number of days after which the file is considered dumpable """


def get_days(seconds: float) -> float:
    return seconds / (60 * 60 * 24)


def get_size(path: Path) -> int:
    """Returns the size of the file/directory. If it's a directory, it sums up the sizes of all the files in it"""
    total = 0

    try:
        for dirpath, _, filenames in os.walk(path, followlinks=False):
            for f in filenames:
                fp = Path(dirpath) / f
                
                if not fp.is_symlink():
                    total += fp.stat().st_size
    except (PermissionError, FileNotFoundError) as e:
        return 0
    return total


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
            message = (
                f"{Color.RED} ✘ {colorize(file_to_dump.path)}{Color.RED}: {e}{Color.DEFAULT}"
            )
            error_messages.append(message)

    print(*error_messages, sep="\n", end="\n", file=sys.stderr)

    return total_size


def initialize_trash_management() -> None:
    """
    Creates the necessary files for trash management in the home directory,
    does nothing if those files already exist.
    """
    if not TRASH_DIR.exists():
        print(f"{Color.GREEN}Creating {TRASH_DIR} file for trash management")
        TRASH_DIR.mkdir()

    if not DUMPLOG.exists():
        print(f"{Color.GREEN}Creating {DUMPLOG} file for trash management")
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
        f"{Color.GREEN}The following files have been in the trash for more than"
        f"{DELETED_FILE_AGE_LIMIT} days:{Color.DEFAULT}",
        end="\n\n",
    )
    print(
        *[colorize(file).replace(str(TRASH_DIR) + "/", "") for file in dumpable],
        sep="\n",
        end="\n\n",
    )

    print(
        f"{Color.GREEN}Do you wish to permanently delete them?"
        f"[{Color.LIGHTGREEN_EX}y{Color.GREEN}/{Color.RED}n{Color.GREEN}] {Color.DEFAULT}",
        end="",
    )

    try:
        answer = input().strip()

    except KeyboardInterrupt:
        print(f"\n{Color.GREEN}The files have not been dumped.{Color.DEFAULT}")
        return

    with DUMPLOG.open("a") as dumplog:
        if answer.lower() in ["y", "yes", "yeah", "yep, sure", "yep", "why not"]:
            freed_memory = dump(dumpable)
            print(
                f"{Color.GREEN}Successfully freed {Color.CYAN}{freed_memory / 1024 / 1024:.2f}{Color.GREEN} MB{Color.DEFAULT}"
            )

            dumplog.write(f"{time.strftime('%d.%m.%Y')} User dumped trash\n")

        elif answer.lower() in ["n", "no", "nope", "nah", "no way", "nah, thanks"]:
            print(
                f"{Color.GREEN}The files have not been dumped, you'll be reminded again in 7 days.{Color.DEFAULT}"
            )

            dumplog.write(f"{time.strftime('%d.%m.%Y')} User declined to dump trash\n")

        else:
            print(
                f"{Color.RED}Invalid input, the files have not been dumped.{Color.DEFAULT}"
            )
