# Every setting

All of these are numbers near the top of [`keymap/keymap.c`](../keymap/keymap.c). The easiest way to change them is the Trackball Tuner (`./tuner.sh`). By hand: change the number, then `./build.sh` and `./flash.sh`.

Each one looks like this; change only the number on the middle line:

```c
#ifndef BALL_SCROLL_DIVISOR
#    define BALL_SCROLL_DIVISOR 2000
#endif
```

To see the current value of any setting:

```sh
grep -n 'define BALL_' keymap/keymap.c
grep -n 'define APP_SWITCH' keymap/keymap.c
```

> **Change by a factor.** macOS accelerates pointer and scroll motion, so speeds feel non-linear. Multiply or divide (×0.8, ×1.25) instead of adding a fixed amount, and change one setting at a time so you know what made the difference.

## Pointer (layer 2 and any layer without its own job)

### `BALL_POINTER_NUM` / `BALL_POINTER_DEN` (default 39 / 40)

Pointer speed, as a fraction of the sensor's own speed. 39/40 = 0.975, a little under the sensor's speed. 1/1 is the sensor's speed; 5/4 is 25% faster.

- Faster: raise the fraction (raise NUM or lower DEN).
- Slower: lower it (e.g. 3/4, 1/2).

### `BALL_SNIPE_NUM` / `BALL_SNIPE_DEN` (default 1 / 2)

Pointer speed while sniping (holding the `HK_S_MODE` key), for precise work. Sniping already lowers the sensor's speed; this fraction slows it further.

## Scroll (layer 1)

### `BALL_SCROLL_DIVISOR` (default 2000)

The ball's vertical motion is divided by this number to make scroll. **A smaller number scrolls faster.** For reference, while this was tuned: 18000 barely moved, 900 was too fast, 2500 was slow-ish.

Scroll direction follows holykeebs' "invert scroll" setting (`HK_I_SCROLL` key in Vial).

## App switcher (layer 0, nothing held)

### `APP_SWITCH_STEP` (default 200)

How far you roll sideways to move one app in the Cmd+Tab switcher, in sensor counts (800 = one inch at the default sensor speed). Lower = more sensitive.

### `APP_SWITCH_TIMEOUT_MS` (default 1000)

How long after your last step the switcher waits before letting go of Cmd, which switches to the selected app. Lower = switches sooner. Too low and it switches before you finish choosing (500 felt too short).

### `APP_SWITCH_LOCK_TRAVEL` (default 20)

How far a gesture travels (in counts) before the code decides whether it's sideways (switch apps) or vertical (ignored). Higher = fewer accidental switches; lower = reacts quicker. Layer 4 uses it too, to tell songs (sideways) from volume (up/down).

### `APP_SWITCH_GESTURE_GAP_MS` (default 150)

How long the ball must be completely still for a gesture to end and its direction decision to reset. Also used on layer 4. Rarely needs changing.

## Volume, songs and brightness (layers 4 and 5)

### `BALL_KEY_STEP` (default 100)

How far you roll up or down (in counts) for one volume or brightness step. Higher = finer control; lower = faster changes.

Brightness sends the `KC_BRIU` / `KC_BRID` keys. If macOS ignores them on your Mac, change them in the main function to `KC_BRMU` / `KC_BRMD` (the brightness keys of Apple's external keyboards).

### `BALL_TRACK_STEP` (default 300)

Layer 4 only: how far you roll sideways (in counts) to skip to the next song (right) or previous song (left). Higher = fewer accidental skips; lower = a shorter roll. 400 felt like too much rolling. Each pause of `APP_SWITCH_GESTURE_GAP_MS` starts the count over, so one longer roll works better than several short flicks.

Songs use the `KC_MNXT` / `KC_MPRV` media keys; macOS sends them to whatever is playing. In most players the first "previous" restarts the current song and a second one goes back.

## Layer numbers

These say which layer gives which job. They're plain `#define`s (no `#ifndef` around them):

```c
#define BALL_SCROLL_LAYER 1
#define BALL_VOLUME_LAYER 4
#define BALL_BRIGHTNESS_LAYER 5
```

Layer 0 is always the app switcher and layer 3 drag scroll. Every other layer is the pointer.

## Other files

| File | Setting | Default | What it does |
|---|---|---|---|
| `keymap/config.h` | `TAP_CODE_DELAY` | 5 | Milliseconds each tapped key is held (switcher arrows, volume taps) |
| `keymap/config.h` | `DYNAMIC_KEYMAP_LAYER_COUNT` | 8 | How many layers Vial shows |
| `keymap/config.h` | `VIAL_KEYBOARD_UID` | holykeebs' | Vial's ID for the Keyball44. Don't change it |
| `keymap/rules.mk` | `RGB_MATRIX_ENABLE`, `VIA_ENABLE`, `VIAL_ENABLE` | yes | Turn those features on |
| `build.sh` | `OLED` | yes | `OLED=no ./build.sh` builds without the OLED screen |

## Hold times are in Vial, not here

How long you hold a key before it becomes a layer is a **tap dance** setting in Vial (**Tap Dance** tab, **Tapping term**). No firmware install needed. Until that time passes, the ball still does the app switcher, so for the pointer key a short term (around 170 ms) feels best.
