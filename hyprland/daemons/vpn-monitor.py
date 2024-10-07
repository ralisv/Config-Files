#!/usr/bin/env python3

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional


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
class MullvadStatus:
    state: str
    details: Optional[ConnectedDetails | DisconnectedDetails | Literal["nothing"]]


EWW_CONFIG = Path("~/Config-Files/hyprland/eww").expanduser()


def update_eww(status_report: str) -> None:
    subprocess.run(
        [
            "eww",
            "--config",
            EWW_CONFIG.as_posix(),
            "update",
            f"vpn-status={status_report}",
        ]
    )


def parse_mullvad_status(json_data: dict) -> MullvadStatus:
    state = json_data.get("state", "disconnected")
    details = json_data.get("details", "nothing")

    if state in ["connected", "connecting"]:
        endpoint = Endpoint(**details["endpoint"])
        location = Location(**details["location"])
        connected_details = ConnectedDetails(
            endpoint=endpoint,
            location=location,
            feature_indicators=details.get("feature_indicators", []),
        )
        return MullvadStatus(state=state, details=connected_details)
    elif state == "disconnected":
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
    else:
        return f"Unknown state: {status.state}"


def run_mullvad_status():
    process = subprocess.Popen(
        ["mullvad", "status", "--json", "listen"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1,  # Line buffered
    )

    print("Monitoring Mullvad VPN status...")
    print("Press Ctrl+C to stop.")

    try:
        for line in iter(process.stdout.readline, ""):  # type: ignore
            try:
                status_dict = json.loads(line.strip())
                status = parse_mullvad_status(status_dict)
                print(f"State: {status.state}")

                eww_status = format_status_for_eww(status)
                update_eww(eww_status)
                print(f"Updated eww variable: {eww_status}")

                if isinstance(status.details, ConnectedDetails):
                    ip = (
                        status.details.location.ipv4
                        or status.details.location.ipv6
                        or "N/A"
                    )
                    print(
                        f"Connected to: {status.details.location.city}, {status.details.location.country}"
                    )
                    print(f"IP address: {ip}")
                    print(f"Features: {', '.join(status.details.feature_indicators)}")
                elif isinstance(status.details, DisconnectedDetails):
                    if status.details.location:
                        ip = (
                            status.details.location.ipv4
                            or status.details.location.ipv6
                            or "N/A"
                        )
                        print(
                            f"Current location: {status.details.location.city}, {status.details.location.country}"
                        )
                        print(f"IP address: {ip}")
                    print(f"Locked down: {status.details.locked_down}")
                elif isinstance(status.details, str):
                    print(f"Details: {status.details}")

                print("-" * 30)
            except json.JSONDecodeError:
                print("Error parsing JSON output")

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    finally:
        process.terminate()


if __name__ == "__main__":
    run_mullvad_status()
