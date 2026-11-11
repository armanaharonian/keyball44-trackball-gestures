# My changes

Every change made to this setup, newest first. Add a line here each time something changes.

## 2026-11-11: Layer button + ball drives herdr; Space still scrolls

- **What:** hold the layer button (`MO(1)`, left thumb) and roll the ball. If you start rolling within 150 ms of pressing it, the ball moves between herdr panes. If you start later, left/right changes tab and up/down changes workspace. The mode is picked on the first roll of each hold.
- **Why:** Space (`LT(1, KC_SPC)`) turns on the same layer 1, so Space + ball keeps scrolling and the layer button was free.
- **Kept:** the layer button still turns layer 1 on for its keys (numbers, arrows). Hold U / hold I + ball still work.
- **How:** `process_record_keymap` in `keymap/keymap.c` tracks the physical `MO(BALL_SCROLL_LAYER)` press (`herdr_layer_held`, `herdr_layer_pressed_at`). `pointing_device_task_combined_keymap` checks it before layer 1's scroll. The 150 ms is `HERDR_LAYER_PANES_MS`.
- **Undo:** reflash the keymap without the `herdr_layer_*` code.

## 2026-11-11: herdr holds move to U and I; hold T talks to Handy; hold R renames the pane

- **What:** hold `U` + ball moves between herdr panes (was `Y`). Hold `I` + ball: left/right changes tab, up/down changes workspace (was `U`). `Y` is a plain letter again.
- **Hold T:** talks to Handy while held. Tap dance 7 hold went from `Ctrl+Space` to `LCAG(KC_T)` (`Ctrl+Option+Command+T`, held until you let go). The keyboard can't send Apple's `fn`, so Handy's Transcribe shortcut must be `ctrl+option+command+t`, without `fn`.
- **Hold R:** renames the focused herdr pane. `R` is tap dance 11 (tap `r`, hold 200 ms for `QK_USER_0`). The firmware turns `QK_USER_0` into one `ctrl+alt+r` tap, which `~/.config/herdr/config.toml` maps to `rename_pane` (backup: `config.toml.bak18`).
- **How:** `process_record_keymap` in `keymap/keymap.c` checks `KC_U`/`KC_I` instead of `KC_Y`/`KC_U`, and handles `HERDR_RENAME`. T and R live in `layouts/arman.vil` (backup: `layouts/arman.vil.bak-before-t-handy`).
- **Typing:** `I` now types on release or when the next key is pressed, like `U`. `R` types on release, like the other tap-dance letters.
- **Undo:** reflash the `20d0b27` keymap; put `300` back as tap dance 7's hold, and plain `KC_R` (21) on the R key.

## 2026-11-10: Hold Y + ball moves herdr panes, hold U + ball changes tab and workspace

- **What:** hold `Y` and roll the ball to move between herdr panes. Hold `U` and roll: left/right changes tab, up/down changes workspace. Works in any app, with no detector. Without Y or U the ball is the app switcher. This replaces hold A + ball.
- **How:** `process_record_keymap` in `keymap/keymap.c` holds back plain `KC_Y`/`KC_U`. `herdr_ball` sends `ctrl+alt+h/j/k/l` or `ctrl+alt+shift+arrow`, one per `HERDR_STEP` (150) counts. Built on the `9bf802b` keymap (before the detector) plus the `KC_G` default from `85fd96c`.
- **Typing:** Y and U type on release if the ball never stepped, or right away when another key is pressed during the hold, so the typing order is kept. Holding them no longer auto-repeats.
- **Kept:** hold-A Cmd+Option and hold-G Control in the Vial layout, and the herdr keys in `~/.config/herdr/config.toml`.
- **Undo:** reflash the `9bf802b` keymap (with the `KC_G` line).

## 2026-11-10: Hold A + ball moves herdr panes; the watcher is gone

- **What:** hold `A` and roll the ball to move between herdr panes. Hold `A` + `Shift` and roll: left/right changes tab, up/down changes workspace. Works in any app, with no watcher. Without `A` the ball always does the app switcher.
- **Why:** the watcher (`tools/herdr-watch.py`) ran `osascript` several times a second and kept WindowServer busy. When it stopped while Ghostty was in front, herdr mode stayed on and the app switcher stopped working.
- **How:** `herdr_a_held` in `keymap/keymap.c` tracks the physical `A` (`TD(10)`), so the ball moves panes before the 150 ms hold turns it into Cmd+Option. `herdr_panes` drops that Cmd+Option while it sends `ctrl+alt+h/j/k/l` or `ctrl+alt+shift+arrow`.
- **Removed:** the raw-HID herdr mode message (`0x7E`), Cmd (hold-F) + ball for tabs, and the Cmd+Opt+arrows swap. All three depended on the watcher. The LaunchAgent is unloaded and its plist deleted from `~/Library/LaunchAgents`. `tools/herdr-watch.py` and its plist template are deleted from the repo.
- **Side effect:** rolling the ball during a hold shorter than 150 ms still types `a` when you let go.
- **Undo:** reflash the previous `keymap.c`.

## 2026-11-10: herdr Ctrl+T new tab, Ctrl+Shift+T new workspace

- **What:** `new_tab = ["prefix+c", "ctrl+t"]` and `new_workspace = ["prefix+shift+n", "ctrl+shift+t"]` in `~/.config/herdr/config.toml`. The old prefix keys still work. Backup: `config.toml.bak6`.
- **Also:** `close_workspace = ["prefix+shift+d", "ctrl+shift+w"]`, so `Ctrl+Shift+W` closes the whole workspace. Backup: `config.toml.bak7`.
- **Side effect:** `Ctrl+T` (transpose characters in the shell) no longer reaches the pane.
- **Undo:** remove the two lines.

## 2026-11-10: herdr Cmd + ball changes tab and workspace

- **What:** in herdr mode (Ghostty in front), hold `Command` (hold-F or any Cmd) and roll the ball: left/right changes tab, up/down changes workspace. Without Cmd the ball still moves between panes.
- **How:** `herdr_panes` in `keymap/keymap.c` sends `ctrl+alt+shift+arrow` (same chords as Cmd+Opt+arrows) and drops Cmd while sending. `herdr_f_held` tracks the physical `F`, so it works before the 150 ms hold ends.
- **Status:** flashed and working.
- **Undo:** reflash the previous `herdr_panes`.

## 2026-11-10: Hold A is Cmd+Option

- **What:** the `A` key (layer 0, row 1, col 1) is now tap dance `TD(10)`: tap for `a`, hold 150 ms for `Cmd+Option` together. Use it with the arrows in herdr for tabs and workspaces.
- **Status:** applied, saved in `layouts/arman.vil`, tested and working. Backup: `layouts/arman.vil.bak-before-a-hold`.
- **Hold time:** 150 ms, set in tap dance 10 (Vial → Tap Dance tab).
- **Undo:** in Vial put plain `A` back on that key, save the layout.

## 2026-11-10: herdr Cmd+Opt+arrows move tabs and workspaces

- **What:** in herdr mode (Ghostty in front), hold `Cmd+Opt` and press left/right to change herdr tab, up/down to change workspace.
- **How:** `process_record_keymap` in `keymap/keymap.c` swaps that chord for `ctrl+alt+shift+arrow`, because the Mac never sends Cmd to a terminal. `~/.config/herdr/config.toml` maps those to `previous_tab`, `next_tab`, `previous_workspace`, `next_workspace`. Backup: `config.toml.bak5`.
- **Needs:** firmware flashed (`./build.sh`, then `./flash.sh`).
- **Status:** flashed and working. The firmware tracks the physical `A` key (`herdr_a_held`), so an arrow pressed before the 150 ms hold still counts. It also reads weak mods, which the hold-A tap dance sets. `flash.sh` fails with `open failed` while the watcher runs: `launchctl unload` it first, then load it again.
- **Undo:** remove `process_record_keymap` and the four keys from `config.toml`, then reflash.

## 2026-11-10: Ball moves between herdr panes (automatic)

- **What:** while Ghostty (the terminal that runs herdr) is the front app, rolling the ball with no key held moves focus between herdr panes: right, left, down, up. In every other app the ball still does Cmd+Tab.
- **How:** `tools/herdr-watch.py` checks the front app and sends one raw-HID message (`0x7E`, on or off) to the keyboard. The firmware (`keymap/keymap.c`, `herdr_panes`) then taps `ctrl+alt+h/j/k/l` per `HERDR_PANE_STEP` (150) counts of travel. Herdr maps those chords to `focus_pane_*` in `~/.config/herdr/config.toml`.
- **Limit:** the watcher knows the app, not the pane. Any Ghostty window counts as herdr mode.
- **Needs:** firmware flashed (`./flash.sh`, after saving your layout in Vial), and the watcher running. Install it with `sed "s|__REPO__|$PWD|g" tools/com.armanaharonian.herdr-watch.plist > ~/Library/LaunchAgents/com.armanaharonian.herdr-watch.plist && launchctl load ~/Library/LaunchAgents/com.armanaharonian.herdr-watch.plist`. macOS asks once to let it control System Events.
- **Status:** firmware flashed and verified (`would change 0 entries`). Watcher installed as a LaunchAgent (`com.armanaharonian.herdr-watch`). Bug fixed: System Events reports the app as `ghostty` (lowercase), so the watcher now compares names case-insensitively. Before that it never turned herdr mode on.
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
