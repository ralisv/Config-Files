#!/usr/bin/env python3

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import List, Literal, Optional

from utils import update_eww


@dataclass
class Endpoint:
    address: str
    protocol: str
    tunnel_type: str
    quantum_resistant: bool
    proxy: Optional[str]
    obfuscation: Optional[str]
    entry_endpoint: Optional[str]
    tunnel_interface: Optional[str]
    daita: bool


@dataclass
class Location:
    ipv4: Optional[str]
    ipv6: Optional[str]
    country: str
    city: str
    latitude: float
    longitude: float
    mullvad_exit_ip: bool
    hostname: Optional[str]
    bridge_hostname: Optional[str]
    entry_hostname: Optional[str]
    obfuscator_hostname: Optional[str]


@dataclass
class ConnectedDetails:
    endpoint: Endpoint
    location: Location
    feature_indicators: List[str]


@dataclass
class DisconnectedDetails:
    location: Optional[Location]
    locked_down: bool


@dataclass
class ErrorCause:
    reason: str


@dataclass
class ErrorDetails:
    cause: ErrorCause
    block_failure: str | None


@dataclass
class MullvadStatus:
    state: str
    details: Optional[
        ConnectedDetails | DisconnectedDetails | Literal["nothing"] | ErrorDetails
    ]


EWW_CONFIG = Path("~/Config-Files/hyprland/eww").expanduser()

LOG_PREFIX = "vpn-monitor: "


def get_mullvad_status_manual() -> MullvadStatus:
    process = subprocess.Popen(
        ["mullvad", "status", "--json", "listen"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1,  # Line buffered
    )

    return parse_mullvad_status(json.loads(process.stdout.readline().strip()))  # type: ignore


def parse_mullvad_status(json_data: dict) -> MullvadStatus:
    state = json_data.get("state", "disconnected")
    details = json_data.get("details", "nothing")

    if state == "disconnected":
        if isinstance(details, dict):
            location = (
                Location(**details["location"]) if details.get("location") else None
            )
            disconnected_details = DisconnectedDetails(
                location=location, locked_down=details.get("locked_down", False)
            )
            return MullvadStatus(state=state, details=disconnected_details)
        else:
            return MullvadStatus(state=state, details=None)

    if state in ["connected", "connecting"]:
        endpoint = Endpoint(**details["endpoint"])
        location = Location(**details["location"])
        connected_details = ConnectedDetails(
            endpoint=endpoint,
            location=location,
            feature_indicators=details.get("feature_indicators", []),
        )
        return MullvadStatus(state=state, details=connected_details)

    elif state == "error":
        return MullvadStatus(
            state=state,
            details=ErrorDetails(
                cause=ErrorCause(**details["cause"]),
                block_failure=details.get("block_failure"),
            ),
        )
    else:
        return MullvadStatus(state=state, details=details)


def format_status_for_eww(status: MullvadStatus) -> str:
    if status.state == "connected" and isinstance(status.details, ConnectedDetails):
        ip = status.details.location.ipv4 or status.details.location.ipv6 or "N/A"
        return f"Connected: {status.details.location.city}, {status.details.location.country} [{ip}]"
    elif status.state == "connecting":
        return "Connecting..."
    elif status.state == "disconnected":
        if isinstance(status.details, DisconnectedDetails) and status.details.location:
            ip = status.details.location.ipv4 or status.details.location.ipv6 or "N/A"
            return f"Disconnected: {status.details.location.city}, {status.details.location.country} [{ip}]"
        else:
            return "Disconnected"
    elif status.state == "disconnecting":
        return "Disconnecting..."
    elif (
        status.state == "error"
        and isinstance(status.details, ErrorDetails)
        and status.details.cause.reason == "is_offline"
    ):
        return "Offline"
    else:
        return f"Unknown status: {status}"


def vpn_monitor():
    process = subprocess.Popen(
        ["mullvad", "status", "--json", "listen"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1,  # Line buffered
    )

    print(f"{LOG_PREFIX} monitoring Mullvad VPN status...")

    try:
        for line in iter(process.stdout.readline, ""):  # type: ignore
            try:
                status = parse_mullvad_status(json.loads(line.strip()))
                print(f"{LOG_PREFIX} status: {status.state}")
                update_eww({"vpn-status": format_status_for_eww(status)})

                if status.state == "disconnected":
                    print(f"{LOG_PREFIX} vpn in disconnected state. Retry in 1 second.")
                    sleep(1)

                    status = get_mullvad_status_manual()
                    print(f"{LOG_PREFIX} status: {status.state}")
                    update_eww({"vpn-status": format_status_for_eww(status)})

            except json.JSONDecodeError:
                print(f"{LOG_PREFIX} error parsing JSON output")

    except KeyboardInterrupt:
        print(f"{LOG_PREFIX} monitoring stopped.")
    finally:
        process.terminate()


if __name__ == "__main__":
    vpn_monitor()
