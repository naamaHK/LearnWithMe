"""
main.py – LearnWithMe 🎓
Top-level launcher: Writing Game OR Number Game
"""

import tkinter as tk
from shared import BG, DARK, FONT_TITLE, FONT_HEB, FONT_SMALL, BTN_GREEN, BTN_BLUE

from writing_game import WritingMenu
from math_game import MathMenu
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ColoringGame'))
from coloring_game import ColoringMenu


class HomeScreen:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("לומדים ביחד! 🎓")
        self.root.geometry("860x680")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self._build()

    def _build(self):
        self.frame = tk.Frame(self.root, bg=BG)
        self.frame.pack(expand=True, fill="both")

        # ── Header ────────────────────────────────────────────────────────────
        tk.Label(self.frame, text="🎓  לוֹמְדִים בְּיַחַד!  🎓",
                 font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=(60, 8))
        tk.Label(self.frame, text="בְּחַר בְּאֵיזֶה מִשְׂחָק תִּרְצֶה לִשְׂחָק:",
                 font=FONT_HEB, bg=BG, fg="#7F8C8D").pack(pady=(0, 45))

        btn_cfg = dict(
            font=(FONT_HEB[0], 22, "bold"),
            fg=DARK, padx=40, pady=26,
            relief="raised", bd=5, cursor="hand2", width=24,
        )

        # Writing Game button
        tk.Button(
            self.frame,
            text="✏️   מִשְׂחַק כְּתִיבָה",
            bg="#AED6F1",
            command=self._go_writing,
            **btn_cfg,
        ).pack(pady=12)

        # Math Game button
        tk.Button(
            self.frame,
            text="🔢   מִשְׂחַק חֶשְׁבּוֹן",
            bg="#A9DFBF",
            command=self._go_math,
            **btn_cfg,
        ).pack(pady=12)

        # Coloring Game button
        tk.Button(
            self.frame,
            text="🎨   סֵפֶר הַצְּבִיעָה",
            bg="#F9E4F5",
            command=self._go_coloring,
            **btn_cfg,
        ).pack(pady=12)

    def _clear(self):
        self.frame.destroy()

    def _rebuild(self):
        self._build()

    def _go_writing(self):
        self._clear()
        WritingMenu(self.root, back_cb=self._rebuild)

    def _go_math(self):
        self._clear()
        MathMenu(self.root, back_cb=self._rebuild)

    def _go_coloring(self):
        self._clear()
        self.root.resizable(True, True)
        ColoringMenu(self.root, back_cb=self._rebuild)


def main():
    root = tk.Tk()
    HomeScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
