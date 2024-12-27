import subprocess


def send_notification(urgency: str, timeout: int, title: str, body: str) -> None:
    """Send a notification using notify-send.

    Args:
        urgency (str): urgency level of the notification
        timeout (int): time in milliseconds to show the notification
        title (str): title of the notification
        body (str): body of the notification
    """
    subprocess.run(["notify-send", "-u", urgency, "-t", str(timeout), title, body])


def update_eww(toUpdate: dict[str, str]) -> None:
    """Update eww variables.

    Args:
        toUpdate (dict[str, str]): dictionary of [variable name]:[value] pairs to update
    """
    subprocess.run(
        [
            "eww",
            "update",
            *(f"{key}={value}" for key, value in toUpdate.items()),
        ]
    )
