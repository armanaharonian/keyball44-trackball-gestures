// Copyright 2021 @Yowkees
// Copyright 2022 MURAOKA Taro (aka KoRoN, @kaoriya)
// Copyright 2026 Idan Kamara (@idank)
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

#define TAP_CODE_DELAY 5

// No auto mouse layer: the ball's role is picked per layer in keymap.c (app
// switcher on 0, scroll on 1, pointer on 2), and layers are held explicitly.

#define DYNAMIC_KEYMAP_LAYER_COUNT 8

// Vial identity and unlock combo. VIAL_INSECURE lives in the shared userspace
// config (users/holykeebs/config.h), so it is intentionally not repeated here.
// The unlock combo is unused while VIAL_INSECURE is set, but kept so re-securing
// later doesn't require re-picking keys: the two outermost top keys, matrix
// [0,0] (top-left of the left half) and [4,0] (top-right of the right half).
#define VIAL_KEYBOARD_UID {0x74, 0x4A, 0x13, 0xB3, 0x25, 0x0A, 0x24, 0x04}
#define VIAL_UNLOCK_COMBO_ROWS { 0, 4 }
#define VIAL_UNLOCK_COMBO_COLS { 0, 0 }
