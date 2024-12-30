import logging
import subprocess
from dataclasses import dataclass
from math import ceil
from pathlib import Path
from time import sleep
from typing import Dict, List, Optional

from pydantic import BaseModel, TypeAdapter, field_validator
from utils import send_notification, update_eww

logger = logging.getLogger("audio_monitor")

EWW_CONFIG_PATH = Path("~/Config-Files/hyprland/eww").expanduser()
BLOCKS = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]


class Volume(BaseModel):
    """Volume information for an audio device."""

    value: int
    value_percent: str
    db: str


class AudioDevice(BaseModel):
    """Information about an audio device."""

    state: str
    name: str
    description: str
    channel_map: list[str]
    mute: bool
    volume: Dict[str, Volume]

    @field_validator("channel_map", mode="before")
    def split_channel_map(cls, value) -> list[str]:  # pylint: disable=no-self-argument
        """Split the channel map string into a list of channels."""
        if isinstance(value, str):
            return [element.strip() for element in value.split(",")]
        return value


@dataclass
class AudioState:
    """State of the audio devices."""

    sink: AudioDevice
    source: AudioDevice


def get_audio_devices() -> List[AudioDevice]:
    """Get the list of audio devices."""
    sources = subprocess.run(
        ["pactl", "--format=json", "list", "sources"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    sinks = subprocess.run(
        ["pactl", "--format=json", "list", "sinks"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    parse_devices = TypeAdapter(list[AudioDevice]).validate_json
    return parse_devices(sources) + parse_devices(sinks)


def get_default_device(device_type) -> str:
    """Get the default audio device of the specified type."""
    cmd = ["pactl", f"get-default-{device_type}"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def update_eww_variables(audio: AudioState) -> None:
    """Update the Eww variables with the audio device information."""
    update_eww(
        {
            "sink-settings": f"♫ {format_device_info(audio.sink)}",
            "source-settings": f"🎙 {format_device_info(audio.source)}",
        }
    )


def format_device_info(device: Optional[AudioDevice]) -> str:
    """Format the audio device information for display."""
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
    """Get the current sound settings"""
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

    if source is None or sink is None:
        raise ValueError("Could not find default audio devices.")

    return AudioState(sink=sink, source=source)  # type: ignore


def audio_monitor() -> None:
    """Monitor audio devices for changes."""
    process = subprocess.Popen(
        ["pactl", "subscribe"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    logger.info("Monitoring for audio changes...")
    try:
        audio = get_sound_settings()
    except (ValueError, subprocess.CalledProcessError) as e:
        logger.error("Error getting audio devices: %s", e)
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
                        logger.info("Audio source device changed: %s", new_audio.source)

                    if new_audio.sink.name != audio.sink.name:
                        send_notification(
                            "normal",
                            5000,
                            "Audio sink device changed",
                            new_audio.sink.description,
                        )
                        logger.info("Audio sink device changed: %s", new_audio.sink)

                    audio = new_audio
                    update_eww_variables(audio)

            except subprocess.CalledProcessError as e:
                logger.error("Error while updating audio devices: %s", e)

    except KeyboardInterrupt:
        logger.info("Monitoring stopped.")

    finally:
        process.terminate()


if __name__ == "__main__":
    audio_monitor()
