// Copyright 2022 MURAOKA Taro (aka KoRoN, @kaoriya)
// Copyright 2026 Idan Kamara (@idank)
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H
#include "users/holykeebs/holykeebs.h"
#include "users/holykeebs/pointing.h"

#ifdef VIA_ENABLE
#    include "via.h"
#endif

// The stock Keyball keymap carried over to the holykeebs userspace. Layers 0-2
// are unchanged. Layer 3 (hold the left inner thumb) keeps its role as the
// settings layer with the Keyball keycodes replaced by their HK_* equivalents:
// the CPI and scroll-divider key pairs become one hold-and-tap key each
// (hold HK_P_SET_D / HK_P_SET_S / HK_P_SET_THR, tap up/down), the scroll-snap
// keys become HK_C_SCROLL (cycles the axis lock), and RGBLIGHT keys become their
// RGB Matrix counterparts. Holding layer 3 also puts the ball into scroll mode,
// as the stock firmware did.

// clang-format off
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
  // keymap for default (VIA)
  [0] = LAYOUT_universal(
    KC_ESC   , KC_Q     , KC_W     , KC_E     , KC_R     , KC_T     ,                                        KC_Y     , KC_U     , KC_I     , KC_O     , KC_P     , KC_DEL   ,
    KC_TAB   , KC_A     , KC_S     , KC_D     , KC_F     , KC_G     ,                                        KC_H     , KC_J     , KC_K     , KC_L     , KC_SCLN  , S(KC_7)  ,
    KC_LSFT  , KC_Z     , KC_X     , KC_C     , KC_V     , KC_B     ,                                        KC_N     , KC_M     , KC_COMM  , KC_DOT   , KC_SLSH  , KC_INT1  ,
              KC_LALT,KC_LGUI,LCTL_T(KC_LNG2)     ,LT(1,KC_SPC),LT(3,KC_LNG1),                  KC_BSPC,LT(2,KC_ENT), RCTL_T(KC_LNG2),     KC_RALT  , KC_PSCR
  ),

  [1] = LAYOUT_universal(
    HK_C_SCROLL ,  KC_F1   , KC_F2    , KC_F3   , KC_F4    , KC_F5    ,                                         KC_F6    , KC_F7    , KC_F8    , KC_F9    , KC_F10   , KC_F11   ,
    HK_I_SCROLL ,  _______ , _______  , KC_UP   , KC_ENT   , KC_DEL   ,                                         KC_PGUP  , MS_BTN1  , KC_UP    , MS_BTN2  , MS_BTN3  , KC_F12   ,
    _______   ,  _______ , KC_LEFT  , KC_DOWN , KC_RGHT  , KC_BSPC  ,                                         KC_PGDN  , KC_LEFT  , KC_DOWN  , KC_RGHT  , _______  , _______  ,
                  _______  , _______ , _______  ,         _______  , _______  ,                   _______  , _______  , _______       , _______  , _______
  ),

  [2] = LAYOUT_universal(
    _______  ,S(KC_QUOT), KC_7     , KC_8    , KC_9     , S(KC_8)  ,                                         S(KC_9)  , S(KC_1)  , S(KC_6)  , KC_LBRC  , S(KC_4)  , _______  ,
    _______  ,S(KC_SCLN), KC_4     , KC_5    , KC_6     , KC_RBRC  ,                                         KC_NUHS  , KC_MINS  , S(KC_EQL), S(KC_3)  , KC_QUOT  , S(KC_2)  ,
    _______  ,S(KC_MINS), KC_1     , KC_2    , KC_3     ,S(KC_RBRC),                                        S(KC_NUHS),S(KC_INT1), KC_EQL   ,S(KC_LBRC),S(KC_SLSH),S(KC_INT3),
                  KC_0     , KC_DOT  , _______  ,         _______  , _______  ,                   KC_DEL   , _______  , _______       , _______  , _______
  ),

  [3] = LAYOUT_universal(
    RM_TOGG  , HK_AML_T , HK_AML_UP, HK_AML_DN, _______  , HK_BONGO_T,                                       HK_DUMP  , RM_SPDU  , RM_SPDD  , _______  , _______  , _______  ,
    RM_NEXT  , RM_HUEU  , RM_SATU  , RM_VALU  , KC_UP    , HK_S_MODE ,                                       HK_P_SET_D, HK_P_SET_S, HK_P_SET_THR, _______, _______  , _______  ,
    RM_PREV  , RM_HUED  , RM_SATD  , RM_VALD  , KC_DOWN  , HK_S_MODE_T,                                      HK_D_MODE, HK_D_MODE_T, _______ , _______  , _______  , HK_SAVE  ,
                  QK_BOOT  , HK_RESET , _______  ,        _______  , _______  ,                   _______  , _______  , _______       , HK_RESET , QK_BOOT
  ),

  [4] = LAYOUT_universal(
    _______  , _______   , _______  , _______  , _______  , _______  ,                                        _______  , _______  , _______  , _______ , _______ , _______  ,
    _______  , _______  , _______  , _______  , _______  , _______ ,                                        _______  , _______  , _______  , _______ , _______  , _______  ,
    _______ , _______  , _______  , _______  , _______  , _______ ,                                        _______  , _______ , _______ , _______  , _______  , _______ ,
                  _______  , _______  , _______  ,        _______  , _______  ,                   _______  , _______  , _______       , _______  , _______
  ),

  [5] = LAYOUT_universal(
    _______  , _______   , _______  , _______  , _______  , _______  ,                                        _______  , _______  , _______  , _______ , _______ , _______  ,
    _______  , _______  , _______  , _______  , _______  , _______ ,                                        _______  , _______  , _______  , _______ , _______  , _______  ,
    _______ , _______  , _______  , _______  , _______  , _______ ,                                        _______  , _______ , _______ , _______  , _______  , _______ ,
                  _______  , _______  , _______  ,        _______  , _______  ,                   _______  , _______  , _______       , _______  , _______
  ),

  [6] = LAYOUT_universal(
    _______  , _______   , _______  , _______  , _______  , _______  ,                                        _______  , _______  , _______  , _______ , _______ , _______  ,
    _______  , _______  , _______  , _______  , _______  , _______ ,                                        _______  , _______  , _______  , _______ , _______  , _______  ,
    _______ , _______  , _______  , _______  , _______  , _______ ,                                        _______  , _______ , _______ , _______  , _______  , _______ ,
                  _______  , _______  , _______  ,        _______  , _______  ,                   _______  , _______  , _______       , _______  , _______
  ),

  [7] = LAYOUT_universal(
    _______  , _______   , _______  , _______  , _______  , _______  ,                                        _______  , _______  , _______  , _______ , _______ , _______  ,
    _______  , _______  , _______  , _______  , _______  , _______ ,                                        _______  , _______  , _______  , _______ , _______  , _______  ,
    _______ , _______  , _______  , _______  , _______  , _______ ,                                        _______  , _______ , _______ , _______  , _______  , _______ ,
                  _______  , _______  , _______  ,        _______  , _______  ,                   _______  , _______  , _______       , _______  , _______
  ),
};
// clang-format on

layer_state_t layer_state_set_user(layer_state_t state) {
    // Keyball convention: the ball scrolls while the settings layer is held.
    hk_set_dragscroll_both(get_highest_layer(state) == 3);
    return state;
}

// What the ball does depends on the highest active layer:
//   0: app switcher (sideways only; vertical motion is ignored)
//   1: vertical scroll
//   3: drag scroll (userspace, see layer_state_set_user)
//   4: volume (ball up/down taps volume up/down)
//   5: screen brightness (ball up/down taps brightness up/down)
//   any other: normal pointer
//
// App switcher: the first sideways step holds Cmd and opens the macOS switcher
// (Cmd+Tab to the right, Cmd+Shift+Tab to the left); further steps move the
// selection with the arrow keys. Cmd is released, switching to the selected
// app, APP_SWITCH_TIMEOUT_MS after the last step. Each gesture (motion between
// pauses of APP_SWITCH_GESTURE_GAP_MS) is locked to one axis by its first
// APP_SWITCH_LOCK_TRAVEL counts, so a mostly vertical gesture never switches.
// A vertical lock is re-checked every APP_SWITCH_LOCK_TRAVEL counts and turns
// horizontal once sideways motion clearly dominates, so a gesture that starts
// vertical (repositioning the finger) still switches without a full stop.

#define BALL_SCROLL_LAYER 1
#define BALL_VOLUME_LAYER 4
#define BALL_BRIGHTNESS_LAYER 5

// Vertical ball travel, in sensor counts, per volume/brightness key tap.
#ifndef BALL_KEY_STEP
#    define BALL_KEY_STEP 100
#endif

// Ball travel, in sensor counts (800 CPI by default), per switcher step.
#ifndef APP_SWITCH_STEP
#    define APP_SWITCH_STEP 200
#endif

// Layer 1 scroll runs this many times slower than the drag scroll on layer 3
// (which follows the scroll throttle setting alone).
#ifndef BALL_SCROLL_DIVISOR
#    define BALL_SCROLL_DIVISOR 2000
#endif

// Pointer speed on the pointer layers, as a fraction of the sensor's CPI.
// Scaled here rather than via the CPI so the switcher and scroll keep theirs.
#ifndef BALL_POINTER_NUM
#    define BALL_POINTER_NUM 39
#endif
#ifndef BALL_POINTER_DEN
#    define BALL_POINTER_DEN 40
#endif

// Same, while sniping (HK_S_MODE), which already lowers the sensor's CPI.
#ifndef BALL_SNIPE_NUM
#    define BALL_SNIPE_NUM 1
#endif
#ifndef BALL_SNIPE_DEN
#    define BALL_SNIPE_DEN 2
#endif

#ifndef APP_SWITCH_TIMEOUT_MS
#    define APP_SWITCH_TIMEOUT_MS 1000
#endif

#ifndef APP_SWITCH_GESTURE_GAP_MS
#    define APP_SWITCH_GESTURE_GAP_MS 150
#endif

#ifndef APP_SWITCH_LOCK_TRAVEL
#    define APP_SWITCH_LOCK_TRAVEL 20
#endif

typedef enum { AXIS_NONE, AXIS_HORIZONTAL, AXIS_VERTICAL } app_switch_axis_t;

static bool              app_switch_active = false;
static app_switch_axis_t app_switch_axis   = AXIS_NONE;
static int32_t           app_switch_acc_x  = 0;
static int32_t           app_switch_acc_y  = 0;
static uint16_t          app_switch_last_motion;
static uint16_t          app_switch_last_step;

static void app_switch_end(void) {
    if (app_switch_active) {
        unregister_code(KC_LGUI);
        app_switch_active = false;
    }
}

static void app_switch_reset_gesture(void) {
    app_switch_axis  = AXIS_NONE;
    app_switch_acc_x = 0;
    app_switch_acc_y = 0;
}

// Turns vertical ball motion into scroll the same way the userspace's drag
// scroll does, so the scroll throttle and inversion settings apply here too,
// slowed down by BALL_SCROLL_DIVISOR. The division remainder carries over
// between reports so slow motion still adds up to scroll.
static mouse_hv_report_t ball_scroll(int16_t y) {
    const hk_pointer_state_t* state = hk_active_pointer_state();
    static int32_t            remainder = 0;

    int32_t num = state->scroll_direction_inverted ? -y : y;
    int32_t den = BALL_SCROLL_DIVISOR;
#ifdef POINTING_DEVICE_HIRES_SCROLL_ENABLE
    num *= pointing_device_get_hires_scroll_resolution();
#endif
    if (state->pointer_scroll_throttle > 0) {
        den *= state->pointer_scroll_throttle;
    }

    remainder += num;
    int32_t v = remainder / den;
    remainder -= v * den;

    if (v > MOUSE_REPORT_HV_MAX) v = MOUSE_REPORT_HV_MAX;
    if (v < MOUSE_REPORT_HV_MIN) v = MOUSE_REPORT_HV_MIN;
    return v;
}

// Scales one pointer axis by num/den, carrying the remainder over between
// reports so slow motion isn't rounded away.
static mouse_xy_report_t ball_pointer_scale(mouse_xy_report_t delta, int32_t* remainder, int32_t num, int32_t den) {
    *remainder += (int32_t)delta * num;
    const int32_t scaled = *remainder / den;
    *remainder -= scaled * den;
    return scaled;
}

// Turns vertical ball travel into taps of `up` (ball rolled up) or `down`, one
// per BALL_KEY_STEP counts. The accumulator is reset on leaving the layer.
static int32_t ball_key_acc = 0;

static void ball_key_steps(int16_t y, uint16_t up, uint16_t down) {
    ball_key_acc += y;
    while (ball_key_acc <= -BALL_KEY_STEP) {
        ball_key_acc += BALL_KEY_STEP;
        tap_code(up);
    }
    while (ball_key_acc >= BALL_KEY_STEP) {
        ball_key_acc -= BALL_KEY_STEP;
        tap_code(down);
    }
}

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

report_mouse_t pointing_device_task_combined_keymap(report_mouse_t mouse_report) {
    const uint8_t layer = get_highest_layer(layer_state);
    if (layer != BALL_VOLUME_LAYER && layer != BALL_BRIGHTNESS_LAYER) {
        ball_key_acc = 0;
    }

    if (layer != 0) {
        app_switch_end();
        app_switch_reset_gesture();
        if (layer == BALL_SCROLL_LAYER) {
            mouse_report.v = ball_scroll(mouse_report.y);
            mouse_report.x = 0;
            mouse_report.y = 0;
        } else if (layer == BALL_VOLUME_LAYER || layer == BALL_BRIGHTNESS_LAYER) {
            if (layer == BALL_VOLUME_LAYER) {
                ball_key_steps(mouse_report.y, KC_VOLU, KC_VOLD);
            } else {
                ball_key_steps(mouse_report.y, KC_BRIU, KC_BRID);
            }
            mouse_report.x = 0;
            mouse_report.y = 0;
        } else {
            static int32_t rem_x = 0, rem_y = 0;
            const bool     sniping = hk_active_pointer_state()->cursor_mode == CURSOR_MODE_SNIPING;
            const int32_t  num     = sniping ? BALL_SNIPE_NUM : BALL_POINTER_NUM;
            const int32_t  den     = sniping ? BALL_SNIPE_DEN : BALL_POINTER_DEN;
            mouse_report.x = ball_pointer_scale(mouse_report.x, &rem_x, num, den);
            mouse_report.y = ball_pointer_scale(mouse_report.y, &rem_y, num, den);
        }
        return mouse_report;
    }

    // Released on a timer from the last step rather than from the last motion:
    // a hand resting on the ball keeps reporting tiny movements, which would
    // otherwise hold Cmd down indefinitely.
    if (app_switch_active && timer_elapsed(app_switch_last_step) > APP_SWITCH_TIMEOUT_MS) {
        app_switch_end();
    }

    const int16_t x = mouse_report.x;
    const int16_t y = mouse_report.y;
    mouse_report.x  = 0;
    mouse_report.y  = 0;

    if (x == 0 && y == 0) {
        if (timer_elapsed(app_switch_last_motion) > APP_SWITCH_GESTURE_GAP_MS) {
            app_switch_reset_gesture();
        }
        return mouse_report;
    }
    app_switch_last_motion = timer_read();

    if (app_switch_axis == AXIS_NONE) {
        app_switch_acc_x += x;
        app_switch_acc_y += y;
        if (abs(app_switch_acc_x) < APP_SWITCH_LOCK_TRAVEL && abs(app_switch_acc_y) < APP_SWITCH_LOCK_TRAVEL) {
            return mouse_report;
        }
        if (abs(app_switch_acc_x) > abs(app_switch_acc_y)) {
            app_switch_axis = AXIS_HORIZONTAL;
            app_switch_acc_y = 0;
        } else {
            app_switch_axis = AXIS_VERTICAL;
            app_switch_acc_x = 0;
            app_switch_acc_y = 0;
            return mouse_report;
        }
    } else if (app_switch_axis == AXIS_HORIZONTAL) {
        app_switch_acc_x += x;
    } else {
        // A resting hand jitters, so the gap that ends a gesture may never come;
        // re-checking here keeps a vertical lock from deadening the switcher.
        app_switch_acc_x += x;
        app_switch_acc_y += y;
        if (abs(app_switch_acc_x) < APP_SWITCH_LOCK_TRAVEL && abs(app_switch_acc_y) < APP_SWITCH_LOCK_TRAVEL) {
            return mouse_report;
        }
        if (abs(app_switch_acc_x) <= 2 * abs(app_switch_acc_y)) {
            app_switch_acc_x = 0;
            app_switch_acc_y = 0;
            return mouse_report;
        }
        app_switch_axis  = AXIS_HORIZONTAL;
        app_switch_acc_y = 0;
    }

    while (app_switch_acc_x >= APP_SWITCH_STEP) {
        app_switch_acc_x -= APP_SWITCH_STEP;
        app_switch_step(true);
    }
    while (app_switch_acc_x <= -APP_SWITCH_STEP) {
        app_switch_acc_x += APP_SWITCH_STEP;
        app_switch_step(false);
    }
    return mouse_report;
}

#ifdef VIA_ENABLE
// Reflect the runtime-detected ball combination into the VIA "Ball availability"
// layout option (None=0, Right=1, Left=2, Dual=3 -> bits 0-1), so VIA/Remap shows
// the thumb keys for the installed configuration. Called by the userspace once
// detection completes (see hk_pointing_devices_detected_keymap).
void hk_pointing_devices_detected_keymap(bool left_has_pointing, bool right_has_pointing) {
    uint8_t  layouts = (right_has_pointing ? 0x01 : 0x00) | (left_has_pointing ? 0x02 : 0x00);
    uint32_t curr    = via_get_layout_options();
    uint32_t next    = (curr & ~0x3) | layouts;
    if (next != curr) {
        via_set_layout_options(next);
    }
}
#endif
