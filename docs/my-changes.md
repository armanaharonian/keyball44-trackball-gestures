# My changes

Every change made to this setup, newest first. Add a line here each time something changes.

## 2026-11-10: Control moves to hold-G

- **What:** the `G` key (base layer, `keymap/keymap.c`) is now `LCTL_T(KC_G)`. Tap it for `g`. Hold it for `Control`.
- **Why:** `Control` is easier to reach from the home row than from the thumbs.
- **Kept:** the two thumb `LCTL_T(KC_LNG2)` keys are unchanged, so `Control` is on the `G` and on both thumbs.
- **Hold time:** the firmware sets no `TAPPING_TERM`, so `G` uses the same global tapping term as the other hold keys. Change it in Vial (QMK Settings → Tapping Term), not here.
- **Status:** applied live to the keyboard over USB (layer 0, row 1, col 5 set to `0x210A`), no firmware flash. Built `firmware.uf2` contains the same change. Until a layout is saved in `layouts/`, a later `./flash.sh` stops, and a flash resets keys to the saved layout, so save the layout in Vial first.
- **Undo:** put `KC_G` back in place of `LCTL_T(KC_G)` in `keymap/keymap.c`, then `./build.sh` and `./flash.sh`.

## 2026-11-10: herdr split keys (not part of the keyboard firmware)

- **What:** in `~/.config/herdr/config.toml`, `Ctrl+H` splits to the side (`split_vertical`) and `Ctrl+N` splits down (`split_horizontal`). The old `prefix+v` and `prefix+minus` still work.
- **Side effect:** `Ctrl+H` (backspace) and `Ctrl+N` (next history line) no longer reach the program inside a pane. If that bothers you, use `ctrl+alt+h` and `ctrl+alt+n`.
- **Backup:** `~/.config/herdr/config.toml.bak2` holds the config from before this change.
