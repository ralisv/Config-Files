#!/usr/bin/env python3

import json
import subprocess
from dataclasses import dataclass
from math import ceil
from pathlib import Path
from time import sleep

from utils import send_notification, update_eww

EWW_CONFIG_PATH = Path("~/Config-Files/hyprland/eww").expanduser()
BLOCKS = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

LOG_PREFIX = "audio-monitor: "


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


@dataclass
class AudioState:
    sink: AudioDevice
    source: AudioDevice


def log(message: str):
    """Log a message with a predefined prefix."""
    print(f"{LOG_PREFIX}{message}")


def get_audio_devices() -> list[AudioDevice]:
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


def get_default_device(device_type):
    cmd = ["pactl", f"get-default-{device_type}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def update_eww_variables(audio: AudioState):
    update_eww(
        {
            f"sink-settings": f"♫ {format_device_info(audio.sink)}",
            f"source-settings": f"🎙 {format_device_info(audio.source)}",
        }
    )


def format_device_info(device: AudioDevice) -> str:
    if device is None:
        return "N/A"

    volume = int(next(iter(device.volume.values())).value_percent[:-1])
    volume_string = (
        "".join(BLOCKS[: ceil(volume / 18)]).ljust(8, " ")
        if not device.mute
        else "  MUTE  "
    )

    cropped_description = (
        device.description[:27].ljust(30, ".")
        if len(device.description) > 30
        else device.description
    )

    return f"{cropped_description}: [{volume_string}]"


def get_sound_settings() -> AudioState:
    default_source = get_default_device("source")
    default_sink = get_default_device("sink")

    audio_devices = get_audio_devices()
    source = next(
        (device for device in audio_devices if device.name == default_source),
        None,
    )
    sink = next(
        (device for device in audio_devices if device.name == default_sink),
        None,
    )

    return AudioState(sink=sink, source=source)  # type: ignore


def audio_monitor():
    process = subprocess.Popen(
        ["pactl", "subscribe"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    log("Monitoring for audio changes...")

    audio = get_sound_settings()

    if None in (audio.sink, audio.source):
        sleep(2)
        audio = get_sound_settings()

    update_eww_variables(audio)

    try:
        while True:
            line = process.stdout.readline()  # type: ignore
            if not line:
                break

            if "change" not in line:
                continue

            try:
                new_audio = get_sound_settings()

                if new_audio != audio:
                    if new_audio.source.name != audio.source.name:
                        send_notification(
                            "normal",
                            5000,
                            "Audio source device changed",
                            new_audio.source.description,
                        )
                        log(f"Audio source device changed")
                    if new_audio.sink.name != audio.sink.name:
                        send_notification(
                            "normal",
                            5000,
                            "Audio sink device changed",
                            new_audio.sink.description,
                        )
                        log(f"Audio sink device changed")

                    audio = new_audio
                    update_eww_variables(audio)

            except Exception as e:
                log(f"Error updating audio devices: {e}")

    except KeyboardInterrupt:
        log("Monitoring stopped.")

    finally:
        process.terminate()


if __name__ == "__main__":
    audio_monitor()
