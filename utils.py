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


def remove(args):
    status = STATUS_GOOD
    if not args:
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

            shutil.move(file, os.path.join(TRASH, file_name))

            with open(RMLOG, "a") as f:
                f.write(f"{time.strftime('%d. %m. %Y')} {file} moved to ~/.trash-bin/{file_name}\n")

        if not files:
            status = STATUS_LITTLE_ERROR
            print(f"{Fore.RED}{arg} does not match any files or directories{Fore.RESET}", file=sys.stderr)

    return status


def dump_trash():
    """ Permanently deletes all files in .trash-bin directory that haven't been modified in more than 30 days """
    with open(RMLOG, "a") as f:
        for file in glob.glob(f"{TRASH}/*"):
            try:
                if (time.time() - os.path.getmtime(file)) // (60 * 60 * 24) > 30:
                    if os.path.isdir(file):
                        shutil.rmtree(file)
                    else:
                        os.remove(file)

                    f.write(f"{time.strftime('%d. %m. %Y')} {file} removed permanently\n")

            except Exception as e:
                f.write(f"{time.strftime('%d. %m. %Y')} {e}\n")




def start_in_new_session(process, args, quiet=True):
    pid = os.fork()
    if pid == 0:
        os.setsid()
        if quiet:
            with open(os.devnull, "w") as f:
                os.dup2(f.fileno(), 1)
                os.dup2(f.fileno(), 2)

        os.execvp(process, [process] + list(args))
