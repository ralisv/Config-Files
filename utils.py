import os
import glob
import shutil
import sys
import time
from colorama import Fore, init


init()


STATUS_GOOD = 0
STATUS_LITTLE_ERROR = 1
STATUS_NO_ENTRIES = 2
TRASH = os.path.expanduser("~/.trash-bin")
RMLOG = os.path.expanduser("~/.rmlog.txt")


def remove(args, talkative=True):
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
            except e:

                if talkative:
                    print(f"{Fore.RED}{e}{Fore.RESET}")

                status = STATUS_LITTLE_ERROR

            if talkative:
                print(f"{Fore.YELLOW}{file}{Fore.GREEN} moved into trash{Fore.RESET}")

            with open(RMLOG, "a") as f:
                f.write(f"{time.strftime('%d. %m. %Y')} {file} moved to ~/.trash-bin/{file_name}\n")

        if not files:
            status = STATUS_LITTLE_ERROR

            if talkative:
                print(f"{Fore.RED}{arg} does not match any files or directories{Fore.RESET}", file=sys.stderr)

    return status


def get_size(entry):
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


def dump_trash(talkative=True):
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
                f.write(f"{time.strftime('%d. %m. %Y')} {e}\n")

    if talkative:
        print(f'{Fore.GREEN}Total size of deleted files: {Fore.YELLOW}{total_size / (1024 * 1024):.2f}{Fore.GREEN} MB{Fore.RESET}')


def start_in_new_session(process, args, quiet=True):
    pid = os.fork()
    if pid == 0:
        os.setsid()
        if quiet:
            with open(os.devnull, "w") as f:
                os.dup2(f.fileno(), 1)
                os.dup2(f.fileno(), 2)

        os.execvp(process, [process] + list(args))
