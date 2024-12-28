#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path
from time import sleep
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, TypeAdapter
from utils import send_notification, update_eww


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
    feature_indicators: list[str]


class DisconnectedDetails(BaseModel):
    location: Optional[Location]
    locked_down: bool


class ErrorCause(BaseModel):
    reason: str


class ErrorDetails(BaseModel):
    cause: ErrorCause
    block_failure: Optional[str]


class ConnectedStatus(BaseModel):
    state: Literal["connected"]
    details: ConnectedDetails


class DisconnectedStatus(BaseModel):
    state: Literal["disconnected"]
    details: DisconnectedDetails


class ErrorStatus(BaseModel):
    state: Literal["error"]
    details: ErrorDetails


class ConnectingStatus(BaseModel):
    state: Literal["connecting"]


class DisconnectingStatus(BaseModel):
    state: Literal["disconnecting"]


MullvadStatus = Annotated[
    Union[
        ConnectedStatus,
        DisconnectedStatus,
        ErrorStatus,
        ConnectingStatus,
        DisconnectingStatus,
    ],
    Field(discriminator="state"),
]


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
    # Parse the JSON string into a dictionary first
    data_dict = json.loads(json_data)

    parse_status = TypeAdapter(MullvadStatus).validate_python

    return parse_status(data_dict)


def format_status_for_eww(status: MullvadStatus) -> str:
    match status:
        case ConnectedStatus(
            details=ConnectedDetails(
                location=Location(city=city, country=country, ipv4=ipv4, ipv6=ipv6)
            )
        ):
            ip = ipv4 or ipv6 or "N/A"
            return f"Connected: {city}, {country} [{ip}]"
        case ConnectingStatus():
            return "Connecting..."
        case DisconnectedStatus(
            details=DisconnectedDetails(
                location=Location(city=city, country=country, ipv4=ipv4, ipv6=ipv6)
            )
        ):
            ip = ipv4 or ipv6 or "N/A"
            return f"Disconnected: {city}, {country} [{ip}]"
        case DisconnectedStatus():
            return "Disconnected"
        case DisconnectingStatus():
            return "Disconnecting..."
        case ErrorStatus(details=ErrorDetails(cause=ErrorCause(reason="is_offline"))):
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
    prev_status: Optional[MullvadStatus] = None

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

                if prev_status is not None and status.state != prev_status.state:
                    send_notification(
                        "normal", 5_000, "VPN status change", f"New state: {status.state}"
                    )

                prev_status = status

            except subprocess.CalledProcessError as e:
                log(f"Error parsing JSON output or updating status: {e}")

    except KeyboardInterrupt:
        log("Monitoring stopped.")

    finally:
        process.terminate()


if __name__ == "__main__":
    vpn_monitor()
