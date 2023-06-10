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
STATUS_BIG_ERROR = 3

TRASH = os.path.expanduser("~/.trash-bin")
RMLOG = os.path.expanduser("~/.rmlog.txt")
DUMPLOG = os.path.expanduser("~/.dumplog.txt")

DELETED_FILE_AGE_LIMIT = 30

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
            print(f"{Fore.RED}An error occurred while attempting to delete {Fore.YELLOW}{entry.name}{Fore.RED}: {e}{Fore.RESET}")

            with open(DUMPLOG, "a") as f:
                f.write(f"{time.strftime('%d. %m. %Y')} Dumping of {entry.name} failed: {e}\n")

    return total_size


def ask_whether_to_dump() -> None:
    """
    Asks the user whether to dump the trash or not,
    only asks if there are files that can be dumped and if the user hasn't been asked in the last 7 days
    """
    if os.path.exists(DUMPLOG) and (time.time() - os.path.getmtime(DUMPLOG)) // (60 * 60 * 24) < 7 \
            or not (dumpable := sorted(get_dumpable_files(DELETED_FILE_AGE_LIMIT), key=lambda entry: entry.name)):
        return
    
    print(f"The following files have been in the trash for more than {DELETED_FILE_AGE_LIMIT} days:")
    for entry in dumpable:
        print(f"{Fore.YELLOW}{entry.name}{Fore.RESET}")

    print("Do you want to permanently delete them? [y/n] ", end="")
    answer = input()

    if answer.lower() in ["y", "yes", "yeah", "yep, sure", "yep", "why not"]:
        freed_memory = dump_trash(dumpable)
        print(f"{Fore.GREEN}Successfully freed {freed_memory / 1024 / 1024:.2f} MB{Fore.RESET}")

    else:
        print(f"{Fore.GREEN}The files have not been dumped, you'll be asked again in 7 days.{Fore.RESET}")
        with open(DUMPLOG, "a") as f:
            f.write(f"{time.strftime('%d.%m.%Y')} User declined to dump trash\n")


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


def super_ls(args: List[str]) -> None:
    """
    Executes git status when in a git repository and always executes ls after that
    """
    status = STATUS_GOOD

    try:
        is_git_repo = os.path.exists(".git")

        if is_git_repo:
            status = start_in_new_session(
                "git", ["status", "--short"],
                quiet=False
            ) or status
            start_in_new_session("echo", [], quiet=False)

        status = start_in_new_session(
            "ls", ["--color=always"] + args,
            quiet=False,
            env={"LS_COLORS":  open("/home/ralis/Config-Files/ls-colors.txt").read()}
        ) or status
    
    except Exception as e:
        print(f"{Fore.RED}{e}{Fore.RESET}", file=sys.stderr)
        status = STATUS_BIG_ERROR
    
    finally:
        return status
