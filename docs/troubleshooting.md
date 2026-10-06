# Troubleshooting

Almost every problem comes from one of three things: **Docker is closed**, **Vial is open**, or **the Terminal is in the wrong folder**.

## Setup and build

**`no such file or directory` when running a script**
The Terminal is in another folder. Go back to the project:
```sh
cd ~/keyball44-trackball-gestures
```

**`Missing: docker` (or git, python3)**
Install what it names. Docker Desktop: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/). git and python3: `xcode-select --install`.

**`Docker isn't running` or `Cannot connect to the Docker daemon`**
Open Docker Desktop and wait for the whale icon in the menu bar:
```sh
open -a Docker
docker info --format '{{.ServerVersion}} running'
```
When the second command prints a version followed by `running`, build again. To avoid this: Docker → Settings → General → **Start Docker Desktop when you sign in**.

**`error:` lines during the build**
Usually a typo in `keymap/keymap.c`. The line names the file and line number, like `keymap.c:124:`. Fix that line and build again. If you used the tuner, it already put the file back.

**The build downloads a lot the first time**
Normal. The QMK Docker image is about 2.85 GB and is downloaded once. Don't delete it in Docker's Images tab, or the next build downloads it again.

## Installing (flash)

**`keyboard is locked`**
Vial (the app or a vial.rocks tab) is connected to the keyboard, and the scripts read Vial's replies by mistake. Close Vial completely and run the command again.

**`The keyboard differs from layouts/….vil`**
The keys on the keyboard don't match your newest saved layout, so installing now would lose them. In Vial: **File → Save current layout** into `layouts/`, close Vial, and run `./flash.sh` again.

**`uses combos, macros, …`**
The layout tool can't restore combos, macros, key overrides or alt-repeat keys yet, so it refuses rather than losing them. Either remove them in Vial and save the layout again, or install by hand: copy `firmware.uf2` to the `RPI-RP2` drive (see below) and re-create them in Vial afterwards.

**Stuck on `Press the boot key now` after pressing it**
The key press didn't reach boot mode. Double-tap the small **reset button** on the half with the USB cable. The `RPI-RP2` drive appears and the script continues by itself.

**Keys are wrong after an interrupted install**
The firmware went in but your layout wasn't put back. Send it again:
```sh
./load-layout.sh layouts/<your file>.vil
```

**Installing by hand**
Double-tap the reset button on the USB half. A drive called `RPI-RP2` appears. Drag `firmware.uf2` onto it; the keyboard restarts by itself. Then restore your keys with `./load-layout.sh`.

## Using it

**The ball switches apps when I wanted the pointer**
A tap-dance key only becomes a layer after its tapping term. Lower the term of your pointer key in Vial (Tap Dance tab), or wait a moment before moving the ball.

**My layer key types its letter while I'm typing fast**
The opposite problem: raise that key's tapping term a little.

**Cmd+Tab stays open, or switches too soon**
Adjust `APP_SWITCH_TIMEOUT_MS` (see [settings.md](settings.md)).

**Scrolling zooms instead of scrolling**
Cmd is being held. Wait one second for the switcher to close, or press and release Cmd.

**Brightness doesn't change**
See the brightness note in [settings.md](settings.md#ball_key_step-default-100).

## Safety

- Unplug USB before connecting or disconnecting the cable between the halves.
- Only the half with the USB cable needs new firmware.
