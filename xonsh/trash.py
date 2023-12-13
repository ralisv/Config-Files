import glob
import os
import shutil
import sys
import time
from pathlib import Path
from typing import List

from colors import Color, colorize
from utils import bytes_to_megabytes, get_size, seconds_to_days

TRASH_DIR = Path.home() / ".trash-bin"
""" Path to the directory where the files are moved when deleted """

DUMPLOG = Path.home() / ".dump.log"
""" Path to the file where the information related to dumping is stored """

DELETED_FILE_AGE_LIMIT = 30
""" Number of days after which the file is considered dumpable """


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
            trashed_file = Path(TRASH_DIR) / file.name
            if trashed_file.exists():
                # If file with such name already exists in trash, rename it
                i = 1
                while (TRASH_DIR / f"{file.name}_{i}").exists():
                    i += 1

                trashed_file = TRASH_DIR / f"{file.name}_{i}"

            try:
                file_size = bytes_to_megabytes(get_size(file))
                message = f"{Color.GREEN} ✔ {colorize(file.name)} ({Color.CYAN}{file_size:.2f} MB{Color.DEFAULT}){Color.DEFAULT}"

                # shutil.move works across different file systems, Path.rename
                # does not
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


def get_dumpable_files(age_limit: int) -> List[Path]:
    """
    Returns a list of files in .trash-bin directory that haven't been modified
    in more than 30 days

    Args:
        age_limit (int): The number of days after which the file is considered dumpable

    Returns:
        List[Path]: A list of files that can be dumped
    """
    dumpable_files: List[Path] = []
    for trashed_file in TRASH_DIR.iterdir():
        try:
            last_modification_time = trashed_file.stat().st_mtime
            if (time.time() - seconds_to_days(last_modification_time)) > age_limit:
                dumpable_files.append(trashed_file)
        except FileNotFoundError:
            # In case of a broken symbolic link
            dumpable_files.append(trashed_file)

    return dumpable_files


def dump(files: List[Path]) -> int:
    """
    Permanently deletes the given files and returns the amount of memory freed

    Args:
        files (List[Path]): The files to delete

    Returns:
        int: The amount of memory freed in bytes
    """
    error_messages: List[str] = []
    total_size = 0

    for file_to_dump in files:
        try:
            curr_size = get_size(file_to_dump)

            if file_to_dump.is_dir():
                shutil.rmtree(file_to_dump)
            else:
                file_to_dump.unlink()

            total_size += curr_size

        except Exception as e:
            message = (
                f"{Color.RED} ✘ {colorize(str(file_to_dump))}{Color.RED}: {e}{Color.DEFAULT}"
            )
            error_messages.append(message)

    print(*error_messages, sep="\n", end="\n", file=sys.stderr)

    return total_size


def initialize_trash_management() -> None:
    """
    Verifies that trash management is functional.
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

    if DUMPLOG.exists() and seconds_to_days(
            time.time() - DUMPLOG.stat().st_mtime) < 30:
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
        *[colorize(str(file)).replace(str(TRASH_DIR) + "/", "")
            for file in dumpable],
        sep="\n",
        end="\n\n",
    )

    print(
        f"{Color.GREEN}Do you wish to permanently delete them?"
        f"[{Color.LIME_GREEN}y{Color.GREEN}/{Color.RED}n{Color.GREEN}] {Color.DEFAULT}",
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
                f"{Color.GREEN}Successfully freed {Color.CYAN}{bytes_to_megabytes(freed_memory):.2f}{Color.GREEN} MB{Color.DEFAULT}"
            )

            dumplog.write(f"{time.strftime(" % d. % m. % Y")} User dumped trash\n")

        elif answer.lower() in ["n", "no", "nope", "nah", "no way", "nah, thanks"]:
            print(
                f"{Color.GREEN}The files have not been dumped, you'll be reminded again in 7 days.{Color.DEFAULT}"
            )

            dumplog.write(f"{time.strftime(" % d. % m. % Y")} User declined to dump trash\n")

        else:
            print(
                f"{Color.RED}Invalid input, the files have not been dumped.{Color.DEFAULT}"
            )
