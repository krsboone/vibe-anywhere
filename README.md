# vibe-anywhere

Send prompts to Claude Code from anywhere — phone, tablet, or any browser — via a password-gated web interface and ntfy.sh.

## How it works

```
yoursite.com/vibe-sender  →  ntfy.sh topic  →  listener.py  →  claude -p "..."
     (browser)               (relay)           (this repo)     (local machine)
```

1. You open `yoursite.com/vibe-sender` on your phone, enter your password, pick a project, type a prompt
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
| `NTFY_TOPIC` | `your-private-topic` | The ntfy.sh topic to subscribe to. Ensure it's something that can never be guessed |
| `DIR_PROJECT1` | `/path/to/project/repo1` | Local path for repo1 |
| `DIR_PROJECT2` | `/path/to/project/repo1` | Local path for repo2 |

## Running

```bash
python listener.py
```

Leave it running in a terminal or tmux session. It reconnects automatically if the stream drops.

## Adding a project

1. Add a new entry to `PROJECTS` in `listener.py`
2. Add the corresponding `DIR_*` variable to `.env.example` and your `.env`
3. Add the project as a radio button option in `vibe.php` on yoursite.com
4. Grant Claude Code permission to act in that project — see below

## Permissions

`claude -p` runs non-interactively, so it cannot prompt for the usual tool
permissions (Write, Edit, Bash). Without an explicit grant, Claude will
report that it needs permission and stop without making any changes.

For each project you want vibe-anywhere to be able to modify, copy
[`examples/settings.local.json.example`](examples/settings.local.json.example)
to `.claude/settings.local.json` in that project's repo and add
`.claude/settings.local.json` to that repo's `.gitignore`. This grants a
scoped allowlist (file edits + git add/commit/push) rather than bypassing
permissions entirely.

Only grant this in repos you're comfortable having modified and pushed to
unattended — start with the minimum allowlist needed and add to it
deliberately.

### Trusting the project directory

Claude Code only honors a project's `.claude/settings.local.json` in
directories it has been told to trust. `claude -p` runs non-interactively
and can't show the "Do you trust the files in this folder?" prompt, so if a
project directory has never been opened in Claude Code before, `-p` falls
back to a restricted mode and ignores the allowlist — even if it's present.

For each project directory, do this once, interactively:

```bash
cd /path/to/project && claude
```

Accept the trust prompt, then exit (`/exit` or Ctrl+D). After that,
`claude -p` invocations from `listener.py` will pick up
`.claude/settings.local.json` for that directory.

## Sender

Add `remote-sender/vibe-sender-example.php` to your site after updating `$allowed`, `'topic'`.

NOTE: all user supplied values will need to be collected then sent to this script in a manner similar to:
```
const res  = await fetch('remote-sender/vibe-sender-example.php', { method: 'POST', body: new FormData(form) });
```
Access to these files should be gated, this is your responsibility! 
The ntfy.sh topic is shared between the two repos; the sender publishes, this listener subscribes.
