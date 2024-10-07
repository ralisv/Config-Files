import json
import re
import subprocess
from dataclasses import dataclass


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
        # Run the pactl command for both sources and sinks
        sources = subprocess.run(
            ["pactl", "--format=json", "list", "sources"],
            capture_output=True,
            text=True,
        )
        sinks = subprocess.run(
            ["pactl", "--format=json", "list", "sinks"], capture_output=True, text=True
        )

        # Combine and parse the JSON output
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


def print_audio_state(state):
    print("\nCurrent Audio State:")
    print(f"Sink (Output): {state.sink.name}")
    print(f"  Volume: {state.sink.volume}%")
    print(f"  Muted: {'Yes' if state.sink.muted else 'No'}")
    print(f"Source (Input): {state.source.name}")
    print(f"  Volume: {state.source.volume}%")
    print(f"  Muted: {'Yes' if state.source.muted else 'No'}")


def main():
    process = subprocess.Popen(
        ["pactl", "subscribe"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    print("Monitoring for audio changes...")

    try:
        for line in iter(process.stdout.readline, ""):  # type: ignore
            if "change" not in line:
                continue

            try:
                default_source = get_default_device("source")
                default_sink = get_default_device("sink")

                audio_devices = get_audio_devices()
                # Find the default source and sink
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

            except Exception as e:
                print(f"Error getting audio devices: {e}")
                continue

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    finally:
        process.terminate()


if __name__ == "__main__":
    main()
