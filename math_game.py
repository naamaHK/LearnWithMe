"""
math_game.py – Hebrew maths exercises for kids
  Mode A: Addition & subtraction up to 10
  Mode B: Addition & subtraction up to 20
  Mode C: Addition & subtraction up to 100
"""

import tkinter as tk
import random
from shared import (
    BG, DARK, BTN_GREEN, BTN_RED, BTN_BLUE, BTN_YELLOW,
    BTN_PURPLE, BTN_ORANGE,
    FONT_TITLE, FONT_HEB, FONT_SMALL,
    PRAISES, TRY_AGAIN,
    play_sound, make_scrollable, shake, hearts_str,
)

THEMES = [
    ("🍎", "#FDEDEC"),
    ("🦋", "#F5EEF8"),
    ("⭐", "#FEFCBF"),
    ("🍌", "#FFFDE7"),
    ("🐟", "#EAF4FB"),
    ("🌸", "#FCE4EC"),
    ("🍊", "#FFF3E0"),
    ("🐝", "#FFFDE7"),
    ("🍇", "#F3E5F5"),
    ("🚀", "#E8EAF6"),
]

# ── Drawing helpers ────────────────────────────────────────────────────────────

def _draw_icon_box(canvas, count, emoji, bg_col, x, y,
                   box_fill, box_outline,
                   icon_size=28, max_cols=5, crossed=False):
    """
    Draw `count` icons inside a coloured box at top-left (x, y).
    Returns (box_w, box_h).
    """
    cell = icon_size + 4

    if count == 0:
        bw, bh = 52, 52
        canvas.create_rectangle(x, y, x + bw, y + bh,
                                 fill=box_fill, outline=box_outline, width=2)
        canvas.create_text(x + bw // 2, y + bh // 2, text="0",
                           font=("Arial", 18, "bold"), fill="#7F8C8D")
        return bw, bh

    cols = min(count, max_cols)
    rows = (count + max_cols - 1) // max_cols
    box_w = cols * cell + 10
    box_h = rows * cell + 10

    canvas.create_rectangle(x, y, x + box_w, y + box_h,
                             fill=box_fill, outline=box_outline, width=2)

    for i in range(count):
        col = i % max_cols
        row = i // max_cols
        cx = x + 5 + col * cell + icon_size // 2
        cy = y + 5 + row * cell + icon_size // 2

        icon_bg  = "#FFCDD2" if crossed else bg_col
        icon_ol  = "#EF9A9A" if crossed else "#D5D8DC"
        canvas.create_oval(cx - icon_size // 2, cy - icon_size // 2,
                           cx + icon_size // 2, cy + icon_size // 2,
                           fill=icon_bg, outline=icon_ol, width=1)
        canvas.create_text(cx, cy, text=emoji,
                           font=("Arial", max(8, icon_size - 8)))
        if crossed:
            r = icon_size // 2 - 3
            canvas.create_line(cx - r, cy - r, cx + r, cy + r,
                               fill="#C62828", width=2)
            canvas.create_line(cx + r, cy - r, cx - r, cy + r,
                               fill="#C62828", width=2)

    return box_w, box_h


def _draw_subtraction_box(canvas, total, cross_count, emoji, bg_col,
                          x, y, icon_size=28, max_cols=10):
    """
    Draw `total` icons in ONE grid.
    The last `cross_count` icons have a red × through them.
    The first (total - cross_count) icons are normal (child counts these).
    Returns (box_w, box_h).
    """
    cell = icon_size + 4
    normal_count = total - cross_count

    if total == 0:
        bw, bh = 52, 52
        canvas.create_rectangle(x, y, x + bw, y + bh,
                                 fill="#F8F9FA", outline="#AEB6BF", width=2)
        canvas.create_text(x + bw // 2, y + bh // 2, text="0",
                           font=("Arial", 18, "bold"), fill="#7F8C8D")
        return bw, bh

    cols = min(total, max_cols)
    rows = (total + max_cols - 1) // max_cols
    box_w = cols * cell + 10
    box_h = rows * cell + 10

    canvas.create_rectangle(x, y, x + box_w, y + box_h,
                             fill="#F8F9FA", outline="#AEB6BF", width=2)

    for i in range(total):
        col = i % max_cols
        row = i // max_cols
        cx = x + 5 + col * cell + icon_size // 2
        cy = y + 5 + row * cell + icon_size // 2

        is_crossed = (i >= normal_count)
        icon_bg = "#FFCDD2" if is_crossed else "#D5F5E3"
        icon_ol = "#EF9A9A" if is_crossed else "#A9E4C3"

        canvas.create_oval(cx - icon_size // 2, cy - icon_size // 2,
                           cx + icon_size // 2, cy + icon_size // 2,
                           fill=icon_bg, outline=icon_ol, width=1)
        canvas.create_text(cx, cy, text=emoji,
                           font=("Arial", max(8, icon_size - 8)))
        if is_crossed:
            r = icon_size // 2 - 3
            canvas.create_line(cx - r, cy - r, cx + r, cy + r,
                               fill="#C62828", width=2)
            canvas.create_line(cx + r, cy - r, cx - r, cy + r,
                               fill="#C62828", width=2)

    return box_w, box_h


def draw_math_visual(canvas, a, b, op, theme, max_val=10):
    """
    Addition:    [a icons green box] + [b icons blue box]  (side by side)
    Subtraction: [a icons total, last b crossed with red ×]  (single grid)
    """
    canvas.delete("all")
    emoji, bg_col = theme

    PAD = 10
    OP_W = 44
    OP_FONT = ("Arial Rounded MT Bold", 30, "bold")

    if op == "+":
        # ── Addition: two separate boxes ────────────────────────────────────
        if max_val <= 10:
            icon_size, max_cols = 34, 5
        elif max_val <= 20:
            icon_size, max_cols = 28, 5
        else:
            icon_size, max_cols = 22, 10

        y_top = 14
        bw_a, bh_a = _draw_icon_box(canvas, a, emoji, bg_col,
                                     PAD, y_top,
                                     "#D5F5E3", "#1E8449",
                                     icon_size, max_cols)
        op_x = PAD + bw_a + 6
        bw_b, bh_b = _draw_icon_box(canvas, b, emoji, bg_col,
                                     op_x + OP_W, y_top,
                                     "#D6EAF8", "#1A5276",
                                     icon_size, max_cols)
        mid_y = y_top + max(bh_a, bh_b, 50) // 2
        canvas.create_text(op_x + OP_W // 2, mid_y,
                           text="+", font=OP_FONT, fill="#E67E22")
        new_h = max(bh_a, bh_b) + y_top + 20
        canvas.config(height=max(new_h, 80))

    else:
        # ── Subtraction: single grid, last b icons crossed out ───────────────
        # Use more columns for larger numbers so grid stays compact
        if max_val <= 10:
            icon_size, max_cols = 36, 5
        elif max_val <= 20:
            icon_size, max_cols = 30, 10
        else:
            icon_size, max_cols = 22, 10

        bw, bh = _draw_subtraction_box(canvas, a, b, emoji, bg_col,
                                        PAD, 14, icon_size, max_cols)
        canvas.config(height=max(bh + 34, 80))


# ───────────────────────────────────────────────────────────────────────────────
# Math sub-menu
# ───────────────────────────────────────────────────────────────────────────────

class MathMenu:
    def __init__(self, root, back_cb):
        self.root = root
        self.back_cb = back_cb
        self.root.geometry("860x620")
        self._build()

    def _build(self):
        self.frame = tk.Frame(self.root, bg=BG)
        self.frame.pack(expand=True, fill="both")

        tk.Label(self.frame, text="🔢  מִשְׂחַק חֶשְׁבּוֹן 🔢",
                 font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=(50, 10))
        tk.Label(self.frame, text="בְּחַר בְּאֵיזֶה תַּרְגִּיל תִּרְצֶה לְתַרְגֵּל:",
                 font=FONT_HEB, bg=BG, fg="#7F8C8D").pack(pady=(0, 30))

        btn_cfg = dict(font=(FONT_HEB[0], 20, "bold"), fg=DARK,
                       padx=30, pady=22, relief="raised", bd=4,
                       cursor="hand2", width=26)

        tk.Button(self.frame, text="🌱  חִבּוּר וְחִסּוּר עַד 10",
                  bg="#A9DFBF", command=lambda: self._start(10), **btn_cfg).pack(pady=8)
        tk.Button(self.frame, text="🌿  חִבּוּר וְחִסּוּר עַד 20",
                  bg="#AED6F1", command=lambda: self._start(20), **btn_cfg).pack(pady=8)
        tk.Button(self.frame, text="🌳  חִבּוּר וְחִסּוּר עַד 100",
                  bg="#D7BDE2", command=lambda: self._start(100), **btn_cfg).pack(pady=8)

        tk.Button(self.frame, text="← חֲזֹר לַתַּפְרִיט הָרָאשִׁי",
                  font=FONT_SMALL, bg="#ECF0F1", fg=DARK,
                  relief="flat", cursor="hand2",
                  command=self._back).pack(pady=(28, 0))

    def _clear(self):  self.frame.destroy()
    def _back(self):   self._clear(); self.back_cb()
    def _rebuild(self): self._build()

    def _start(self, max_val):
        self._clear()
        MathGame(self.root, max_val=max_val, back_cb=self._rebuild)


# ───────────────────────────────────────────────────────────────────────────────
# Generic Math Game
# ───────────────────────────────────────────────────────────────────────────────

class MathGame:
    MAX_GUESSES = 3

    def __init__(self, root, max_val: int, back_cb):
        self.root     = root
        self.back_cb  = back_cb
        self.max_val  = max_val
        self.answer   = 0
        self.theme    = random.choice(THEMES)
        self.a = self.b = 0
        self.op = "+"

        # Initial canvas height (will be updated dynamically)
        self.canvas_w = 560
        self.canvas_h = 120

        self.root.geometry("900x840")
        self._build()
        self._new_question()

    def _build(self):
        self._outer, self.frame = make_scrollable(self.root)

        top = tk.Frame(self.frame, bg=BG)
        top.pack(fill="x", padx=15, pady=(12, 0))
        tk.Button(top, text="← חֲזֹר", font=FONT_SMALL, bg="#ECF0F1",
                  fg=DARK, relief="flat", cursor="hand2",
                  command=self._back).pack(side="left")

        if self.max_val <= 10:
            title_text, title_color = "🌱 חִבּוּר וְחִסּוּר עַד 10", BTN_GREEN
        elif self.max_val <= 20:
            title_text, title_color = "🌿 חִבּוּר וְחִסּוּר עַד 20", BTN_BLUE
        else:
            title_text, title_color = "🌳 חִבּוּר וְחִסּוּר עַד 100", BTN_PURPLE

        tk.Label(self.frame, text=title_text,
                 font=FONT_TITLE, bg=BG, fg=title_color).pack(pady=(8, 4))

        self.hearts_lbl = tk.Label(self.frame, text="", font=FONT_SMALL, bg=BG, fg=DARK)
        self.hearts_lbl.pack()

        self.q_lbl = tk.Label(self.frame, text="",
                               font=("Arial Rounded MT Bold", 44, "bold"),
                               bg=BG, fg=DARK)
        self.q_lbl.pack(pady=(12, 6))

        canvas_frame = tk.Frame(self.frame, bg="#F0F3F4", bd=2, relief="groove")
        canvas_frame.pack(pady=8, padx=20)
        self.count_canvas = tk.Canvas(canvas_frame,
                                       width=self.canvas_w,
                                       height=self.canvas_h,
                                       bg="#FAFAFA", highlightthickness=0)
        self.count_canvas.pack(padx=6, pady=6)

        # Non-revealing instruction
        self.inst_lbl = tk.Label(self.frame, text="", font=FONT_SMALL,
                                  bg=BG, fg="#5D6D7E")
        self.inst_lbl.pack(pady=(2, 0))

        ans_frame = tk.Frame(self.frame, bg=BG)
        ans_frame.pack(pady=14)
        tk.Label(ans_frame, text="הַתְּשׁוּבָה:", font=FONT_HEB,
                 bg=BG, fg=DARK).pack(side="right", padx=10)
        self.entry = tk.Entry(ans_frame, font=("Arial", 36, "bold"),
                              width=5, justify="center", bd=3, relief="groove",
                              bg="white", fg=DARK, insertbackground=DARK)
        self.entry.pack(side="right", padx=8)
        self.entry.bind("<Return>", lambda e: self._check())

        bf = tk.Frame(self.frame, bg=BG)
        bf.pack(pady=8)
        self.check_btn = tk.Button(bf, text="✅ בדוק!", font=FONT_HEB, bg="#A9DFBF", fg=DARK,
                   padx=20, pady=10, relief="raised", bd=3, cursor="hand2",
                   command=self._check)
        self.check_btn.pack(side="left", padx=8)

        self.feedback = tk.Label(self.frame, text="",
                                  font=(FONT_HEB[0], 20, "bold"),
                                  bg=BG, fg=BTN_GREEN, wraplength=720)
        self.feedback.pack(pady=14)

    def _new_question(self):
        self.theme = random.choice(THEMES)
        self.guesses_left = self.MAX_GUESSES
        self._update_hearts()
        self.entry.config(state="normal")
        self.check_btn.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.feedback.config(text="")

        self.op = random.choice(["+", "-"])
        if self.op == "+":
            self.a = random.randint(0, self.max_val)
            self.b = random.randint(0, self.max_val - self.a)
            self.answer = self.a + self.b
            q = f"{self.a}  +  {self.b}  =  ?"
            inst = "סִפְרוּ אֶת כָּל הַסִּמְלִים יַחַד! 🔢"
        else:
            self.a = random.randint(0, self.max_val)
            self.b = random.randint(0, self.a)
            self.answer = self.a - self.b
            q = f"{self.a}  −  {self.b}  =  ?"
            inst = "סִפְרוּ כַּמָּה נִשְׁאַר! 🔢"

        self.q_lbl.config(text=q)
        self.inst_lbl.config(text=inst)

        draw_math_visual(self.count_canvas, self.a, self.b, self.op,
                         self.theme, max_val=self.max_val)

    def _check(self):
        if self.guesses_left <= 0:
            return
        raw = self.entry.get().strip()
        if not raw:
            return
        try:
            user_ans = int(raw)
        except ValueError:
            self.feedback.config(text="❓ כתבו מספר בבקשה!", fg=BTN_ORANGE)
            return

        if user_ans == self.answer:
            play_sound("success")
            self.feedback.config(text=random.choice(PRAISES), fg=BTN_GREEN)
            self.guesses_left = 0
            self.entry.config(state="disabled")
            self.check_btn.config(state="disabled")
            self.root.after(1500, self._new_question)
        else:
            self.guesses_left -= 1
            play_sound("fail")
            shake(self.root)
            self._update_hearts()
            if self.guesses_left == 0:
                self.feedback.config(
                    text=f"😔 התשובה הנכונה היא: {self.answer}",
                    fg=BTN_ORANGE)
                self.entry.config(state="disabled")
                self.check_btn.config(state="disabled")
                self.root.after(2000, self._new_question)
            else:
                self.feedback.config(text=random.choice(TRY_AGAIN), fg=BTN_RED)

    def _update_hearts(self):
        self.hearts_lbl.config(
            text=f"נִסְיוֹנוֹת: {hearts_str(self.guesses_left, self.MAX_GUESSES)}")

    def _back(self):
        self._outer.destroy()
        self.root.geometry("860x620")
        self.back_cb()
