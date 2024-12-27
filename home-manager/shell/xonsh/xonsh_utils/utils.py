import os
import subprocess
from pathlib import Path

from tabulate import tabulate  # type: ignore # pylint: disable=import-error
from xonsh_utils.colors import (  # pylint: disable=import-error
    GIT_STATUS_COLORS,
    GIT_STATUS_COLORS_STAGED,
    Color,
    Style,
    colorize_filename,
)

GIT_STATUS_VERBOSE: dict[str, str] = {
    "M": "Modified",
    "MM": "Modified after staged",
    "A": "Added",
    "D": "Deleted",
    "R": "Renamed",
    "C": "Copied",
    "U": "Unmerged",
    "??": "Untracked",
    "DU": "Unmerged, both deleted",
    "AU": "Unmerged, added by us",
    "UD": "Unmerged, deleted by them",
    "UA": "Unmerged, added by them",
    "DA": "Unmerged, deleted by us",
    "AA": "Unmerged, both added",
    "UU": "Unmerged, both modified",
    "AD": "Unmerged, added by us, deleted by them",
}
""" A dictionary mapping git status codes to verbose descriptions """


def super_git_status() -> str:
    """
    Returns a string containing git status in super colorful format

    The paths of dirty files are relative to the current working directory.

    Returns:
        str: git status
    """
    # Get root directory of the git repository
    git_revparse = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )

    # When not in a git repository, return empty string
    if git_revparse.returncode != 0:
        return ""

    repo_root = Path(git_revparse.stdout.strip())

    # Get the git status in short format
    git_status = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
    )

    # When git status reports no changes, return empty string
    if git_status.stdout == "":
        return ""

    # Get the staged files
    git_diff = subprocess.run(
        ["git", "diff", "--name-only", "--cached"],
        capture_output=True,
        text=True,
        check=True,
    )

    staged_files = set(git_diff.stdout.splitlines())

    file_states = [line.split() for line in git_status.stdout.split("\n") if line]

    # When too many files were received from git status
    if len(file_states) > 1000:
        return f"{Color.RED}Super git status error: TooManyEntries ({len(file_states)})"

    # Create the table
    table_data: list[tuple[str, str, str]] = []
    for state, *_, filename in file_states:
        state_color = (
            GIT_STATUS_COLORS
            if filename not in staged_files
            else GIT_STATUS_COLORS_STAGED
        ).get(state, Style.DEFAULT)

        # Get the relative path to the file
        file_path = os.path.relpath(repo_root / filename, Path.cwd())

        verbose_state = GIT_STATUS_VERBOSE.get(state, "")

        table_data.append(
            (
                f"{state_color}{state}",
                f"{state_color}{verbose_state}",
                colorize_filename(file_path),
            )
        )

    return tabulate(table_data, tablefmt="plain") + "\n"
