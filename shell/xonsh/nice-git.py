#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from utils import super_git_status


def main():
    git_status = super_git_status()
    if git_status.strip():
        print(git_status)


if __name__ == "__main__":
    main()
