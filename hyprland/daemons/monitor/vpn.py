#!/usr/bin/env python3

import subprocess
from pathlib import Path
from time import sleep
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from utils import update_eww


class Endpoint(BaseModel):
    address: str
    protocol: str
    tunnel_type: str
    quantum_resistant: bool
    proxy: Optional[str]
    obfuscation: Optional[str]
    entry_endpoint: Optional[str]
    tunnel_interface: Optional[str]
    daita: bool


class Location(BaseModel):
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


class ConnectedDetails(BaseModel):
    endpoint: Endpoint
    location: Location
    feature_indicators: List[str]


class DisconnectedDetails(BaseModel):
    location: Optional[Location]
    locked_down: bool


class ErrorCause(BaseModel):
    reason: str


class ErrorDetails(BaseModel):
    cause: ErrorCause
    block_failure: Optional[str]


class MullvadStatus(BaseModel):
    state: str
    details: (
        ConnectedDetails
        | DisconnectedDetails
        | Literal["nothing"]
        | ErrorDetails
        | Literal["reconnect"]
    )


EWW_CONFIG = Path("~/Config-Files/hyprland/eww").expanduser()

LOG_PREFIX = "vpn-monitor: "


def log(message: str):
    """Log a message with a predefined prefix."""
    print(f"{LOG_PREFIX}{message}")


def get_mullvad_status_manual() -> MullvadStatus:
    process = subprocess.Popen(
        ["mullvad", "status", "--json", "listen"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1,  # Line buffered
    )

    return parse_mullvad_status(process.stdout.readline().strip())  # type: ignore


def parse_mullvad_status(json_data: str) -> MullvadStatus:
    return MullvadStatus.model_validate_json(json_data)


def format_status_for_eww(status: MullvadStatus) -> str:
    match status.state:
        case "connected" if isinstance(status.details, ConnectedDetails):
            ip = status.details.location.ipv4 or status.details.location.ipv6 or "N/A"
            return f"Connected: {status.details.location.city}, {status.details.location.country} [{ip}]"
        case "connecting":
            return "Connecting..."
        case "disconnected":
            if (
                isinstance(status.details, DisconnectedDetails)
                and status.details.location
            ):
                ip = (
                    status.details.location.ipv4
                    or status.details.location.ipv6
                    or "N/A"
                )
                return f"Disconnected: {status.details.location.city}, {status.details.location.country} [{ip}]"
            else:
                return "Disconnected"
        case "disconnecting":
            return "Disconnecting..."
        case "error" if isinstance(
            status.details, ErrorDetails
        ) and status.details.cause.reason == "is_offline":
            return "Offline"
        case _:
            return f"Unknown status: {status}"


def vpn_monitor():
    process = subprocess.Popen(
        ["mullvad", "status", "--json", "listen"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1,  # Line buffered
    )

    log("Monitoring Mullvad VPN status...")

    try:
        for line in iter(process.stdout.readline, ""):  # type: ignore
            try:
                status = parse_mullvad_status(line.strip())
                log(f"Status: {status.state}")
                update_eww({"vpn-status": format_status_for_eww(status)})

                if status.state == "disconnected":
                    log("VPN in disconnected state. Retry in 1 second.")
                    sleep(1)

                    status = get_mullvad_status_manual()
                    log(f"Status after retrying manually: {status.state}")
                    update_eww({"vpn-status": format_status_for_eww(status)})

            except Exception as e:
                log(f"Error parsing JSON output or updating status: {e}")

    except KeyboardInterrupt:
        log("Monitoring stopped.")

    finally:
        process.terminate()


if __name__ == "__main__":
    vpn_monitor()
