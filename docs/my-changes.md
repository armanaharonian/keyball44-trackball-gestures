# My changes

Every change made to this setup, newest first. Add a line here each time something changes.

## 2026-11-10: Ball moves between herdr panes (automatic)

- **What:** while Ghostty (the terminal that runs herdr) is the front app, rolling the ball with no key held moves focus between herdr panes: right, left, down, up. In every other app the ball still does Cmd+Tab.
- **How:** `tools/herdr-watch.py` checks the front app and sends one raw-HID message (`0x7E`, on or off) to the keyboard. The firmware (`keymap/keymap.c`, `herdr_panes`) then taps `ctrl+alt+h/j/k/l` per `HERDR_PANE_STEP` (150) counts of travel. Herdr maps those chords to `focus_pane_*` in `~/.config/herdr/config.toml`.
- **Limit:** the watcher knows the app, not the pane. Any Ghostty window counts as herdr mode.
- **Needs:** firmware flashed (`./flash.sh`, after saving your layout in Vial), and the watcher running. Install it with `sed "s|__REPO__|$PWD|g" tools/com.armanaharonian.herdr-watch.plist > ~/Library/LaunchAgents/com.armanaharonian.herdr-watch.plist && launchctl load ~/Library/LaunchAgents/com.armanaharonian.herdr-watch.plist`. macOS asks once to let it control System Events.
- **Status:** firmware flashed and verified (`would change 0 entries`). The keyboard answers the mode message. Watcher installed as a LaunchAgent (`com.armanaharonian.herdr-watch`). Not yet tested by rolling the ball in herdr.
- **Undo:** `launchctl unload` the plist, remove it, and reflash without `herdr_panes`.

## 2026-11-10: herdr Ctrl+W closes the pane

- **What:** `close_pane = ["prefix+x", "ctrl+w"]` in `~/.config/herdr/config.toml`. `Ctrl+W` no longer deletes a word inside a pane. Backups: `config.toml.bak3`, `config.toml.bak4`.

## 2026-11-10: Control moves to hold-G

- **What:** the `G` key (layer 0, row 1, col 5) is now tap dance `TD(9)`: tap for `g`, hold 150 ms for `Control`, the same as `Command` on `F`. `V` went back to plain `v` (it had `TD(3)`, Control on a 300 ms hold).
- **Why:** `Control` is easier to reach from the home row than from the thumbs.
- **Kept:** the two thumb `LCTL_T(KC_LNG2)` keys are unchanged, so `Control` is on the `G` and on both thumbs.
- **Hold time:** 150 ms, set in tap dance 9 (Vial → Tap Dance tab).
- **Status:** done and saved in `layouts/arman.vil` (made with `tools/dump_vil.py`, so flashes keep it). That file stays on your computer (gitignored).
- **Undo:** in Vial put plain `G` back on that key and `TD(3)` on `V`, then save the layout.

## 2026-11-10: herdr split keys (not part of the keyboard firmware)

- **What:** in `~/.config/herdr/config.toml`, `Ctrl+H` splits to the side (`split_vertical`) and `Ctrl+N` splits down (`split_horizontal`). The old `prefix+v` and `prefix+minus` still work.
- **Side effect:** `Ctrl+H` (backspace) and `Ctrl+N` (next history line) no longer reach the program inside a pane. If that bothers you, use `ctrl+alt+h` and `ctrl+alt+n`.
- **Backup:** `~/.config/herdr/config.toml.bak2` holds the config from before this change.
