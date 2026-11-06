# Claude Usage for GNOME

GNOME Shell extension that shows how much of your Claude plan you have used in the top bar: the 5-hour limit and the weekly limit (`5h 12% · 7d 40%`).

- Each value turns orange from 80% and red from 90%, with a notification when each threshold is crossed (once per period).
- The menu shows when each limit resets.
- Refreshes every 5 minutes. With no connection or an expired login, it shows the last known value dimmed.

## How it works

The `claude_usage.py` script (installed as `claude-usage`) reads the login the Claude app / Claude Code keeps in `~/.claude/.credentials.json` and queries the same endpoint used by the `/usage` command. The script never refreshes or prints the token; the app itself refreshes it.

> The endpoint is undocumented and may change without notice.

## Install

```bash
./build-deb.sh            # builds dist/gnome-claude-usage_1.0.0_all.deb
sudo apt install ./dist/gnome-claude-usage_1.0.0_all.deb
gnome-extensions enable claude-usage@local
```

Restart GNOME Shell (X11: Alt+F2, `r`, Enter; Wayland: log out and back in).

For another version: `./build-deb.sh 1.1.0`.

## Requirements

- GNOME Shell 45 to 49
- Python 3
- Logged in to the Claude app or Claude Code
