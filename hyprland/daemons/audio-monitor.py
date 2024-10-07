#!/usr/bin/env python3

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

EWW_CONFIG_PATH = Path("~/Config-Files/hyprland/eww").expanduser()

@dataclass
class Volume:
    value: int
    value_percent: str
    db: str

@dataclass
class AudioDevice:
    state: str
    name: str
    description: str
    channel_map: list[str]
    mute: bool
    volume: dict[str, Volume]

def get_audio_devices() -> list[AudioDevice]:
    try:
        sources = subprocess.run(
            ["pactl", "--format=json", "list", "sources"],
            capture_output=True,
            text=True,
        )
        sinks = subprocess.run(
            ["pactl", "--format=json", "list", "sinks"], capture_output=True, text=True
        )

        sources_json = json.loads(sources.stdout)
        sinks_json = json.loads(sinks.stdout)

        audio_devices = []

        for device in sources_json + sinks_json:
            volume_dict = {}
            for channel, vol in device.get("volume", {}).items():
                volume_dict[channel] = Volume(
                    value=vol.get("value", 0),
                    value_percent=vol.get("value_percent", "0%"),
                    db=vol.get("db", "0 dB"),
                )

            audio_device = AudioDevice(
                state=device.get("state", ""),
                name=device.get("name", ""),
                description=device.get("description", ""),
                channel_map=device.get("channel_map", []),
                mute=device.get("mute", False),
                volume=volume_dict,
            )
            audio_devices.append(audio_device)

        return audio_devices

    except subprocess.CalledProcessError as e:
        print(f"Error running pactl command: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output: {e}")
        return []

def get_default_device(device_type):
    cmd = ["pactl", f"get-default-{device_type}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def update_eww_sound_settings(sink: str, source: str):
    subprocess.run(
        [
            "eww",
            "--config",
            EWW_CONFIG_PATH.as_posix(),
            "update",
            f"sink-settings={sink}",
            f"source-settings={source}",
        ],
        check=True,
    )

def format_device_info(device):
    if device is None:
        return "N/A"

    volume = next(iter(device.volume.values())).value_percent
    return f"{device.description}, Volume: {volume}{" [MUTED]" if device.mute else ""}"

def main():
    process = subprocess.Popen(
        ["pactl", "subscribe"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    print("Monitoring for audio changes...")

    source_info = "..."
    sink_info = "..."

    try:
        while True:
            # Execute the loop body once at the beginning
            try:
                default_source = get_default_device("source")
                default_sink = get_default_device("sink")

                audio_devices = get_audio_devices()
                source = next(
                    (
                        device
                        for device in audio_devices
                        if device.name == default_source
                    ),
                    None,
                )
                sink = next(
                    (device for device in audio_devices if device.name == default_sink),
                    None,
                )

                new_source_info = "Source: " + format_device_info(source)
                new_sink_info = "Sink: " + format_device_info(sink)

                if new_source_info != source_info or new_sink_info != sink_info:
                    source_info = new_source_info
                    sink_info = new_sink_info

                    update_eww_sound_settings(sink_info, source_info)

                    print(f"{source_info} | {sink_info}")

            except Exception as e:
                print(f"Error updating audio devices: {e}")

            # Now wait for the next line from the process
            line = process.stdout.readline()
            if not line:
                break
            if "change" not in line:
                continue

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    finally:
        process.terminate()

if __name__ == "__main__":
    main()
