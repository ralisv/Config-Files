import os
import glob
import shutil
import sys
import time
import subprocess

from colorama import Fore, init
from typing import List


init()


STATUS_GOOD = 0
STATUS_LITTLE_ERROR = 1
STATUS_NO_ENTRIES = 2

TRASH = os.path.expanduser("~/.trash-bin")
RMLOG = os.path.expanduser("~/.rmlog.txt")

LS_COLORS = open("./ls-colors.txt").read()


def remove(args: List[str], talkative: bool = True) -> int:
    """
    Moves files and directories passed as arguments into ~/.trash-bin.
    If the file/directory already exists in .trash-bin, it appends a number to its name.

    Globbing is supported.

    @param args: list of files and directories to remove
    @param talkative: if True, prints status messages to stdout

    """
    status = STATUS_GOOD
    if not args:
        if talkative:
            print(f"{Fore.RED}No files or directories passed{Fore.RESET}", file=sys.stderr)
        return STATUS_NO_ENTRIES

    if not os.path.exists(TRASH):
        os.mkdir(TRASH)

    for arg in args:
        arg = os.path.expanduser(arg)
        arg = os.path.abspath(arg)
        files = glob.glob(arg)
        for file in files:
            file_name = os.path.basename(file)

            if os.path.exists(os.path.join(TRASH, file_name)):
                i = 1
                while os.path.exists(os.path.join(TRASH, f"{file_name}_{i}")):
                    i += 1
                file_name = f"{file_name}_{i}"

            try:
                shutil.move(file, os.path.join(TRASH, file_name))
            except Exception as e:

                if talkative:
                    print(f"{Fore.RED}Error while trying to remove {file}: {e}{Fore.RESET}")

                status = STATUS_LITTLE_ERROR
                continue

            if talkative:
                print(f"{Fore.YELLOW}{file}{Fore.GREEN} moved into trash{Fore.RESET}")

            with open(RMLOG, "a") as f:
                f.write(f"{time.strftime('%d. %m. %Y')} {file} moved to ~/.trash-bin/{file_name}\n")

        if not files:
            status = STATUS_LITTLE_ERROR

            if talkative:
                print(f"{Fore.RED}{arg} does not match any files or directories{Fore.RESET}", file=sys.stderr)

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


def dump_trash(talkative: bool = True) -> None:
    """ Permanently deletes all files in .trash-bin directory that haven't been modified in more than 30 days and logs the total size of deleted files """
    total_size = 0

    with open(RMLOG, "a") as f:
        for entry in os.scandir(TRASH):
            try:
                if (time.time() - entry.stat().st_mtime) // (60 * 60 * 24) > 30:

                    total_size += get_size(entry)

                    if entry.is_dir():
                        shutil.rmtree(entry.path)
                    else:
                        os.remove(entry.path)

                    f.write(f"{time.strftime('%d. %m. %Y')} {entry.path} removed permanently\n")

            except Exception as e:
                if talkative:
                    print(f"{Fore.RED}{e}{Fore.RESET}")
                f.write(f"{time.strftime('%d. %m. %Y')} Dumping failed: {e}\n")


    if talkative:
        print(f'{Fore.GREEN}Total size of deleted files: {Fore.YELLOW}{total_size / (1024 * 1024):.2f}{Fore.GREEN} MB{Fore.RESET}')


def start_in_new_session(process: str, args: List[str], quiet: bool = True, env=None) -> int:
    """
    Starts a process in a new session. If quiet os.execvpis True, it redirects stdout and stderr to /dev/null

    @param process: name of the process to start
    @param args: arguments to pass to the process
    @param quiet: if True, redirects stdout and stderr to /dev/null
    """
    stdout = subprocess.DEVNULL if quiet else None
    stderr = subprocess.DEVNULL if quiet else None

    return subprocess.Popen([process] + args, stdout=stdout, stderr=stderr, start_new_session=True, env=env).wait()


def _s(args: List[str]) -> None:
    """
    Executes git status when in a git repository and always executes ls after that
    """
    status_code = STATUS_GOOD

    is_git_repo = os.path.exists(".git")

    if is_git_repo:
        status_code = STATUS_LITTLE_ERROR if start_in_new_session("git", ["status", "--short"], quiet=False) else status_code
    
    if is_git_repo:
        print()

    status_code = STATUS_LITTLE_ERROR if start_in_new_session("ls", ["--color=always"] + args, quiet=False, env={"LS_COLORS": LS_COLORS}) else status_code

    return status_code
