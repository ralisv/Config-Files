import json
import subprocess


def main():
    cmd = "pw-dump -m | jq -c '.'"
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
    )

    try:
        for line in iter(process.stdout.readline, ""):  # type: ignore
            try:
                data = json.loads(line.strip())
                print("Change detected")
            except json.JSONDecodeError:
                print("Error parsing JSON output")

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    finally:
        process.terminate()


if __name__ == "__main__":
    main()
