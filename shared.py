"""
shared.py – Common helpers for LearnWithMe
"""

import tkinter as tk
import subprocess
import random

# ── Colours ───────────────────────────────────────────────────────────────────
BG          = "#FFF8F0"
DARK        = "#2C3E50"
BTN_GREEN   = "#27AE60"
BTN_RED     = "#E74C3C"
BTN_BLUE    = "#2980B9"
BTN_YELLOW  = "#F1C40F"
BTN_PURPLE  = "#8E44AD"
BTN_ORANGE  = "#E67E22"

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_TITLE  = ("Arial Rounded MT Bold", 30, "bold")
FONT_HEB    = ("Arial", 18, "bold")
FONT_SMALL  = ("Arial", 13)
FONT_HUGE   = ("Arial Rounded MT Bold", 42, "bold")

# ── Praise phrases (with niqqud) ──────────────────────────────────────────────
PRAISES = [
    "🎉 כֹּל הַכָּבוֹד! עָנִיתָ נָכוֹן! אַתָּה מַדְהִים! 🌟",
    "⭐ יָפֶה מְאֹד! תְּשׁוּבָה נְכוֹנָה! 🎊",
    "🏆 וָואוּ! נָכוֹן לְגַמְרֵי! אַתָּה גָּאוֹן! 🎉",
    "🌈 מְצֻיָּן! כֹּל הַכָּבוֹד! ⭐",
    "🎯 נָכוֹן! אַתָּה מַמָּשׁ טוֹב בָּזֶה! 🥳",
    "🦄 פַּנְטַסְטִי! תְּשׁוּבָה מֻשְׁלֶמֶת! 💫",
    "🌟 עָשִׂיתָ אֶת זֶה! כֹּל הַכָּבוֹד! 🎊",
]

TRY_AGAIN = [
    "💪 נַסֵּה שׁוּב! אַתָּה יָכוֹל! 😊",
    "🙌 כִּמְעַט! נַסֵּה עוֹד פַּעַם! 💪",
    "😊 לֹא מְוַתְּרִים! נַסֵּה שׁוּב!",
]


# ── Sound ─────────────────────────────────────────────────────────────────────
def play_sound(sound_type: str):
    sounds = {
        "success": "/System/Library/Sounds/Funk.aiff",
        "fail":    "/System/Library/Sounds/Basso.aiff",
    }
    path = sounds.get(sound_type)
    if path:
        try:
            subprocess.Popen(["afplay", path])
        except Exception:
            pass


# ── Say (Hebrew TTS) ──────────────────────────────────────────────────────────
def say_hebrew(text: str):
    try:
        subprocess.Popen(["say", "-v", "Carmit", text])
    except Exception:
        pass


# ── Scrollable frame ──────────────────────────────────────────────────────────
def make_scrollable(root, bg=BG):
    outer = tk.Frame(root, bg=bg)
    outer.pack(expand=True, fill="both")

    canvas = tk.Canvas(outer, bg=bg, highlightthickness=0)
    scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", expand=True, fill="both")

    inner = tk.Frame(canvas, bg=bg)
    win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    def _on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())

    inner.bind("<Configure>", _on_configure)
    canvas.bind("<Configure>", _on_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    return outer, inner


# ── Shake animation ───────────────────────────────────────────────────────────
def shake(root):
    x = root.winfo_x()
    y = root.winfo_y()
    for dx in [10, -10, 7, -7, 4, -4, 0]:
        root.after(30 * abs(dx), lambda d=dx: root.geometry(f"+{x+d}+{y}"))


# ── Hearts display ────────────────────────────────────────────────────────────
def hearts_str(remaining, total=3):
    return "❤️" * remaining + "🖤" * (total - remaining)
