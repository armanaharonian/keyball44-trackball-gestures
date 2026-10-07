# Keyball44 Trackball Gestures

One trackball, many jobs. This is a Vial firmware for the **holykeebs Keyball44** where the trackball does something different depending on which key you hold:

| You hold | The ball does |
|---|---|
| nothing | **Switches apps** (Cmd+Tab): roll sideways to pick an app, let go to switch |
| a layer 1 key | **Scrolls** up and down |
| a layer 2 key | **Moves the mouse pointer** (and a precise "sniping" mode) |
| a layer 4 key | **Changes the volume**: roll up/down. Roll sideways for the next/previous song |
| a layer 5 key | **Changes the screen brightness**: roll up/down |

You choose which keys reach each layer in Vial, like any other key. Nothing switches by itself: the ball only does what the key you're holding says.

It also comes with scripts that build and install the firmware for you, and a **Trackball Tuner**: a page in your browser where you change the pointer speed, scroll speed and the rest with buttons, then install it with one click.

> **Made for:** a holykeebs Keyball44 running Vial, used on **macOS**. Building works on any computer with Docker, but the install script and the tuner are macOS-only. Tested on one Keyball44 with the trackball on the right half and the USB cable on the left.

---

## Contents

1. [What you need](#1-what-you-need)
2. [Download this project](#2-download-this-project)
3. [Run the setup](#3-run-the-setup)
4. [Save your current layout](#4-save-your-current-layout)
5. [Build the firmware](#5-build-the-firmware)
6. [Install it on the keyboard](#6-install-it-on-the-keyboard)
7. [Give yourself keys to reach the layers](#7-give-yourself-keys-to-reach-the-layers)
8. [Try it](#8-try-it)
9. [Tune it to your taste](#9-tune-it-to-your-taste)
10. [Changing keys later](#10-changing-keys-later)
11. [Going back to the original firmware](#11-going-back-to-the-original-firmware)
12. [When something goes wrong](#12-when-something-goes-wrong)

---

## 1. What you need

| Thing | Why | How to get it |
|---|---|---|
| A holykeebs **Keyball44** with Vial | This firmware is made for it | — |
| **Docker Desktop** | Builds the firmware without installing compilers on your Mac | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/), then open it once |
| **Vial** | To change keys and save your layout | [get.vial.today](https://get.vial.today/) (or use [vial.rocks](https://vial.rocks) in Chrome) |
| **git** and **python3** | Used by the scripts | Open the Terminal and run `xcode-select --install` (skip if already installed) |
| About **3 GB** of free disk space | The firmware source is about 2 GB | — |

### Using the Terminal

Every step below happens in the **Terminal** app. If you've never used it:

- Open it with <kbd>⌘ Cmd</kbd> + <kbd>Space</kbd>, type `Terminal`, press <kbd>Enter</kbd>.
- Copy a command from this page, paste it with <kbd>⌘ Cmd</kbd> + <kbd>V</kbd>, press <kbd>Enter</kbd>.
- Wait until the prompt (the line ending in `%`) comes back before running the next one.
- Lines starting with `#` are notes; the Terminal ignores them.
- To stop something that's running, press <kbd>Ctrl</kbd> + <kbd>C</kbd>.

---

## 2. Download this project

```sh
cd ~
git clone https://github.com/armanaharonian/keyball44-trackball-gestures.git
cd keyball44-trackball-gestures
```

From now on, every command runs inside this folder. If you open a new Terminal window, go back with `cd ~/keyball44-trackball-gestures`.

---

## 3. Run the setup

This downloads the holykeebs firmware source (the exact versions this was tested with) and a small Python library for talking to the keyboard. **It takes a few minutes and downloads about 2 GB.** You only do this once.

```sh
./setup.sh
```

It ends with:

```
==> Setup finished
```

---

## 4. Save your current layout

Installing new firmware makes Vial reset all your keys to defaults. The install script puts them back from a saved file, so save your layout first:

1. Open Vial. It finds the keyboard on its own.
2. Click **File → Save current layout**.
3. Save it in this project's **`layouts`** folder, with any name ending in `.vil` (for example `my-layout.vil`).
4. **Close Vial** (<kbd>⌘ Cmd</kbd> + <kbd>Q</kbd>, or close the vial.rocks tab). The scripts can't talk to the keyboard while Vial is connected.

> The install script always uses the **most recently saved** file in `layouts/`.

---

## 5. Build the firmware

Make sure **Docker Desktop is open** (a whale icon in the menu bar). Then:

```sh
./build.sh
```

It prints a lot for about a minute. Success is the last line:

```
Firmware ready: /Users/you/keyball44-trackball-gestures/firmware.uf2
```

> If your Keyball44 has no OLED screen, build with `OLED=no ./build.sh` instead.

---

## 6. Install it on the keyboard

```sh
./flash.sh
```

1. It checks that the keyboard matches your saved layout, then prints:
   ```
   Press the boot key now: right half, bottom row, the outermost key (under P).
   ```
2. **Press that key once.** It's on the right half, bottom row, the key right under <kbd>P</kbd>. For a moment the script turns it into a "boot" key.
3. The keyboard goes quiet for a few seconds while the firmware installs. A drive called `RPI-RP2` may flash by; that's normal.
4. **Don't type** until the last line appears:
   ```
   Flashed. Waiting for the keyboard...
   changed 46 entries
   would change 0 entries
   ```
   The first number varies. `would change 0 entries` means your keys are back exactly as you saved them. Done.

> Only the half with the **USB cable** needs this. The other half keeps working as before.

---

## 7. Give yourself keys to reach the layers

The ball's job depends on the **layer**, so you need keys that turn layers on while held. There are two ways.

### Option A: use the starter layout (easiest)

This project includes `layouts/starter.vil`, the layout it was designed with. It's a normal QWERTY layout plus:

| Hold | Layer | The ball | Also on that layer |
|---|---|---|---|
| <kbd>Space</kbd> (tap for space) | 1 | scrolls | numbers, arrows |
| <kbd>S</kbd> (tap for s) or the <kbd>Backspace</kbd> thumb | 2 | moves the pointer | <kbd>V</kbd> = left click, <kbd>B</kbd> = right click, hold the <kbd>Enter</kbd> thumb = precise pointer |
| <kbd>J</kbd> (tap for j) | 4 | volume, songs | — |
| <kbd>K</kbd> (tap for k) | 5 | brightness | — |
| <kbd>F</kbd> / <kbd>D</kbd> / <kbd>V</kbd> | — | — | hold for Cmd / Alt / Ctrl |

Load it (no firmware install needed):

```sh
./load-layout.sh layouts/starter.vil
```

It ends with `would change 0 entries`. **This replaces your keys**, so do it only if you want this layout. Then save it as your own: open Vial, **File → Save current layout** into `layouts/`, and close Vial.

### Option B: add the keys yourself in Vial

Keep your layout and just add keys for the layers you want:

1. Open Vial and click a key you rarely use.
2. In the bottom panel, open the **Layers** tab and pick **MO(2)** for the pointer (MO(1) scroll, MO(4) volume, MO(5) brightness). "MO" means "on while held".
3. Want the key to still type a letter when tapped? Use a **tap dance** (Vial's **Tap Dance** tab: tap = the letter, hold = `MO(2)`, tapping term about 170 ms) and put `TD(n)` on the key.
4. For clicks, put **Mouse 1** (left) and **Mouse 2** (right) somewhere on layer 2.
5. **File → Save current layout** into `layouts/`, then close Vial.

---

## 8. Try it

- **Switch apps:** don't hold anything. Roll the ball **sideways**: the macOS app switcher opens and moves one app per step. Stop rolling and it switches after one second. Rolling up/down does nothing on purpose, so resting your hand never switches apps.
- **Scroll:** hold your layer 1 key and roll up/down.
- **Pointer:** hold your layer 2 key and move the ball. Click with your Mouse 1 / Mouse 2 keys.
- **Volume / brightness:** hold your layer 4 or 5 key and roll up/down.
- **Songs:** hold your layer 4 key and roll sideways: right for the next song, left for the previous one.

> **Tip:** a tap-dance key only becomes a layer after its tapping term (the hold time). Until then, the ball still switches apps. If you start moving the ball too early when holding <kbd>S</kbd>, lower its tapping term a bit.

---

## 9. Tune it to your taste

### The easy way: the Trackball Tuner

```sh
./tuner.sh
```

A page opens in your browser with every setting, a plain explanation, and **Faster / Slower** buttons. Change what you like, then press **Build and flash**. It saves the change, starts Docker if needed, builds, installs, and shows a big banner when it's time to press the boot key. Close Vial before you press the button.

When you're done, go back to the Terminal and press <kbd>Ctrl</kbd> + <kbd>C</kbd> to stop the tuner.

### By hand

All settings are numbers near the top of [`keymap/keymap.c`](keymap/keymap.c). Change a number, then run `./build.sh` and `./flash.sh`.

| Setting | Default | What it does | Make it… |
|---|---|---|---|
| `BALL_POINTER_NUM` / `BALL_POINTER_DEN` | 39 / 40 | Pointer speed, as a fraction of the sensor's speed | faster: raise the fraction (e.g. 1/1, 5/4) |
| `BALL_SNIPE_NUM` / `BALL_SNIPE_DEN` | 1 / 2 | Pointer speed in precise (sniping) mode | slower: lower the fraction |
| `BALL_SCROLL_DIVISOR` | 2000 | Scroll speed: the motion is divided by this | faster: **lower** it |
| `APP_SWITCH_STEP` | 200 | How far you roll per app (800 = one inch) | more sensitive: lower it |
| `APP_SWITCH_TIMEOUT_MS` | 1000 | Wait after your last move before switching | switch sooner: lower it |
| `APP_SWITCH_LOCK_TRAVEL` | 20 | How far a move goes before it's judged sideways or vertical | fewer accidental switches: raise it |
| `APP_SWITCH_GESTURE_GAP_MS` | 150 | Stillness that ends a gesture | rarely needs changing |
| `BALL_KEY_STEP` | 100 | How far you roll per volume/brightness step | finer control: raise it |
| `BALL_TRACK_STEP` | 300 | How far you roll sideways per song on layer 4 | shorter roll: lower it |

macOS speeds up scrolling and pointer motion, so changes feel non-linear. Change by a factor (×0.8, ×1.25) rather than by a fixed amount, and change one thing at a time. [docs/settings.md](docs/settings.md) explains each one in detail.

---

## 10. Changing keys later

Change keys in Vial as usual; no firmware install needed. **Before the next `./flash.sh` or tuner build**, save the layout again (**File → Save current layout** into `layouts/`) and close Vial. If you forget, the install stops and tells you, so you never lose keys.

---

## 11. Going back to the original firmware

To return to holykeebs' original Vial keymap:

```sh
./build.sh --stock
./flash.sh
```

Your layout comes back the same way.

---

## 12. When something goes wrong

| You see | Why | Fix |
|---|---|---|
| `no such file or directory` | The Terminal is in another folder | `cd ~/keyball44-trackball-gestures` |
| `Docker isn't running` / `Cannot connect to the Docker daemon` | Docker Desktop is closed | `open -a Docker`, wait for the whale icon, try again |
| `keyboard is locked` | Vial is connected to the keyboard | Close Vial (and any vial.rocks tab), try again |
| `The keyboard differs from …` | Keys changed in Vial since your last save | Save the layout from Vial into `layouts/`, close Vial, try again |
| Stuck on `Press the boot key now` after pressing it | The key didn't reach boot mode | Double-tap the small **reset button** on the USB half; the script continues |
| Keys are wrong after an interrupted install | The layout wasn't put back | `./load-layout.sh layouts/<your file>.vil` |
| `uses combos, macros…` | The layout tool can't restore those yet | Remove them in Vial, or install the `.uf2` by hand and re-create them |

More detail in [docs/troubleshooting.md](docs/troubleshooting.md).

> **Safety:** unplug the USB cable before connecting or disconnecting the cable between the two halves. Plugging it in while powered can damage the controllers.

---

## What's in this project

```
keyball44-trackball-gestures/
├── README.md            this guide
├── setup.sh             one-time download of the firmware source
├── build.sh             builds firmware.uf2 with Docker
├── flash.sh             installs it and puts your layout back
├── load-layout.sh       sends a saved layout to the keyboard
├── tuner.sh             opens the Trackball Tuner in your browser
├── keymap/              the firmware: keymap.c (the trackball code), config.h, rules.mk, vial.json
├── layouts/             your saved layouts, plus starter.vil
├── tools/               restore_vil.py (layout restore over USB), the tuner's code
└── docs/                how it works, every setting, troubleshooting
```

Want to know how the code works? Read [docs/how-it-works.md](docs/how-it-works.md). It assumes no C knowledge.

---

## Credits and license

- The [Keyball](https://github.com/Yowkees/keyball) keyboard by Yowkees, and the Keyball44 build and firmware by [holykeebs](https://holykeebs.com).
- [QMK](https://qmk.fm) and [Vial](https://get.vial.today).
- The trackball gestures, tuner and scripts in this repo.

Licensed under the GNU GPL v2, like QMK. See [LICENSE](LICENSE).
