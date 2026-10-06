"""Vial .vil keycode names -> 16-bit QMK keycodes (vial-qmk/quantum/keycodes.h).

.vil files use Vial's legacy spellings (KC_BSPACE, LT1(KC_SPACE)), so several
names below are older QMK aliases. Shared by restore_vil.py and the key editor.
"""
import re

BASIC = {
    "KC_NO": 0x00, "KC_TRNS": 0x01, "KC_ENTER": 0x28, "KC_ESCAPE": 0x29, "KC_BSPACE": 0x2A,
    "KC_TAB": 0x2B, "KC_SPACE": 0x2C, "KC_MINUS": 0x2D, "KC_EQUAL": 0x2E, "KC_LBRACKET": 0x2F,
    "KC_RBRACKET": 0x30, "KC_BSLASH": 0x31, "KC_NONUS_HASH": 0x32, "KC_SCOLON": 0x33,
    "KC_QUOTE": 0x34, "KC_GRAVE": 0x35, "KC_COMMA": 0x36, "KC_DOT": 0x37, "KC_SLASH": 0x38,
    "KC_CAPSLOCK": 0x39,
    "KC_PSCREEN": 0x46, "KC_SCROLLLOCK": 0x47, "KC_PAUSE": 0x48, "KC_INSERT": 0x49, "KC_HOME": 0x4A,
    "KC_PGUP": 0x4B, "KC_DELETE": 0x4C, "KC_END": 0x4D, "KC_PGDOWN": 0x4E,
    "KC_RIGHT": 0x4F, "KC_LEFT": 0x50, "KC_DOWN": 0x51, "KC_UP": 0x52, "KC_KP_MINUS": 0x56,
    "KC_NONUS_BSLASH": 0x64,
    "KC_RO": 0x87, "KC_JYEN": 0x89, "KC_LANG1": 0x90, "KC_LANG2": 0x91,
    "KC_AUDIO_MUTE": 0xA8, "KC_AUDIO_VOL_UP": 0xA9, "KC_AUDIO_VOL_DOWN": 0xAA,
    "KC_MEDIA_NEXT_TRACK": 0xAB, "KC_MEDIA_PREV_TRACK": 0xAC, "KC_MEDIA_STOP": 0xAD,
    "KC_MEDIA_PLAY_PAUSE": 0xAE, "KC_BRIGHTNESS_UP": 0xBD, "KC_BRIGHTNESS_DOWN": 0xBE,
    "KC_MS_U": 0xCD, "KC_MS_D": 0xCE, "KC_MS_L": 0xCF, "KC_MS_R": 0xD0,
    "KC_BTN1": 0xD1, "KC_BTN2": 0xD2, "KC_BTN3": 0xD3, "KC_BTN4": 0xD4, "KC_BTN5": 0xD5,
    "KC_WH_U": 0xD9, "KC_WH_D": 0xDA, "KC_WH_L": 0xDB, "KC_WH_R": 0xDC,
    "KC_LCTRL": 0xE0, "KC_LSHIFT": 0xE1, "KC_LALT": 0xE2, "KC_LGUI": 0xE3,
    "KC_RCTRL": 0xE4, "KC_RSHIFT": 0xE5, "KC_RALT": 0xE6, "KC_RGUI": 0xE7,
    "QK_BOOT": 0x7C00,
    "RM_TOGG": 0x7842, "RM_NEXT": 0x7843, "RM_PREV": 0x7844, "RM_HUEU": 0x7845, "RM_HUED": 0x7846,
    "RM_SATU": 0x7847, "RM_SATD": 0x7848, "RM_VALU": 0x7849, "RM_VALD": 0x784A,
    "RM_SPDU": 0x784B, "RM_SPDD": 0x784C,
}
for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    BASIC["KC_" + c] = 0x04 + i
for i, c in enumerate("1234567890"):
    BASIC["KC_" + c] = 0x1E + i
for i in range(1, 13):
    BASIC["KC_F%d" % i] = 0x3A + i - 1
for i in range(13, 25):
    BASIC["KC_F%d" % i] = 0x68 + i - 13
for i in range(16):
    BASIC["USER%02d" % i] = 0x7E00 + i

# Modifier bits: left Ctrl/Shift/Alt/GUI = 1/2/4/8, the right-hand ones add 0x10.
MODS = {"LCTL": 0x01, "LSFT": 0x02, "LALT": 0x04, "LGUI": 0x08,
        "RCTL": 0x11, "RSFT": 0x12, "RALT": 0x14, "RGUI": 0x18}
MOD_TAP = {m + "_T": bits for m, bits in MODS.items()}
LAYER_FN = {"TO": 0x5200, "MO": 0x5220, "DF": 0x5240, "TG": 0x5260, "OSL": 0x5280, "TT": 0x52C0}


def kc(name):
    if name == -1:
        return None
    if name in BASIC:
        return BASIC[name]
    m = re.fullmatch(r"(\w+)\((\w+)\)", name)
    if m and m[1] in MODS:
        return (MODS[m[1]] << 8) | kc(m[2])
    m = re.fullmatch(r"LT(\d+)\((\w+)\)", name)
    if m:
        return 0x4000 | (int(m[1]) << 8) | kc(m[2])
    m = re.fullmatch(r"(\w+)\((\d+)\)", name)
    if m and m[1] in LAYER_FN:
        return LAYER_FN[m[1]] | int(m[2])
    m = re.fullmatch(r"TD\((\d+)\)", name)
    if m:
        return 0x5700 | int(m[1])
    m = re.fullmatch(r"(\w+_T)\((\w+)\)", name)
    if m and m[1] in MOD_TAP:
        return 0x2000 | (MOD_TAP[m[1]] << 8) | kc(m[2])
    raise KeyError(name)
