#!/usr/bin/env python3
import json
import os
import subprocess
import time

import requests
from dotenv import load_dotenv

load_dotenv()

TOPIC = os.getenv("NTFY_TOPIC", "your-private-topic")

PROJECTS = {
    "krisboone":       os.getenv("DIR_KRISBOONE",       "/Users/kris/Coding/krisboone"),
    "stepstoolsports": os.getenv("DIR_STEPSTOOLSPORTS", "/Users/kris/Coding/stepstoolsports"),
}


def handle(message_text: str) -> None:
    try:
        payload = json.loads(message_text)
    except json.JSONDecodeError:
        print(f"[skip] non-JSON: {message_text!r}")
        return

    project = payload.get("project", "")
    prompt  = payload.get("prompt", "").strip()

    if not project or not prompt:
        print("[skip] missing project or prompt")
        return

    cwd = PROJECTS.get(project)
    if not cwd:
        print(f"[skip] unknown project: {project!r}")
        return

    print(f"[{project}] {prompt[:100]}")
    subprocess.run(["claude", "-p", prompt], cwd=cwd)


def listen() -> None:
    url = f"https://ntfy.sh/{TOPIC}/json"
    print(f"Listening on ntfy.sh/{TOPIC} …")

    while True:
        try:
            with requests.get(url, stream=True, timeout=(10, None)) as r:
                for raw in r.iter_lines():
                    if not raw:
                        continue
                    try:
                        event = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    if event.get("event") == "message":
                        handle(event.get("message", ""))
        except Exception as e:
            print(f"[error] {e} — reconnecting in 5 s …")
            time.sleep(5)


if __name__ == "__main__":
    listen()
