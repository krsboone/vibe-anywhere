# vibe-anywhere

Send prompts to Claude Code from anywhere — phone, tablet, or any browser — via a password-gated web interface and ntfy.sh.

## How it works

```
krisboone.com/vibe  →  ntfy.sh topic  →  listener.py  →  claude -p "..."
     (browser)             (relay)          (this repo)      (local machine)
```

1. You open `krisboone.com/vibe` on your phone, enter your password, pick a project, type a prompt
2. The page publishes a JSON command to a private ntfy.sh topic
3. `listener.py` (running on your local machine) receives it via a persistent HTTP stream
4. It invokes `claude -p` in the matching project directory

## Setup

```bash
cp .env.example .env
# edit .env with your project paths if they differ from the defaults
pip install -r requirements.txt
```

## Configuration

`.env` — all values have sensible defaults, override as needed:

| Variable | Default | Description |
|---|---|---|
| `NTFY_TOPIC` | `your-private-topic` | The ntfy.sh topic to subscribe to |
| `DIR_KRISBOONE` | `/Users/kris/Coding/krisboone` | Local path for krisboone.com |
| `DIR_STEPSTOOLSPORTS` | `/Users/kris/Coding/stepstoolsports` | Local path for stepstoolsports.com |

## Running

```bash
python listener.py
```

Leave it running in a terminal or tmux session. It reconnects automatically if the stream drops.

## Adding a project

1. Add a new entry to `PROJECTS` in `listener.py`
2. Add the corresponding `DIR_*` variable to `.env.example` and your `.env`
3. Add the project as a radio button option in `vibe.php` on krisboone.com

## Sender

The web interface lives in the `krisboone.com` repo — `vibe.php` + `api/vibe_send.php`. The ntfy.sh topic is shared between the two repos; the sender publishes, this listener subscribes.
