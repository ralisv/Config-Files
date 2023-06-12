import os
import glob
import shutil
import sys
import time
import subprocess
import stat

from colorama import Fore, init
from typing import List


init()

LS_COLORS = open(f"{os.path.expanduser('~')}/Config-Files/ls-colors.txt").read()
""" The contents of the LS_COLORS environment variable """

LS_COLORS_PARSED = dict(map(lambda assignment: assignment.split(sep="="), LS_COLORS.split(sep=":")))
""" LS_COLORS parsed into a dictionary where the keys are file types and the values are color codes """


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


def colorize(filename: str) -> str:
    """
    Returns the filename enclosed in the color escape sequence based on LS_COLORS
    It is required that at least rs (reset) color is defined in LS_COLORS, as it is
    used as a fallback when color for the file type is not defined
    """
    # Get the file extension
    _, ext = os.path.splitext(filename)
    ext = f"*{ext}"

    color = None

    if os.path.isfile(filename) and ext in LS_COLORS_PARSED:
        color = LS_COLORS_PARSED[ext]

    # If the file is a directory, get the directory color
    elif os.path.isdir(filename):
        color = LS_COLORS_PARSED.get('di')

    # If the file is a symbolic link, get the link color
    elif os.path.islink(filename):
        color = LS_COLORS_PARSED.get('ln')

    # If the file is a fifo pipe, get the pipe color
    elif os.path.exists(filename) and stat.S_ISFIFO(os.stat(filename).st_mode):
        color = LS_COLORS_PARSED.get('pi')

    # If the file is a socket, get the socket color
    elif os.path.exists(filename) and stat.S_ISSOCK(os.stat(filename).st_mode):
        color = LS_COLORS_PARSED.get('so')

    # If the file is a block (buffered) special file, get the block color
    elif os.path.exists(filename) and stat.S_ISBLK(os.stat(filename).st_mode):
        color = LS_COLORS_PARSED.get('bd')

    # If the file is a character (unbuffered) special file, get the character color
    elif os.path.exists(filename) and stat.S_ISCHR(os.stat(filename).st_mode):
        color = LS_COLORS_PARSED.get('cd')

    # If the file is a symbolic link and orphaned, get the orphan color
    elif os.path.islink(filename) and not os.path.exists(os.readlink(filename)):
        color = LS_COLORS_PARSED.get('or')

    # If the file is a regular file and an executable
    elif os.path.isfile(filename) and os.access(filename, os.X_OK):
        color = LS_COLORS_PARSED.get('ex')

    if color is None:
        color = LS_COLORS_PARSED.get('rs')

    # Return the filename enclosed in the color escape sequence
    # The "\033[0m" sequence at the end resets the color back to the default
    return f"\033[{color}m{filename}\033[0m"


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
            message = f"{Fore.GREEN} ✔ {colorize(os.path.basename(file_name))}{Fore.RESET}"

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


def get_size(entry: os.DirEntry) -> int:
    """ Returns the size of the file/directory. If it's a directory, it sums up the sizes of all the files in it """
    if entry.is_file():
        return entry.stat().st_size
    total = 0
    try:
        for sub_entry in os.scandir(entry):
            total += get_size(sub_entry)

    except PermissionError:
        return 0
    
    return total


def get_dumpable_files(age_limit: int) -> List[os.DirEntry]:
    """
    Returns a list of files in .trash-bin directory that haven't been modified in given time
    @param age_limit: number of days after which the file is considered dumpable
    """
    return [entry for entry in os.scandir(TRASH) if (time.time() - entry.stat().st_mtime) // (60 * 60 * 24) > age_limit]


def dump_trash(to_dump: List[os.DirEntry]) -> None:
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
    if os.path.exists(DUMPLOG) and (time.time() - os.path.getmtime(DUMPLOG)) // (60 * 60 * 24) < 7:
        return
    
    dumpable = sorted(get_dumpable_files(DELETED_FILE_AGE_LIMIT), key=lambda entry: entry.name)
    if not dumpable:
        return

    print(f"{Fore.GREEN}The following files have been in the trash for more than {DELETED_FILE_AGE_LIMIT} days:{Fore.RESET}", end="\n\n")
    print(*[colorize(file.path).replace(os.path.expanduser("~/.trash-bin/"), "") for file in dumpable], sep="\n", end="\n\n")

    print(f"{Fore.GREEN}Do you wish to permanently delete them?" \
          "[{Fore.LIGHTGREEN_EX}y{Fore.GREEN}/{Fore.RED}n{Fore.GREEN}] {Fore.RESET}", end="")
    answer = input()

    with open(DUMPLOG, "a") as f:

        if answer.lower() in ["y", "yes", "yeah", "yep, sure", "yep", "why not"]:
            freed_memory = dump_trash(dumpable)
            print(f"{Fore.GREEN}Successfully freed {Fore.CYAN}{freed_memory / 1024 / 1024:.2f}{Fore.GREEN} MB{Fore.RESET}")

            f.write(f"{time.strftime('%d.%m.%Y')} User dumped trash\n")

        else:
            print(f"{Fore.GREEN}The files have not been dumped, you'll be reminded again in 7 days.{Fore.RESET}")

            f.write(f"{time.strftime('%d.%m.%Y')} User declined to dump trash\n")


def start_in_new_session(process: str, args: List[str], quiet: bool = True, env=None) -> None:
    """
    Starts a process in a new session. If quiet os.execvpis True, it redirects stdout and stderr to /dev/null

    @param process: name of the process to start
    @param args: arguments to pass to the process
    @param quiet: if True, redirects stdout and stderr to /dev/null
    """
    stdout = subprocess.DEVNULL if quiet else None
    stderr = subprocess.DEVNULL if quiet else None

    subprocess.Popen([process] + args, stdout=stdout, stderr=stderr, start_new_session=True, env=env)


def super_ls(args: List[str]) -> None:
    """
    Executes git status when in a git repository and always executes ls after that
    """
    status = STATUS_GOOD

    try:
        is_git_repo = os.path.exists(".git")

        if is_git_repo:
            start_in_new_session(
                "git", ["status", "--short"],
                quiet=False
            ) or status
            time.sleep(0.005)
            start_in_new_session("echo", [], quiet=False)

        start_in_new_session(
            "ls", ["--color=always", "-X"] + args,
            quiet=False,
            env={"LS_COLORS":  LS_COLORS}
        )
    
    except Exception as e:
        print(f"{Fore.RED}{e}{Fore.RESET}", file=sys.stderr)
        status = STATUS_BIG_ERROR
    
    finally:
        return status
