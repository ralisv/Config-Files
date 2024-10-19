#!/usr/bin/env python3

import subprocess
from math import ceil
from pathlib import Path
from time import sleep
from typing import Dict, List

from pydantic import BaseModel, TypeAdapter, field_validator, validator

from utils import send_notification, update_eww

EWW_CONFIG_PATH = Path("~/Config-Files/hyprland/eww").expanduser()
BLOCKS = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

LOG_PREFIX = "audio-monitor: "


class Volume(BaseModel):
    value: int
    value_percent: str
    db: str


class AudioDevice(BaseModel):
    state: str
    name: str
    description: str
    channel_map: list[str]
    mute: bool
    volume: Dict[str, Volume]

    @field_validator("channel_map", mode="before")
    def split_channel_map(cls, value):
        # Check if the value is a string and split it into a list
        if isinstance(value, str):
            return [element.strip() for element in value.split(",")]
        return value


class AudioState(BaseModel):
    sink: AudioDevice
    source: AudioDevice


def log(message: str):
    """Log a message with a predefined prefix."""
    print(f"{LOG_PREFIX}{message}")


def get_audio_devices() -> List[AudioDevice]:
    sources = subprocess.run(
        ["pactl", "--format=json", "list", "sources"],
        capture_output=True,
        text=True,
    ).stdout
    sinks = subprocess.run(
        ["pactl", "--format=json", "list", "sinks"], capture_output=True, text=True
    ).stdout

    parse_devices = TypeAdapter(list[AudioDevice]).validate_json
    return parse_devices(sources) + parse_devices(sinks)


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
                        log(f"Audio source device changed {new_audio.source}")

                    if new_audio.sink.name != audio.sink.name:
                        send_notification(
                            "normal",
                            5000,
                            "Audio sink device changed",
                            new_audio.sink.description,
                        )
                        log(f"Audio sink device changed {new_audio.sink}")

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
