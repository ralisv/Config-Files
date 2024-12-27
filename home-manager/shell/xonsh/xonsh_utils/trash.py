import glob
import os
import shutil
import sys
from pathlib import Path

from xonsh_utils.colors import (  # pylint: disable=import-error
    Color,
    Style,
    colorize_filename,
)

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
            f"{Color.RED}No files or directories passed{Style.DEFAULT}", file=sys.stderr
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
                message = (
                    f"{Color.GREEN} ✔ {colorize_filename(file.name)}{Style.DEFAULT}"
                )

                # shutil.move works across different file systems, Path.rename does not
                shutil.move(str(file), str(trashed_file))
                ok_messages.append(message)

            except Exception as e:
                message = f"{Color.RED} ✘ {colorize_filename(file.name)}{Color.RED}: {e}{Style.DEFAULT}"
                error_messages.append(message)

        if not files:
            message = f"{Color.RED} ✘ {arg}: Does not match any files or directories{Style.DEFAULT}"
            error_messages.append(message)

    print(*ok_messages, sep="\n", end="")
    print(*error_messages, sep="\n", end="", file=sys.stderr)


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
