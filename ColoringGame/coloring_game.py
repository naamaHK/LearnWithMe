"""
coloring_game.py – ספר הצביעה הדיגיטלי 🎨
Digital coloring book – click a color, click the page to fill!
"""

import tkinter as tk
import os
import datetime
from PIL import Image, ImageDraw, ImageTk

# ── Paths ───────────────────────────────────────────────────────────────────────
GAME_DIR  = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(GAME_DIR, "pages")

# Canvas fills the available space dynamically – these are the minimum/default sizes
CANVAS_W = 900
CANVAS_H = 650

# ── Style ───────────────────────────────────────────────────────────────────────
BG         = "#FFF8F2"
DARK       = "#2C3E50"
PALETTE_BG = "#F0EDE8"
FONT_BIG   = ("Arial Rounded MT Bold", 24, "bold")
FONT_MED   = ("Arial", 17, "bold")
FONT_SM    = ("Arial", 13)
FONT_PAL   = ("Arial", 11, "bold")

# ── 9 Themes ────────────────────────────────────────────────────────────────────
THEMES = [
    ("🌊  עולם הים",                 "ocean",       "#C8F0FF"),
    ("🦕  דינוזאורים",               "dinos",       "#D5F5D5"),
    ("🚗  כלי רכב",                  "vehicles",    "#FFF9C4"),
    ("🦄  חדי קרן",                  "unicorn",     "#FFF0FA"),
    ("🌸  מנדלות",                   "mandalas",    "#F5E6FF"),
    ("👸  נסיכות",                   "princess",    "#F3D9F5"),
    ("🚒  פאו פטרול – יחידת החילוץ", "rescue",      "#FDEBD0"),
    ("🐶  בלואי ובינגו",             "bluey",        "#D6F0FF"),
    ("🐱  הלו קיטי",                 "hello_kitty", "#FADADD"),
    ("🚀  חלל",                      "space",       "#D6E4F7"),
    ("👽  סטיץ׳",                    "stitch",      "#C5CAE9"),
]

# ── 24-color palette ─────────────────────────────────────────────────────────────
PALETTE = [
    # column 1          column 2          column 3          column 4
    ("#FF0000","אדום"),  ("#FF6600","כתום"),("#FFEA00","צהוב"),("#C8FF00","ירוק-צהוב"),
    ("#00CC44","ירוק"),  ("#00AAFF","תכלת"),("#0000EE","כחול"),("#6600CC","סגול"),
    ("#FF00FF","ורוד-סגול"),("#FF0077","ורוד-עז"),("#FF99CC","ורוד בהיר"),("#FFCCAA","אפרסק"),
    ("#FF3333","אדום כהה"),("#FF9900","ענבר"),("#88FF00","ליים"),("#00FFCC","טורקיז"),
    ("#FF69B4","ורוד"),  ("#663300","חום"), ("#CC8800","חרדל"),("#FFD700","זהב"),
    ("#FFFFFF","לבן"),   ("#BBBBBB","אפור"),("#555555","אפור כהה"),("#000000","שחור"),
]

# ── Page thumbnail cache ─────────────────────────────────────────────────────────
_thumb_cache = {}


# ═══════════════════════════════════════════════════════════════════════════════
# Theme Menu
# ═══════════════════════════════════════════════════════════════════════════════

class ColoringMenu:
    def __init__(self, root, back_cb):
        self.root    = root
        self.back_cb = back_cb
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        self._build()

    def _build(self):
        self.frame = tk.Frame(self.root, bg=BG)
        self.frame.pack(fill="both", expand=True)

        # Back button
        top = tk.Frame(self.frame, bg=BG)
        top.pack(fill="x", padx=14, pady=(10, 0))
        tk.Button(top, text="← חזור", font=FONT_SM, bg="#ECF0F1",
                  fg=DARK, relief="flat", cursor="hand2",
                  command=self._back).pack(side="left")

        tk.Label(self.frame, text="🎨  ספר הצביעה שלי",
                 font=FONT_BIG, bg=BG, fg=DARK).pack(pady=(8, 4))
        tk.Label(self.frame, text="בחרי נושא לצביעה 👇",
                 font=FONT_SM, bg=BG, fg="#7F8C8D").pack(pady=(0, 12))

        # 5-column grid of theme buttons (2 rows for 10 themes)
        grid = tk.Frame(self.frame, bg=BG)
        grid.pack()

        for i, (name, key, color) in enumerate(THEMES):
            row, col = divmod(i, 3)  # Change to 3 columns
            btn = tk.Button(grid, text=name,
                            font=("Arial", 14, "bold"), fg=DARK,
                            bg=color, padx=10, pady=18,
                            relief="raised", bd=4, cursor="hand2", width=18,
                            highlightbackground=color,
                            command=lambda k=key: self._open_theme(k))
            btn.grid(row=row, column=col, padx=8, pady=7)

    def _open_theme(self, key):
        self.frame.destroy()
        ColoringBook(self.root, key, back_cb=self._rebuild)

    def _rebuild(self): self._build()
    def _back(self):    self.frame.destroy(); self.back_cb()


# ═══════════════════════════════════════════════════════════════════════════════
# Page selector
# ═══════════════════════════════════════════════════════════════════════════════

class ColoringBook:
    def __init__(self, root, theme_key, back_cb):
        self.root      = root
        self.theme_key = theme_key
        self.back_cb   = back_cb
        self.theme_dir = os.path.join(PAGES_DIR, theme_key)
        self._build()

    def _build(self):
        self.frame = tk.Frame(self.root, bg=BG)
        self.frame.pack(fill="both", expand=True)

        top = tk.Frame(self.frame, bg=BG)
        top.pack(fill="x", padx=14, pady=(10, 0))
        tk.Button(top, text="← חזור לנושאים", font=FONT_SM, bg="#ECF0F1",
                  fg=DARK, relief="flat", cursor="hand2",
                  command=self._back).pack(side="left")

        theme_name = next((n for n, k, _ in THEMES if k == self.theme_key), self.theme_key)
        tk.Label(self.frame, text=f"{theme_name}  — בחרי דף",
                 font=FONT_BIG, bg=BG, fg=DARK).pack(pady=(10, 14))

        pages_grid = tk.Frame(self.frame, bg=BG)
        pages_grid.pack(pady=6)

        pages = sorted(f for f in os.listdir(self.theme_dir) if f.endswith(".png"))
        self._thumbs = []

        for i, fn in enumerate(pages):
            path = os.path.join(self.theme_dir, fn)
            key  = path
            if key not in _thumb_cache:
                img = Image.open(path).resize((200, 150), Image.LANCZOS)
                _thumb_cache[key] = ImageTk.PhotoImage(img)
            thumb = _thumb_cache[key]
            self._thumbs.append(thumb)

            col, row_num = i % 3, i // 3  # Change to 3 columns
            card = tk.Frame(pages_grid, bg="white", bd=2, relief="groove")
            card.grid(row=row_num, column=col, padx=12, pady=10)

            tk.Button(card, image=thumb, relief="flat", cursor="hand2",
                      command=lambda p=path: self._open_page(p)).pack()
            tk.Label(card, text=f"דף {i+1}", font=FONT_SM,
                     bg="white", fg=DARK).pack(pady=3)

    def _open_page(self, path):
        self.frame.destroy()
        ColoringPageView(self.root, path, back_cb=self._rebuild)

    def _rebuild(self): self._build()
    def _back(self):    self.frame.destroy(); self.back_cb()


# ═══════════════════════════════════════════════════════════════════════════════
# Coloring page viewer  (the actual painting interface)
# ═══════════════════════════════════════════════════════════════════════════════

class ColoringPageView:
    MAX_UNDO = 15

    def __init__(self, root, page_path, back_cb):
        self.root          = root
        self.back_cb       = back_cb
        self.page_path     = page_path
        self.sel_hex       = "#FF0000"
        self.sel_rgb       = (255, 0, 0)
        self.history       = []
        self.color_buttons = {}

        self.root.geometry("1380x850")
        self.root.resizable(True, True)

        # Load image
        raw = Image.open(page_path)
        self.orig_pil    = raw.convert("RGB")
        self.current_pil = self.orig_pil.copy()
        self.pil_w       = self.orig_pil.width
        self.pil_h       = self.orig_pil.height

        self._build()
        self._refresh()

    # ── Build UI ──────────────────────────────────────────────────────────────
    def _build(self):
        self.frame = tk.Frame(self.root, bg=BG)
        self.frame.pack(fill="both", expand=True)

        # ── Top bar ──────────────────────────────────────────────────────────
        top = tk.Frame(self.frame, bg="#ECF0F1")
        top.pack(fill="x")

        tk.Button(top, text="← חזור", font=FONT_SM, bg="#ECF0F1",
                  fg=DARK, relief="flat", cursor="hand2",
                  command=self._back).pack(side="left", padx=10, pady=8)

        for text, bg_col, fg_col, cmd in [
            ("↩ בטל",      "#D1ECF1", "#0c5460", self._undo),
            ("🗑 נקה הכל", "#F8D7DA", "#721c24", self._clear_all),
            ("💾 שמור",    "#D4EDDA", "#155724", self._save),
        ]:
            tk.Button(top, text=text, font=FONT_SM, bg=bg_col, fg=fg_col,
                      relief="raised", bd=2, cursor="hand2",
                      command=cmd).pack(side="right", padx=6, pady=6)

        # ── Main area ─────────────────────────────────────────────────────────
        main = tk.Frame(self.frame, bg=BG)
        main.pack(fill="both", expand=True, padx=8, pady=5)

        # Palette sidebar
        self._build_palette(main)

        # Canvas
        right = tk.Frame(main, bg="white", bd=3, relief="groove")
        right.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(right, width=CANVAS_W, height=CANVAS_H,
                                bg="white", cursor="hand2",
                                highlightthickness=0)
        self.canvas.pack(padx=4, pady=4)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas_img = None

    def _build_palette(self, parent):
        pal = tk.Frame(parent, bg=PALETTE_BG, bd=2, relief="groove", width=360)
        pal.pack(side="left", fill="y", padx=(0, 8))
        pal.pack_propagate(False)

        tk.Label(pal, text="🎨 צבעים", font=("Arial", 15, "bold"),
                 bg=PALETTE_BG, fg=DARK).pack(pady=(10, 5))

        # Selected color preview + name
        preview_frame = tk.Frame(pal, bg=PALETTE_BG)
        preview_frame.pack(pady=(0, 6), padx=10, fill="x")
        self.sel_preview = tk.Label(preview_frame, text="  ", bg=self.sel_hex,
                                    width=4, height=2, relief="sunken", bd=3)
        self.sel_preview.pack(side="right", padx=(4, 8))
        self.color_name_lbl = tk.Label(preview_frame, text=PALETTE[0][1],
                                        font=("Arial", 12, "bold"),
                                        bg=PALETTE_BG, fg=DARK,
                                        anchor="e", justify="right", wraplength=125)
        self.color_name_lbl.pack(side="right", expand=True, fill="x")

        # 6 rows × 4 cols = 24 swatches
        grid = tk.Frame(pal, bg=PALETTE_BG)
        grid.pack(padx=6, pady=4)

        for i, (hex_col, name) in enumerate(PALETTE):
            row, col = divmod(i, 4)
            # macOS fix: highlightbackground is needed to show button color
            btn = tk.Button(grid, bg=hex_col, width=4, height=1,
                            relief="flat", bd=0, cursor="hand2",
                            highlightbackground=hex_col,
                            activebackground=hex_col,
                            command=lambda h=hex_col: self._pick_color(h))
            btn.grid(row=row, column=col, padx=2, pady=2)
            btn.bind("<Enter>", lambda e, n=name, b=btn: (
                self.color_name_lbl.config(text=n)))
            self.color_buttons[hex_col] = btn

    # ── Color picking ─────────────────────────────────────────────────────────
    def _pick_color(self, hex_col):
        old_btn = self.color_buttons.get(self.sel_hex)
        if old_btn:
            old_btn.config(relief="raised", bd=2)
        self.sel_hex = hex_col
        self.sel_rgb = self._hex_to_rgb(hex_col)
        self.sel_preview.config(bg=hex_col)
        new_btn = self.color_buttons.get(hex_col)
        if new_btn:
            new_btn.config(relief="sunken", bd=4)
        name = next((n for h, n in PALETTE if h == hex_col), "")
        self.color_name_lbl.config(text=name)

    @staticmethod
    def _hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    # ── Canvas painting ───────────────────────────────────────────────────────
    def _on_click(self, event):
        # Map canvas → PIL coords
        sx = self.pil_w / CANVAS_W
        sy = self.pil_h / CANVAS_H
        px = max(0, min(int(event.x * sx), self.pil_w - 1))
        py = max(0, min(int(event.y * sy), self.pil_h - 1))

        # Don't paint over black outlines
        pixel = self.current_pil.getpixel((px, py))
        if all(c < 60 for c in pixel[:3]):
            return

        # Save for undo
        self.history.append(self.current_pil.copy())
        if len(self.history) > self.MAX_UNDO:
            self.history.pop(0)

        # Bucket fill
        img = self.current_pil.copy()
        ImageDraw.floodfill(img, (px, py), self.sel_rgb, thresh=35)
        self.current_pil = img
        self._refresh()

    def _refresh(self):
        display = self.current_pil.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
        self._tk_img = ImageTk.PhotoImage(display)
        if self.canvas_img is None:
            self.canvas_img = self.canvas.create_image(0, 0, anchor="nw",
                                                        image=self._tk_img)
        else:
            self.canvas.itemconfig(self.canvas_img, image=self._tk_img)

    # ── Actions ───────────────────────────────────────────────────────────────
    def _undo(self):
        if self.history:
            self.current_pil = self.history.pop()
            self._refresh()

    def _clear_all(self):
        self.history.append(self.current_pil.copy())
        self.current_pil = self.orig_pil.copy()
        self._refresh()

    def _save(self):
        save_dir = os.path.expanduser("~/Desktop/צביעות")
        os.makedirs(save_dir, exist_ok=True)
        ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(save_dir, f"צביעה_{ts}.png")
        self.current_pil.save(path)
        # Flash the save button green briefly
        self.frame.after(50, lambda: None)

    def _back(self):
        _thumb_cache.clear()
        self.frame.destroy()
        self.root.resizable(True, True)
        self.root.geometry("1100x750")
        self.back_cb()
