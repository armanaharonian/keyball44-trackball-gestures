# How it works

What the firmware does, explained from zero. No C knowledge needed. The code is in [`keymap/keymap.c`](../keymap/keymap.c).

## The big picture

Your keyboard isn't just switches and wires. Each half has a small computer chip (an RP2040) running a program called **firmware**. This one is **QMK**, the most popular open-source keyboard firmware, in its **Vial** flavor (which lets you change keys live).

About a thousand times a second, QMK:

1. **Scans the keys.** It checks which keys are pressed.
2. **Looks up what they mean** on the active layer: `A`, `Enter`, "turn on layer 2"…
3. **Reads the trackball:** how far it rolled since last time, as an `x` and a `y`.
4. **Runs this project's code**, which decides what that motion becomes: pointer, scroll, Cmd+Tab, volume…
5. **Tells the computer** over USB: these keys are down, the mouse moved this much.

Step 4 is what this project adds. Everything else comes from QMK and holykeebs.

### Three pieces of code

| Code | Folder | From |
|---|---|---|
| QMK + Vial | `vial-qmk/` (downloaded by `setup.sh`) | QMK and Vial, holykeebs' fork |
| holykeebs userspace: trackball sensor, OLED, sniping, drag scroll | `qmk-userspace/` (downloaded by `setup.sh`) | holykeebs |
| **This keymap**: what the ball does on each layer | `keymap/` | this project |

`build.sh` copies `keymap/` into `vial-qmk` and compiles the three together.

### Vial owns keys, the firmware owns the ball

- **Keys, layers, tap dances** live in the keyboard's memory. You change them in Vial, live, and save them as `.vil` files.
- **What the ball does** can't be expressed in Vial, so it's C code in `keymap.c`. Changing it means building and installing new firmware.

## Layers

A **layer** is a whole alternate keyboard. Layer 0 is what you type on. Holding a layer key turns another layer on while you hold it. Several can be on at once; the **highest** wins.

This firmware asks only one question: *which is the highest layer that's on right now?* The answer picks the ball's job:

| Layer | Ball |
|---|---|
| 0 | App switcher (Cmd+Tab), sideways only |
| 1 | Vertical scroll |
| 3 | Drag scroll (scroll in any direction, a holykeebs feature) |
| 4 | Volume up/down; sideways = next/previous song |
| 5 | Brightness up/down |
| anything else (2, 6, 7) | Normal pointer |

The job is tied to the layer **number**, not to a key. Move your layer keys around in Vial freely; the ball follows.

## Words you'll see in the code

| Word | Meaning |
|---|---|
| `KC_A`, `KC_ENTER` | A plain key ("keycode") |
| `KC_LGUI` | Left Cmd (QMK calls it GUI) |
| `MO(2)` | Layer 2 while held |
| `LT(1, KC_SPC)` | Tap for Space, hold for layer 1 |
| `TD(2)` | Tap dance number 2, defined in Vial |
| `register_code(k)` / `unregister_code(k)` | Press and hold / release a key |
| `tap_code(k)` | Press and release a key |
| `timer_read()` / `timer_elapsed(t)` | The time now / milliseconds since `t` |
| count | The sensor's unit of distance. 800 counts = one inch by default |
| mouse report | What goes to the computer: `x`/`y` move the pointer, `v` scrolls. Setting a field to 0 means "nothing" |
| sniping | holykeebs' precise mode: lowers the sensor speed while you hold `HK_S_MODE` |

## Reading C in five minutes

Every example is real code from `keymap.c`.

**Comments.** Anything after `//` is a note for humans.

```c
// Vertical ball travel, in sensor counts, per volume/brightness key tap.
```

**Settings.** `#define NAME value` means "wherever `NAME` appears, use `value`". The settings use a three-line pattern:

```c
#ifndef BALL_SCROLL_DIVISOR
#    define BALL_SCROLL_DIVISOR 2000
#endif
```

Read it as "if not already defined, define `BALL_SCROLL_DIVISOR` as 2000". To change a setting, change only the number on the middle line.

**Variables** are named boxes holding a value. `bool` holds true/false, `int32_t` a whole number. `static` means the value is kept between one ball report and the next, which is how the code remembers things.

```c
static bool    app_switch_active = false;   // is the switcher open?
static int32_t app_switch_acc_x  = 0;       // sideways distance rolled so far
```

**Functions** are named recipes. This one is one step of the app switcher:

```c
static void app_switch_step(bool right) {
    app_switch_last_step = timer_read();
    if (!app_switch_active) {
        app_switch_active = true;
        register_code(KC_LGUI);
        tap_code16(right ? KC_TAB : S(KC_TAB));
    } else {
        tap_code(right ? KC_RGHT : KC_LEFT);
    }
}
```

In plain words: *remember the time. If the switcher isn't open, hold Cmd and tap Tab (or Shift+Tab when going left). If it's already open, tap the right or left arrow.* `right ? A : B` means "if right, A; otherwise B".

**Loops.** `while (…) { … }` repeats as long as the condition holds:

```c
while (ball_key_acc <= -BALL_KEY_STEP) {
    ball_key_acc += BALL_KEY_STEP;
    tap_code(up);
}
```

*While the ball has rolled up at least one step's worth, take one step off the total and tap volume up.* Roll fast, get several taps.

## `keymap.c`, part by part

| Part | What it does |
|---|---|
| `keymaps[]` | Default keys. Only used until Vial's keymap takes over |
| `layer_state_set_user` | Turns drag scroll on while layer 3 is held |
| Settings (`#define`s) | All the tuning numbers ([docs/settings.md](settings.md)) |
| `ball_scroll` | Turns vertical motion into scroll, divided by `BALL_SCROLL_DIVISOR` |
| `ball_pointer_scale` | Multiplies pointer motion by a fraction (the pointer speed) |
| `ball_key_steps` | Turns vertical motion into volume or brightness taps |
| `ball_media` | Layer 4: locks each gesture to one direction; up/down goes to `ball_key_steps` (volume), sideways taps next/previous song |
| `app_switch_step` | One switcher step: Cmd+Tab first, then arrows |
| `pointing_device_task_combined_keymap` | **The main function.** Runs on every ball report and picks the ball's job |
| `hk_pointing_devices_detected_keymap` | Tells VIA/Vial which half has the ball |

### The main function

`pointing_device_task_combined_keymap` receives the ball's motion and returns what actually goes to the computer.

1. It asks which layer is highest.
2. **Layer 1:** vertical motion becomes scroll; the pointer stays still.
3. **Layer 4:** like the switcher, each gesture first picks a direction from its first `APP_SWITCH_LOCK_TRAVEL` counts, so a wobbly volume roll never skips a song. Up/down becomes volume taps; sideways taps next song (right) or previous song (left) every `BALL_TRACK_STEP` counts. The direction is re-checked every `APP_SWITCH_LOCK_TRAVEL` counts and flips only when the other direction moved more than 2× as far.
4. **Layer 5:** vertical motion becomes brightness taps.
5. **Other layers (except 0):** the motion is scaled by the pointer speed fraction (or the sniping one) and moves the pointer.
6. **Layer 0, the app switcher:** the pointer never moves here. Instead:
   - **Close on a timer.** If Cmd is held and `APP_SWITCH_TIMEOUT_MS` passed since the last step, Cmd is released and macOS switches.
   - **End a gesture on stillness.** No motion for `APP_SWITCH_GESTURE_GAP_MS` ends the gesture.
   - **Lock a direction.** A gesture adds up travel until one direction reaches `APP_SWITCH_LOCK_TRAVEL`. Vertical gestures do nothing, so moving your hand up and down never switches apps.
   - **Re-check vertical.** If sideways travel later gets over 2× the vertical, the lock turns sideways, so a gesture that started a bit vertical still works.
   - **Step.** Every `APP_SWITCH_STEP` counts sideways calls `app_switch_step`.

Turning on any other layer releases Cmd right away.

### Why the "remainder" variables

Chips divide in whole numbers and throw fractions away. Roll the ball 1 count with a speed of 39/40: 1 × 39 / 40 = 0.975, which becomes 0, so slow careful moves would never reach the screen. The code keeps the leftover (the remainder) and adds it to the next report, so slow motion still adds up.

## Design decisions (and why)

These were tried the other way first and didn't work:

- **Cmd is released on a timer, not "when the ball stops".** A hand resting on the ball jitters forever, so "stops" never came and Cmd stayed stuck. Scrolling with Cmd stuck zooms the page.
- **Scroll and the switcher are on separate layers.** Mixing them on layer 0 caused accidental zooms.
- **No direction lock lasts "until the ball stops".** A permanent vertical lock left the switcher dead on a second quick use.
- **Auto-mouse is off.** QMK's auto-mouse turns a layer on whenever the ball moves, which fights "hold a key to choose the job".

## Ideas to build next

- A browser layer: roll left/right for back/forward or previous/next tab.
- Mission Control or desktop switching on the ball.

They need new code in the main function, following the same pattern as the app switcher.
