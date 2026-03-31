"""
writing_game.py – Hebrew writing practice for kids
  Mode A: Given an image → type the FIRST LETTER of the word
  Mode B: Given an image → type the FULL WORD (with blank lines)
  Both modes: 🔊 button reads the word aloud via Mac TTS
"""

import tkinter as tk
import random
import math
import os
try:
    from PIL import Image as _PILImage, ImageTk as _ImageTk
    _PIL_OK = True
except ImportError:
    _PIL_OK = False
from shared import (
    BG, DARK, BTN_GREEN, BTN_RED, BTN_BLUE, BTN_ORANGE,
    FONT_TITLE, FONT_HEB, FONT_SMALL,
    PRAISES, TRY_AGAIN,
    play_sound, make_scrollable, shake, hearts_str, say_hebrew,
)

# Folder with pre-generated PNG images (260x220)
_HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(_HERE, 'images')

# ═══════════════════════════════════════════════════════════════════════════════
# Image drawing functions – all on a 260×220 canvas
# ═══════════════════════════════════════════════════════════════════════════════

def _draw_apple(c):
    c.create_oval(40, 30, 220, 190, fill="#E74C3C", outline="#C0392B", width=3)
    c.create_rectangle(116, 10, 122, 40, fill="#8B4513", outline="")
    c.create_oval(108, 15, 128, 40, fill="#27AE60", outline="")
    c.create_oval(65, 70, 95, 100, fill="#F1948A", outline="")

def _draw_butterfly(c):
    c.create_oval(30, 60, 130, 150, fill="#9B59B6", outline="#6C3483", width=2)
    c.create_oval(30, 90, 130, 180, fill="#D2B4DE", outline="#9B59B6", width=2)
    c.create_oval(130, 60, 230, 150, fill="#E74C3C", outline="#A93226", width=2)
    c.create_oval(130, 90, 230, 180, fill="#F1948A", outline="#E74C3C", width=2)
    c.create_oval(118, 60, 142, 190, fill="#1A1A1A", outline="")
    c.create_line(130, 65, 100, 30, fill="#1A1A1A", width=2)
    c.create_oval(96, 25, 106, 35, fill="#1A1A1A")
    c.create_line(130, 65, 160, 30, fill="#1A1A1A", width=2)
    c.create_oval(154, 25, 164, 35, fill="#1A1A1A")

def _draw_sun(c):
    cx, cy, r = 130, 115, 58
    for i in range(12):
        a = math.radians(i * 30)
        c.create_line(cx+(r+5)*math.cos(a), cy+(r+5)*math.sin(a),
                      cx+(r+22)*math.cos(a), cy+(r+22)*math.sin(a),
                      fill="#F39C12", width=4, capstyle="round")
    c.create_oval(cx-r, cy-r, cx+r, cy+r, fill="#F1C40F", outline="#F39C12", width=3)

def _draw_moon(c):
    c.create_oval(60, 25, 220, 195, fill="#F7DC6F", outline="#F1C40F", width=3)
    c.create_oval(90, 20, 240, 190, fill=BG, outline="")
    for sx, sy in [(40, 40), (220, 50), (50, 160), (230, 170)]:
        c.create_text(sx, sy, text="★", font=("Arial", 14), fill="#F1C40F")

def _draw_tree(c):
    c.create_rectangle(108, 150, 152, 210, fill="#8B4513", outline="#6B3410", width=2)
    c.create_polygon(130, 20, 50, 130, 210, 130, fill="#27AE60", outline="#1E8449", width=2)
    c.create_polygon(130, 50, 60, 145, 200, 145, fill="#2ECC71", outline="#27AE60", width=2)
    c.create_polygon(130, 80, 70, 165, 190, 165, fill="#58D68D", outline="#2ECC71", width=2)

def _draw_fish(c):
    c.create_oval(60, 80, 200, 160, fill="#3498DB", outline="#2980B9", width=2)
    c.create_polygon(195, 120, 240, 75, 240, 165, fill="#2980B9", outline="#1F618D", width=2)
    c.create_oval(85, 100, 105, 120, fill="white", outline="#1A1A1A", width=2)
    c.create_oval(90, 105, 100, 115, fill="#1A1A1A")
    c.create_polygon(120, 82, 140, 40, 160, 82, fill="#5DADE2", outline="#2E86C1", width=2)

def _draw_house(c):
    c.create_rectangle(50, 110, 210, 200, fill="#E8D5B7", outline=DARK, width=2)
    c.create_polygon(35, 115, 130, 30, 225, 115, fill="#E74C3C", outline="#C0392B", width=3)
    c.create_rectangle(107, 148, 153, 200, fill="#8B4513", outline=DARK, width=2)
    c.create_oval(148, 170, 155, 177, fill="#F1C40F")
    for wx in [65, 170]:
        c.create_rectangle(wx, 125, wx+35, 155, fill="#AED6F1", outline=DARK, width=2)

def _draw_flower(c):
    cx, cy = 130, 130
    colours = ["#E74C3C", "#F1C40F", "#E91E63", "#FF9800", "#9C27B0"]
    for i, deg in enumerate([0, 72, 144, 216, 288]):
        a = math.radians(deg)
        px, py = cx + 45*math.cos(a), cy + 45*math.sin(a)
        c.create_oval(px-25, py-25, px+25, py+25,
                      fill=colours[i % len(colours)], outline="white", width=2)
    c.create_oval(cx-22, cy-22, cx+22, cy+22, fill="#F1C40F", outline="#F39C12", width=2)
    c.create_line(130, 152, 130, 210, fill="#27AE60", width=5)

def _draw_dog(c):
    c.create_oval(60, 100, 200, 190, fill="#C8A87A", outline="#A08060", width=2)
    c.create_oval(120, 40, 210, 120, fill="#C8A87A", outline="#A08060", width=2)
    c.create_oval(185, 35, 220, 80, fill="#996633", outline="#7A5229", width=2)
    c.create_oval(120, 35, 145, 75, fill="#996633", outline="", width=2)
    c.create_oval(150, 65, 168, 83, fill="white", outline=DARK, width=2)
    c.create_oval(155, 70, 163, 78, fill=DARK)
    c.create_oval(160, 95, 180, 110, fill="#E91E63", outline="#AD1457", width=2)
    c.create_line(62, 100, 30, 55, fill="#C8A87A", width=8, capstyle="round")

def _draw_cat(c):
    c.create_oval(55, 110, 200, 200, fill="#95A5A6", outline="#7F8C8D", width=2)
    c.create_oval(105, 35, 200, 125, fill="#95A5A6", outline="#7F8C8D", width=2)
    c.create_polygon(108, 50, 90, 15, 130, 50, fill="#95A5A6", outline="#7F8C8D", width=2)
    c.create_polygon(197, 50, 215, 15, 175, 50, fill="#95A5A6", outline="#7F8C8D", width=2)
    c.create_polygon(112, 48, 98, 22, 128, 48, fill="#E91E63", outline="")
    c.create_polygon(193, 48, 207, 22, 175, 48, fill="#E91E63", outline="")
    for ex in [125, 170]:
        c.create_oval(ex, 60, ex+20, 82, fill="#2ECC71", outline=DARK, width=2)
        c.create_oval(ex+6, 65, ex+14, 77, fill=DARK)
    c.create_polygon(148, 95, 155, 102, 142, 102, fill="#E91E63")
    for wx1, wy1, wx2, wy2 in [(90, 92, 138, 98), (90, 100, 138, 100),
                                (162, 98, 210, 92), (162, 100, 210, 100)]:
        c.create_line(wx1, wy1, wx2, wy2, fill=DARK, width=1)

def _draw_book(c):
    c.create_rectangle(45, 40, 215, 195, fill="#E74C3C", outline="#C0392B", width=3)
    c.create_rectangle(120, 40, 135, 195, fill="#C0392B", outline="")
    c.create_rectangle(50, 50, 115, 185, fill="#FDFEFE", outline="")
    c.create_rectangle(140, 50, 205, 185, fill="#FDFEFE", outline="")
    for ly in range(70, 180, 18):
        c.create_line(58, ly, 108, ly, fill="#BDC3C7", width=2)
        c.create_line(148, ly, 198, ly, fill="#BDC3C7", width=2)

def _draw_star(c):
    cx, cy, R, r = 130, 115, 95, 40
    pts = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        radius = R if i % 2 == 0 else r
        pts.extend([cx + radius*math.cos(angle), cy + radius*math.sin(angle)])
    c.create_polygon(pts, fill="#F1C40F", outline="#F39C12", width=3)

def _draw_car(c):
    c.create_rectangle(30, 130, 230, 185, fill="#3498DB", outline="#2980B9", width=3)
    c.create_rectangle(65, 85, 185, 135, fill="#5DADE2", outline="#2980B9", width=2)
    c.create_rectangle(72, 92, 125, 130, fill="#AED6F1", outline="#2980B9", width=2)
    c.create_rectangle(135, 92, 178, 130, fill="#AED6F1", outline="#2980B9", width=2)
    for wx in [70, 170]:
        c.create_oval(wx-30, 160, wx+30, 210, fill=DARK, outline="#1A1A1A", width=3)
        c.create_oval(wx-16, 174, wx+16, 198, fill="#7F8C8D")
    c.create_oval(205, 145, 225, 165, fill="#F1C40F", outline="#F39C12", width=2)

def _draw_heart(c):
    cx, cy = 130, 120
    pts = []
    for t_deg in range(0, 361, 3):
        t = math.radians(t_deg)
        x = 16 * math.sin(t) ** 3
        y = -(13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t))
        pts.extend([cx + x*6.5, cy + y*6.5])
    c.create_polygon(pts, fill="#E74C3C", outline="#C0392B", width=3, smooth=True)

def _draw_cloud(c):
    for ox, oy, r in [(80, 130, 45), (130, 110, 55), (180, 130, 45),
                       (55, 155, 35), (205, 155, 35), (130, 155, 45)]:
        c.create_oval(ox-r, oy-r, ox+r, oy+r, fill="white", outline="#BDC3C7", width=2)
    for rx, ry in [(75, 200), (110, 210), (145, 205), (180, 210), (210, 198)]:
        c.create_line(rx, ry, rx-5, ry+20, fill="#5DADE2", width=3, capstyle="round")

def _draw_banana(c):
    c.create_arc(50, 50, 210, 200, start=210, extent=120, style="arc",
                 outline="#F1C40F", width=28)
    c.create_arc(55, 55, 205, 195, start=210, extent=120, style="arc",
                 outline="#F39C12", width=6)
    c.create_oval(65, 145, 83, 163, fill="#8B4513", outline="")
    c.create_oval(183, 68, 201, 86, fill="#8B4513", outline="")

def _draw_ball(c):
    c.create_oval(35, 30, 225, 210, fill="#E74C3C", outline="#C0392B", width=4)
    c.create_arc(35, 30, 225, 210, start=0, extent=180, style="arc",
                 outline="white", width=4)
    c.create_arc(60, 30, 200, 210, start=70, extent=40, style="arc",
                 outline="white", width=4)
    c.create_arc(60, 30, 200, 210, start=250, extent=40, style="arc",
                 outline="white", width=4)

# ── NEW words ──────────────────────────────────────────────────────────────────

def _draw_train(c):
    # Engine body
    c.create_rectangle(30, 110, 160, 175, fill="#E74C3C", outline="#C0392B", width=2)
    # Cab
    c.create_rectangle(60, 75, 155, 115, fill="#C0392B", outline="#A93226", width=2)
    # Window
    c.create_rectangle(80, 85, 135, 108, fill="#AED6F1", outline=DARK, width=2)
    # Chimney + smoke
    c.create_rectangle(40, 60, 62, 115, fill="#C0392B", outline="#A93226", width=2)
    for sx, sy, sz in [(46, 45, 10), (52, 30, 12), (62, 18, 9)]:
        c.create_oval(sx-sz, sy-sz, sx+sz, sy+sz, fill="#95A5A6", outline="")
    # Wheels
    for wx in [55, 105, 135]:
        c.create_oval(wx-20, 165, wx+20, 205, fill=DARK, outline="#7F8C8D", width=2)
        c.create_oval(wx-10, 175, wx+10, 195, fill="#7F8C8D")
    # Wagon
    c.create_rectangle(170, 120, 245, 175, fill="#2980B9", outline="#1A5276", width=2)
    for wx in [185, 225]:
        c.create_oval(wx-14, 165, wx+14, 193, fill=DARK, outline="#7F8C8D", width=2)
    # Coupler
    c.create_line(160, 147, 170, 147, fill=DARK, width=4)

def _draw_cake(c):
    # Layers
    c.create_rectangle(40, 130, 220, 175, fill="#F9E4D4", outline="#E67E22", width=2)
    c.create_rectangle(55, 90, 205, 135, fill="#FDEBD0", outline="#E67E22", width=2)
    c.create_rectangle(75, 58, 185, 95, fill="#F9E4D4", outline="#E67E22", width=2)
    # Frosting drips
    for fx in [60, 95, 130, 165, 195]:
        c.create_oval(fx-9, 128, fx+9, 145, fill="white", outline="")
    for fx in [75, 110, 145, 175]:
        c.create_oval(fx-9, 87, fx+9, 104, fill="white", outline="")
    # Candles
    candle_cols = ["#E74C3C", "#F1C40F", "#27AE60", "#9B59B6"]
    for i, cx in enumerate([95, 120, 145, 165]):
        c.create_rectangle(cx-4, 32, cx+4, 60, fill=candle_cols[i % 4], outline="")
        c.create_oval(cx-5, 22, cx+5, 36, fill="#F1C40F", outline="#F39C12")
    # Stars decoration
    for sx, sy in [(55, 155), (200, 155), (65, 115), (192, 115)]:
        c.create_text(sx, sy, text="✦", font=("Arial", 11), fill="#E67E22")

def _draw_icecream(c):
    # Cone
    c.create_polygon(80, 210, 180, 210, 130, 80, fill="#C8A87A", outline="#A08060", width=2)
    # Cone lines
    for lx in range(90, 175, 15):
        c.create_line(lx, 210, 130 + (lx-130)*0.3, 100, fill="#A08060", width=1)
    # Scoops
    c.create_oval(70, 35, 190, 110, fill="#F48FB1", outline="#E91E63", width=3)  # pink
    c.create_oval(80, 25, 180, 80, fill="#FFFDE7", outline="#F1C40F", width=3)   # vanilla
    # Sprinkles
    colors_s = ["#E74C3C", "#3498DB", "#27AE60", "#F1C40F", "#9B59B6"]
    import random as _r
    _r.seed(42)
    for _ in range(12):
        sx = _r.randint(85, 175); sy = _r.randint(30, 75)
        c.create_rectangle(sx, sy, sx+6, sy+2, fill=_r.choice(colors_s), outline="")
    # Cherry on top
    c.create_oval(118, 14, 142, 38, fill="#E74C3C", outline="#C0392B", width=2)
    c.create_line(130, 14, 125, 5, fill="#27AE60", width=2)

def _draw_boat(c):
    # Hull
    c.create_polygon(20, 155, 240, 155, 210, 200, 50, 200,
                     fill="#E74C3C", outline="#C0392B", width=2)
    # Mast
    c.create_line(130, 155, 130, 40, fill="#8B4513", width=4)
    # Sail
    c.create_polygon(130, 45, 130, 145, 210, 120, fill="white", outline="#BDC3C7", width=2)
    c.create_polygon(130, 55, 130, 145, 55, 130, fill="#AED6F1", outline="#85C1E9", width=2)
    # Flag
    c.create_polygon(130, 40, 155, 52, 130, 64, fill="#F1C40F", outline="#F39C12", width=1)
    # Water waves
    for wy in [210, 218]:
        for wx in range(0, 260, 32):
            c.create_arc(wx, wy, wx+32, wy+14, start=0, extent=180,
                         style="arc", outline="#5DADE2", width=3)

def _draw_rabbit(c):
    # Body
    c.create_oval(60, 115, 200, 210, fill="white", outline="#BDC3C7", width=2)
    # Head
    c.create_oval(80, 55, 180, 135, fill="white", outline="#BDC3C7", width=2)
    # Ears
    c.create_oval(90, 10, 118, 70, fill="white", outline="#BDC3C7", width=2)
    c.create_oval(95, 14, 113, 66, fill="#F8BBD0", outline="")
    c.create_oval(142, 10, 170, 70, fill="white", outline="#BDC3C7", width=2)
    c.create_oval(147, 14, 165, 66, fill="#F8BBD0", outline="")
    # Eyes
    c.create_oval(100, 78, 118, 96, fill="#E91E63", outline="#880E4F", width=2)
    c.create_oval(142, 78, 160, 96, fill="#E91E63", outline="#880E4F", width=2)
    # Nose
    c.create_oval(122, 105, 138, 118, fill="#F48FB1", outline="")
    # Mouth
    c.create_arc(112, 110, 130, 126, start=200, extent=140, style="arc",
                 outline="#BDC3C7", width=2)
    c.create_arc(130, 110, 148, 126, start=200, extent=140, style="arc",
                 outline="#BDC3C7", width=2)
    # Tail
    c.create_oval(170, 170, 210, 210, fill="white", outline="#BDC3C7", width=2)

def _draw_strawberry(c):
    # Body (slightly heart-shaped)
    pts = []
    cx, cy = 130, 115
    for t in range(0, 361, 4):
        t_r = math.radians(t)
        x = 14 * math.sin(t_r)**3
        y = -(12*math.cos(t_r) - 5*math.cos(2*t_r) - 2*math.cos(3*t_r) - math.cos(4*t_r))
        pts.extend([cx + x*5.5, cy + y*5.5])
    c.create_polygon(pts, fill="#E74C3C", outline="#C0392B", width=2, smooth=True)
    # Seeds
    seed_positions = [(115,100),(130,90),(145,100),(110,120),(130,120),(150,120),
                      (118,140),(142,140),(130,155)]
    for sx, sy in seed_positions:
        c.create_oval(sx-4, sy-5, sx+4, sy+3, fill="#F1C40F", outline="#F39C12", width=1)
    # Leaves/calyx
    for lx, ly in [(115, 70), (130, 60), (145, 70), (108, 82), (152, 82)]:
        c.create_polygon(130, 85, lx-8, ly, lx+8, ly, fill="#27AE60", outline="#1E8449")
    # Stem
    c.create_line(130, 62, 128, 35, fill="#27AE60", width=3)

def _draw_pencil(c):
    # Body (rotated 20°-ish — draw straight for simplicity)
    c.create_rectangle(80, 25, 170, 165, fill="#F1C40F", outline="#F39C12", width=2)
    # Top eraser band
    c.create_rectangle(80, 25, 170, 48, fill="#BDC3C7", outline="#95A5A6", width=2)
    # Eraser
    c.create_rectangle(80, 25, 170, 38, fill="#F48FB1", outline="#E91E63", width=1)
    # Ferrule (metal band)
    c.create_rectangle(80, 155, 170, 168, fill="#BDC3C7", outline="#95A5A6", width=2)
    # Tip / wood
    c.create_polygon(80, 165, 170, 165, 125, 210, fill="#C8A87A", outline="#A08060", width=2)
    # Graphite tip
    c.create_polygon(105, 200, 145, 200, 125, 215, fill="#555", outline="")
    # Lines on body simulating wood grain
    for lx in [100, 120, 140, 160]:
        c.create_line(lx, 48, lx, 155, fill="#F39C12", width=1)

def _draw_elephant(c):
    # Body
    c.create_oval(40, 85, 220, 200, fill="#95A5A6", outline="#7F8C8D", width=2)
    # Head
    c.create_oval(130, 40, 245, 135, fill="#95A5A6", outline="#7F8C8D", width=2)
    # Ear
    c.create_oval(35, 55, 115, 145, fill="#BDC3C7", outline="#95A5A6", width=2)
    c.create_oval(48, 68, 100, 130, fill="#F8BBD0", outline="")
    # Trunk (curved via arc)
    c.create_arc(170, 100, 260, 200, start=180, extent=-180, style="arc",
                 outline="#7F8C8D", width=14)
    c.create_arc(155, 185, 260, 230, start=0, extent=180, style="arc",
                 outline="#7F8C8D", width=14)
    # Eye
    c.create_oval(215, 60, 235, 80, fill="white", outline=DARK, width=2)
    c.create_oval(220, 65, 230, 75, fill=DARK)
    # Legs
    for lx in [68, 108, 153, 193]:
        c.create_rectangle(lx, 185, lx+28, 218, fill="#95A5A6", outline="#7F8C8D", width=2)
    # Tail
    c.create_line(42, 130, 22, 108, 18, 90, fill="#7F8C8D", width=4, smooth=True)


# ── Extra word drawings ────────────────────────────────────────────────────────

def _draw_grape(c):
    """ענב – a bunch of grapes"""
    positions = [
        (95,75),(130,75),(165,75),
        (112,100),(147,100),
        (95,125),(130,125),(165,125),
        (112,150),(147,150),
        (130,175),
    ]
    for gx, gy in positions:
        c.create_oval(gx-16, gy-16, gx+16, gy+16,
                      fill="#8E44AD", outline="#6C3483", width=2)
        c.create_oval(gx-8, gy-10, gx-2, gy-4,
                      fill="#BB8FCE", outline="")
    # Stem and leaves
    c.create_line(130, 58, 130, 35, fill="#8B4513", width=3)
    c.create_oval(110, 25, 130, 45, fill="#27AE60", outline="#1E8449", width=1)
    c.create_oval(130, 25, 150, 45, fill="#2ECC71", outline="#27AE60", width=1)

def _draw_eye(c):
    """עין – a big illustrative eye"""
    # Outer eye shape (almondish)
    c.create_arc(30, 80, 230, 160, start=0, extent=180, style="chord",
                 fill="white", outline="#2C3E50", width=3)
    c.create_arc(30, 80, 230, 160, start=180, extent=180, style="chord",
                 fill="white", outline="#2C3E50", width=3)
    # Iris
    c.create_oval(85, 85, 175, 160, fill="#2980B9", outline="#1A5276", width=3)
    # Pupil
    c.create_oval(105, 95, 155, 150, fill="#1A1A1A", outline="")
    # Shine
    c.create_oval(115, 100, 130, 115, fill="white", outline="")
    # Eyelashes
    lash_pts = [(50,110),(40,90),(60,70),(80,60),(100,50),
                (160,50),(180,60),(200,70),(220,90),(210,110)]
    for i, (lx, ly) in enumerate(lash_pts):
        ex = 30 + i*20
        c.create_line(ex, 80 + (80-80)//2, lx, ly,
                      fill="#2C3E50", width=2, capstyle="round")
    # Eyebrow
    c.create_arc(30, 30, 230, 90, start=0, extent=180, style="arc",
                 outline="#2C3E50", width=5)

def _draw_crow(c):
    """עורב – a crow / raven on a branch"""
    # Branch
    c.create_line(10, 170, 250, 170, fill="#8B4513", width=10, capstyle="round")
    c.create_line(60, 170, 55, 200, fill="#8B4513", width=6)
    c.create_line(130, 170, 125, 205, fill="#8B4513", width=6)
    c.create_line(200, 170, 195, 200, fill="#8B4513", width=6)
    # Body
    c.create_oval(80, 85, 190, 165, fill="#2C3E50", outline="#1A252F", width=2)
    # Head
    c.create_oval(150, 60, 220, 120, fill="#2C3E50", outline="#1A252F", width=2)
    # Beak
    c.create_polygon(215, 85, 248, 92, 215, 100,
                     fill="#7F8C8D", outline="#626567", width=1)
    # Eye
    c.create_oval(190, 72, 208, 90, fill="white", outline="#1A252F", width=2)
    c.create_oval(195, 77, 205, 87, fill="#2C3E50")
    c.create_oval(197, 79, 201, 83, fill="white", outline="")
    # Wing highlight
    c.create_arc(85, 90, 185, 160, start=200, extent=100, style="arc",
                 outline="#566573", width=3)
    # Tail feathers
    c.create_polygon(80, 130, 30, 155, 80, 150, fill="#2C3E50", outline="")
    c.create_polygon(80, 140, 20, 170, 80, 162, fill="#34495E", outline="")
    # Feet
    for fx in [115, 145]:
        c.create_line(fx, 163, fx, 172, fill="#7F8C8D", width=3)
        c.create_line(fx, 172, fx-12, 176, fill="#7F8C8D", width=2)
        c.create_line(fx, 172, fx+12, 176, fill="#7F8C8D", width=2)
        c.create_line(fx, 172, fx, 178, fill="#7F8C8D", width=2)

def _draw_lion(c):
    """אריה – a cute lion face"""
    # Mane
    for deg in range(0, 360, 30):
        a = math.radians(deg)
        mx = 130 + 80*math.cos(a)
        my = 120 + 80*math.sin(a)
        c.create_oval(mx-18, my-18, mx+18, my+18,
                      fill="#E67E22", outline="#D35400", width=1)
    # Face
    c.create_oval(65, 55, 195, 185, fill="#F5CBA7", outline="#E59866", width=3)
    # Eyes
    for ex in [100, 160]:
        c.create_oval(ex-14, 90, ex+14, 118, fill="#F1C40F", outline="#D4AC0D", width=2)
        c.create_oval(ex-7, 97, ex+7, 111, fill="#2C3E50", outline="")
        c.create_oval(ex-4, 99, ex, 103, fill="white", outline="")
    # Nose
    c.create_oval(116, 130, 144, 152, fill="#E74C3C", outline="#C0392B", width=2)
    # Mouth
    c.create_line(130, 152, 110, 168, fill="#C0392B", width=2)
    c.create_line(130, 152, 150, 168, fill="#C0392B", width=2)
    # Ears
    c.create_oval(62, 50, 95, 85, fill="#F5CBA7", outline="#E59866", width=2)
    c.create_oval(165, 50, 198, 85, fill="#F5CBA7", outline="#E59866", width=2)
    c.create_oval(68, 55, 87, 78, fill="#E59866", outline="")
    c.create_oval(171, 55, 190, 78, fill="#E59866", outline="")

def _draw_bird(c):
    """ציפור – a colourful bird on a perch"""
    # Perch
    c.create_line(40, 175, 220, 175, fill="#8B4513", width=8, capstyle="round")
    # Body (teardrop using oval)
    c.create_oval(75, 95, 185, 170, fill="#E74C3C", outline="#C0392B", width=2)
    # Wing
    c.create_polygon(80, 120, 45, 155, 110, 155, fill="#E91E63",
                     outline="#AD1457", width=2)
    c.create_arc(45, 125, 110, 160, start=200, extent=120,
                 style="arc", outline="#F48FB1", width=3)
    # Tail feathers
    c.create_polygon(75, 150, 30, 180, 75, 165, fill="#9B59B6", outline="")
    c.create_polygon(75, 155, 18, 185, 75, 170, fill="#8E44AD", outline="")
    # Head
    c.create_oval(145, 55, 215, 125, fill="#F1C40F", outline="#F39C12", width=2)
    # Eye
    c.create_oval(168, 68, 186, 86, fill="white", outline=DARK, width=2)
    c.create_oval(173, 73, 181, 81, fill=DARK)
    c.create_oval(174, 74, 177, 77, fill="white", outline="")
    # Beak
    c.create_polygon(208, 85, 235, 95, 208, 105,
                     fill="#F39C12", outline="#D68910", width=1)
    # Feet
    for fx in [120, 145]:
        c.create_line(fx, 168, fx, 177, fill="#F39C12", width=3)
        c.create_line(fx, 177, fx-10, 183, fill="#F39C12", width=2)
        c.create_line(fx, 177, fx+10, 183, fill="#F39C12", width=2)

def _draw_turtle(c):
    """צב – a cute turtle"""
    # Shadow
    c.create_oval(50, 185, 210, 215, fill="#BDC3C7", outline="")
    # Shell
    c.create_oval(55, 80, 205, 185, fill="#27AE60", outline="#1E8449", width=3)
    # Shell pattern (hexagon-like cells)
    hex_centers = [(130,120),(105,105),(155,105),(105,140),(155,140),(130,88),(130,152)]
    for hx, hy in hex_centers:
        c.create_oval(hx-16, hy-13, hx+16, hy+13,
                      fill="#2ECC71", outline="#1E8449", width=1)
    # Head
    c.create_oval(155, 55, 220, 110, fill="#A9BE8C", outline="#7B9E60", width=2)
    # Eye
    c.create_oval(185, 62, 202, 79, fill="white", outline=DARK, width=2)
    c.create_oval(190, 67, 198, 75, fill=DARK)
    c.create_oval(191, 68, 194, 71, fill="white", outline="")
    # Mouth (smile)
    c.create_arc(165, 85, 210, 108, start=200, extent=140, style="arc",
                 outline="#7B9E60", width=2)
    # Legs
    for lx, ly, ang in [(70,90,220),(70,165,130),(190,90,-40),(190,165,40)]:
        endx = lx + 38*math.cos(math.radians(ang))
        endy = ly + 28*math.sin(math.radians(ang))
        c.create_oval(endx-16, endy-12, endx+16, endy+12,
                      fill="#A9BE8C", outline="#7B9E60", width=2)
        c.create_line(lx, ly, endx, endy, fill="#A9BE8C", width=10, capstyle="round")
    # Tail
    c.create_line(60, 140, 30, 155, fill="#A9BE8C", width=8, capstyle="round")

def _draw_kite(c):
    """עפיפון – a diamond kite with tail"""
    # Kite diamond
    c.create_polygon(130, 20, 220, 120, 130, 195, 40, 120,
                     fill="#E74C3C", outline="#C0392B", width=3)
    # Cross sticks
    c.create_line(130, 20, 130, 195, fill="#8B4513", width=3)
    c.create_line(40, 120, 220, 120, fill="#8B4513", width=3)
    # Color quarters
    c.create_polygon(130, 20, 220, 120, 130, 120, fill="#F1C40F", outline="")
    c.create_polygon(130, 20, 40, 120, 130, 120, fill="#E74C3C", outline="")
    c.create_polygon(130, 195, 220, 120, 130, 120, fill="#9B59B6", outline="")
    c.create_polygon(130, 195, 40, 120, 130, 120, fill="#27AE60", outline="")
    # Sticks on top
    c.create_line(130, 20, 130, 195, fill="#8B4513", width=2)
    c.create_line(40, 120, 220, 120, fill="#8B4513", width=2)
    # Outline again on top
    c.create_polygon(130, 20, 220, 120, 130, 195, 40, 120,
                     fill="", outline="#2C3E50", width=2)
    # Tail
    tail_pts = [130, 195, 125, 210, 135, 225, 125, 240]
    c.create_line(*tail_pts, fill="#E67E22", width=3,
                  smooth=True, capstyle="round")
    # Bow ties on tail
    for ty in [208, 228]:
        c.create_oval(118, ty-5, 142, ty+5, fill="#E91E63", outline="")
    # String to bottom
    c.create_line(130, 195, 130, 215, fill="#7F8C8D", width=1, dash=(4,3))


# ── Word database ─────────────────────────────────────────────────────────────
# (word_plain, word_niqqud, first_letter, draw_fn)
_nopil = lambda c: None   # placeholder for PIL-only images

WORDS = [
    ("תפוח",  "תַּפּוּחַ",  "ת", _draw_apple),
    ("פרפר",  "פַּרְפַּר",  "פ", _draw_butterfly),
    ("שמש",   "שֶׁמֶשׁ",    "ש", _draw_sun),
    ("ירח",   "יָרֵחַ",    "י", _draw_moon),
    ("עץ",    "עֵץ",       "ע", _draw_tree),
    ("דג",    "דָּג",      "ד", _draw_fish),
    ("בית",   "בַּיִת",    "ב", _draw_house),
    ("פרח",   "פֶּרַח",    "פ", _draw_flower),
    ("כלב",   "כֶּלֶב",    "כ", _draw_dog),
    ("חתול",  "חָתוּל",    "ח", _draw_cat),
    ("ספר",   "סֵפֶר",     "ס", _draw_book),
    ("כוכב",  "כּוֹכָב",   "כ", _draw_star),
    ("אוטו",  "אוֹטוֹ",    "א", _draw_car),
    ("לב",    "לֵב",       "ל", _draw_heart),
    ("ענן",   "עָנָן",     "ע", _draw_cloud),
    ("בננה",  "בַּנָּנָה",  "ב", _draw_banana),
    ("כדור",  "כַּדּוּר",  "כ", _draw_ball),
    ("רכבת",  "רַכֶּבֶת",  "ר", _draw_train),
    ("עוגה",  "עוּגָה",    "ע", _draw_cake),
    ("גלידה", "גְּלִידָה", "ג", _draw_icecream),
    ("ספינה", "סְפִינָה",  "ס", _draw_boat),
    ("ארנב",  "אַרְנָב",   "א", _draw_rabbit),
    ("תות",   "תּוּת",     "ת", _draw_strawberry),
    ("עפרון", "עִפָּרוֹן", "ע", _draw_pencil),
    ("פיל",   "פִּיל",     "פ", _draw_elephant),
    # NEW – including ע words
    ("ענב",   "עֵנָב",     "ע", _draw_grape),
    ("עין",   "עַיִן",     "ע", _draw_eye),
    ("עורב",  "עוֹרֵב",    "ע", _draw_crow),
    ("עפיפון","עֲפִיפוֹן", "ע", _draw_kite),
    ("אריה",  "אַרְיֵה",   "א", _draw_lion),
    ("ציפור", "צִפּוֹר",   "צ", _draw_bird),
    ("צב",    "צָב",       "צ", _draw_turtle),
    # NEW – 18 more words (PIL images only, canvas fallback is a no-op)
    ("ים",     "יָם",        "י", _nopil),
    ("שולחן", "שֻלְחָן",  "ש", _nopil),
    ("כיסא",  "כִּיסֵא",   "כ", _nopil),
    ("מטוס",  "מָטֹס",    "מ", _nopil),
    ("טיל",   "טִיל",      "ט", _nopil),
    ("דלת",   "דֶּלֶת",    "ד", _nopil),
    ("עכבר",  "עַכבָּר",   "ע", _nopil),
    ("עכביש", "עַכָּבִש",  "ע", _nopil),
    ("סוס",   "סוּס",      "ס", _nopil),
    ("פרה",   "פָּרָה",    "פ", _nopil),
    ("צפרדע", "צְפַרדֵּע","צ", _nopil),
    ("שמלה", "שִמְלָה",   "ש", _nopil),
    ("מגפיים","מַגָּפַיִם","מ", _nopil),
    ("מתנה", "מַתָּנָה",   "מ", _nopil),
    ("פטרייה","פִטְרִיָה","פ", _nopil),
    ("עיט",   "עַיִט",     "ע", _nopil),
    ("שמיים","שָמַיִם",  "ש", _nopil),
    ("גשר",   "גֶּשֶׁר",    "ג", _nopil),
]


# ═══════════════════════════════════════════════════════════════════════════════
# Confetti animation helper
# ═══════════════════════════════════════════════════════════════════════════════

CONFETTI_COLORS = ["#E74C3C","#F1C40F","#27AE60","#3498DB","#9B59B6",
                   "#E67E22","#E91E63","#1ABC9C","#2ECC71"]

def _start_confetti(root, canvas, redraw_fn=None):
    """
    Animate confetti particles on `canvas` for ~1.2 s.
    `redraw_fn` is called afterward to restore the original image.
    """
    cw = canvas.winfo_reqwidth() or 260
    ch = canvas.winfo_reqheight() or 220
    cx, cy = cw // 2, ch // 2

    particles = []
    for _ in range(22):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 9)
        particles.append({
            'x': cx, 'y': cy,
            'vx': speed * math.cos(angle),
            'vy': speed * math.sin(angle) - 2.5,
            'color': random.choice(CONFETTI_COLORS),
            'size': random.randint(5, 12),
            'shape': random.choice(['oval', 'rect']),
            'life': 1.0,
        })

    def _tick():
        canvas.delete("confetti")
        alive = []
        for p in particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.35     # gravity
            p['vx'] *= 0.97    # air resistance
            p['life'] -= 0.028
            if p['life'] > 0:
                s = max(2, p['size'] * p['life'])
                if p['shape'] == 'oval':
                    canvas.create_oval(p['x']-s, p['y']-s,
                                       p['x']+s, p['y']+s,
                                       fill=p['color'], outline="",
                                       tags="confetti")
                else:
                    canvas.create_rectangle(p['x']-s, p['y']-s,
                                            p['x']+s, p['y']+s,
                                            fill=p['color'], outline="",
                                            tags="confetti")
                alive.append(p)
        particles[:] = alive
        if alive:
            root.after(28, _tick)
        else:
            canvas.delete("confetti")
            if redraw_fn:
                redraw_fn()

    _tick()


def _flash_border(canvas, bad_color="#E74C3C", good_color="#AED6F1", delay=550):
    """Briefly flash the image canvas border red."""
    canvas.config(highlightbackground=bad_color, highlightthickness=4)
    canvas.after(delay, lambda: canvas.config(
        highlightbackground=good_color, highlightthickness=2))


# ═══════════════════════════════════════════════════════════════════════════════
# Writing menu
# ═══════════════════════════════════════════════════════════════════════════════

class WritingMenu:
    def __init__(self, root, back_cb):
        self.root = root
        self.back_cb = back_cb
        self.root.geometry("860x580")
        self._build()

    def _build(self):
        self.frame = tk.Frame(self.root, bg=BG)
        self.frame.pack(expand=True, fill="both")

        tk.Label(self.frame, text="✏️  מִשְׂחַק כְּתִיבָה ✏️",
                 font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=(55, 10))
        tk.Label(self.frame, text="בְּחַר אֵיזֶה מִשְׂחָק תִּרְצֶה לִשְׂחָק:",
                 font=FONT_HEB, bg=BG, fg="#7F8C8D").pack(pady=(0, 35))

        btn_cfg = dict(font=(FONT_HEB[0], 20, "bold"), fg=DARK,
                       padx=30, pady=22, relief="raised", bd=4,
                       cursor="hand2", width=28)

        tk.Button(self.frame, text="🔤  מַה הָאוֹת הָרִאשׁוֹנָה?",
                  bg="#AED6F1", command=self._mode_a, **btn_cfg).pack(pady=10)
        tk.Button(self.frame, text="📝  כְּתֹב אֶת הַמִּלָּה",
                  bg="#A9DFBF", command=self._mode_b, **btn_cfg).pack(pady=10)
        tk.Button(self.frame, text="← חֲזֹר לַתַּפְרִיט הָרָאשִׁי",
                  font=FONT_SMALL, bg="#ECF0F1", fg=DARK,
                  relief="flat", cursor="hand2",
                  command=self._back).pack(pady=(30, 0))

    def _clear(self):   self.frame.destroy()
    def _back(self):    self._clear(); self.back_cb()
    def _rebuild(self): self._build()
    def _mode_a(self):  self._clear(); ModeA(self.root, back_cb=self._rebuild)
    def _mode_b(self):  self._clear(); ModeB(self.root, back_cb=self._rebuild)


# ═══════════════════════════════════════════════════════════════════════════════
# Mode A – First Letter
# ═══════════════════════════════════════════════════════════════════════════════

class ModeA:
    MAX_GUESSES = 3

    def __init__(self, root, back_cb):
        self.root = root
        self.back_cb = back_cb
        self.root.geometry("860x740")
        self.word_pool = WORDS.copy()
        random.shuffle(self.word_pool)
        self.pool_idx = 0
        self._build()
        self._next_word()

    def _build(self):
        self._outer, self.frame = make_scrollable(self.root)

        top = tk.Frame(self.frame, bg=BG)
        top.pack(fill="x", padx=15, pady=(12, 0))
        tk.Button(top, text="← חֲזֹר", font=FONT_SMALL, bg="#ECF0F1",
                  fg=DARK, relief="flat", cursor="hand2",
                  command=self._back).pack(side="left")

        tk.Label(self.frame, text="🔤 מַה הָאוֹת הָרִאשׁוֹנָה?",
                 font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=(8, 3))
        tk.Label(self.frame,
                 text="הִסְתַּכְּלוּ עַל הַתְּמוּנָה — כִּתְבוּ אֶת הָאוֹת הָרִאשׁוֹנָה!",
                 font=FONT_SMALL, bg=BG, fg="#7F8C8D").pack(pady=(0, 4))

        self.hearts_lbl = tk.Label(self.frame, text="", font=FONT_SMALL, bg=BG, fg=DARK)
        self.hearts_lbl.pack()

        img_frame = tk.Frame(self.frame, bg=BG)
        img_frame.pack(pady=10)
        self.img_canvas = tk.Canvas(img_frame, width=260, height=220,
                                    bg="#FDFEFE", highlightthickness=2,
                                    highlightbackground="#AED6F1")
        self.img_canvas.pack()

        ans_frame = tk.Frame(self.frame, bg=BG)
        ans_frame.pack(pady=15)
        tk.Label(ans_frame, text="הָאוֹת הָרִאשׁוֹנָה:", font=FONT_HEB,
                 bg=BG, fg=DARK).pack(side="right", padx=8)
        self.entry = tk.Entry(ans_frame, font=("Arial", 36, "bold"),
                              width=3, justify="center", bd=3, relief="groove",
                              bg="white", fg=DARK, insertbackground=DARK)
        self.entry.pack(side="right", padx=8)
        self.entry.bind("<Return>", lambda e: self._check())

        bf = tk.Frame(self.frame, bg=BG)
        bf.pack(pady=8)
        self.check_btn = tk.Button(bf, text="✅ בדוק!", font=FONT_HEB, bg="#A9DFBF", fg=DARK,
                   padx=20, pady=10, relief="raised", bd=3, cursor="hand2",
                   command=self._check)
        self.check_btn.pack(side="left", padx=6)
        tk.Button(bf, text="🔊 הַשְׁמַע אֶת הַמִּלָּה", font=FONT_HEB,
                  bg="#D7BDE2", fg=DARK, padx=16, pady=10, relief="raised",
                  bd=3, cursor="hand2", command=self._read_aloud).pack(side="left", padx=6)

        self.feedback = tk.Label(self.frame, text="", font=(FONT_HEB[0], 20, "bold"),
                                 bg=BG, fg=BTN_GREEN, wraplength=700)
        self.feedback.pack(pady=15)

    def _next_word(self):
        if self.pool_idx >= len(self.word_pool):
            self.word_pool = WORDS.copy()
            random.shuffle(self.word_pool)
            self.pool_idx = 0
        self.current = self.word_pool[self.pool_idx]
        self.pool_idx += 1
        self.guesses_left = self.MAX_GUESSES

        # Flash new image into canvas with a brief green border
        self.img_canvas.config(highlightbackground="#27AE60", highlightthickness=3)
        self.img_canvas.after(300, lambda: self.img_canvas.config(
            highlightbackground="#AED6F1", highlightthickness=2))
        self._redraw_image()

        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.feedback.config(text="")
        self.check_btn.config(state="normal")
        self._update_hearts()

    def _redraw_image(self):
        self.img_canvas.delete("all")
        png_path = os.path.join(IMAGES_DIR, f'{self.current[0]}.png')
        if _PIL_OK and os.path.exists(png_path):
            pil_img = _PILImage.open(png_path).resize((260, 220), _PILImage.LANCZOS)
            self._tk_img = _ImageTk.PhotoImage(pil_img)   # keep reference!
            self.img_canvas.create_image(0, 0, anchor='nw', image=self._tk_img)
        else:
            self.current[3](self.img_canvas)

    def _check(self):
        if self.guesses_left <= 0:
            return
        answer = self.entry.get().strip()
        if not answer:
            return
        correct = self.current[2]
        if answer == correct:
            play_sound("success")
            self.feedback.config(
                text=random.choice(PRAISES) + f"\nהַמִּלָּה הִיא: {self.current[1]}",
                fg=BTN_GREEN)
            self.guesses_left = 0
            self.entry.config(state="disabled")
            self.check_btn.config(state="disabled")
            # Confetti → then auto-advance
            _start_confetti(self.root, self.img_canvas, redraw_fn=self._redraw_image)
            self.root.after(1500, self._next_word)
        else:
            self.guesses_left -= 1
            play_sound("fail")
            shake(self.root)
            _flash_border(self.img_canvas)
            self._update_hearts()
            self.entry.delete(0, tk.END)
            self.entry.delete(0, tk.END)
            if self.guesses_left == 0:
                self.feedback.config(
                    text=f'😔 הַתְּשׁוּבָה: "{correct}"  ·  הַמִּלָּה: {self.current[1]}',
                    fg=BTN_ORANGE)
                self.entry.config(state="disabled")
                self.check_btn.config(state="disabled")
                # Auto-advance after showing the answer
                self.root.after(2000, self._next_word)
            else:
                self.feedback.config(text=random.choice(TRY_AGAIN), fg=BTN_RED)

    def _read_aloud(self):  say_hebrew(self.current[1])

    def _update_hearts(self):
        self.hearts_lbl.config(
            text=f"נִסְיוֹנוֹת: {hearts_str(self.guesses_left, self.MAX_GUESSES)}")

    def _back(self):
        self._outer.destroy()
        self.root.geometry("860x580")
        self.back_cb()


# ═══════════════════════════════════════════════════════════════════════════════
# Mode B – Write the Full Word
# ═══════════════════════════════════════════════════════════════════════════════

class ModeB:
    MAX_GUESSES = 3

    def __init__(self, root, back_cb):
        self.root = root
        self.back_cb = back_cb
        self.root.geometry("860x800")
        self.word_pool = WORDS.copy()
        random.shuffle(self.word_pool)
        self.pool_idx = 0
        self._build()
        self._next_word()

    def _build(self):
        self._outer, self.frame = make_scrollable(self.root)

        top = tk.Frame(self.frame, bg=BG)
        top.pack(fill="x", padx=15, pady=(12, 0))
        tk.Button(top, text="← חֲזֹר", font=FONT_SMALL, bg="#ECF0F1",
                  fg=DARK, relief="flat", cursor="hand2",
                  command=self._back).pack(side="left")

        tk.Label(self.frame, text="📝 כְּתֹב אֶת הַמִּלָּה",
                 font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=(8, 3))
        tk.Label(self.frame,
                 text="הִסְתַּכְּלוּ עַל הַתְּמוּנָה — כִּתְבוּ אֶת שְׁמָהּ!",
                 font=FONT_SMALL, bg=BG, fg="#7F8C8D").pack(pady=(0, 4))

        self.hearts_lbl = tk.Label(self.frame, text="", font=FONT_SMALL, bg=BG, fg=DARK)
        self.hearts_lbl.pack()

        img_frame = tk.Frame(self.frame, bg=BG)
        img_frame.pack(pady=10)
        self.img_canvas = tk.Canvas(img_frame, width=260, height=220,
                                    bg="#FDFEFE", highlightthickness=2,
                                    highlightbackground="#A9DFBF")
        self.img_canvas.pack()

        self.blanks_lbl = tk.Label(self.frame, text="", font=("Arial", 32, "bold"),
                                   bg=BG, fg=BTN_BLUE)
        self.blanks_lbl.pack(pady=8)
        self.hint_lbl = tk.Label(self.frame, text="", font=FONT_SMALL,
                                  bg=BG, fg="#95A5A6")
        self.hint_lbl.pack()

        ans_frame = tk.Frame(self.frame, bg=BG)
        ans_frame.pack(pady=15)
        tk.Label(ans_frame, text="כִּתְבוּ כָּאן:", font=FONT_HEB,
                 bg=BG, fg=DARK).pack(side="right", padx=10)
        self.entry = tk.Entry(ans_frame, font=("Arial", 30, "bold"),
                              width=12, justify="center", bd=3, relief="groove",
                              bg="white", fg=DARK, insertbackground=DARK)
        self.entry.pack(side="right", padx=8)
        self.entry.bind("<Return>", lambda e: self._check())

        bf = tk.Frame(self.frame, bg=BG)
        bf.pack(pady=8)
        self.check_btn = tk.Button(bf, text="✅ בדוק!", font=FONT_HEB, bg="#A9DFBF", fg=DARK,
                   padx=20, pady=10, relief="raised", bd=3, cursor="hand2",
                   command=self._check)
        self.check_btn.pack(side="left", padx=6)
        tk.Button(bf, text="🔊 הַשְׁמַע אֶת הַמִּלָּה", font=FONT_HEB,
                  bg="#D7BDE2", fg=DARK, padx=16, pady=10, relief="raised",
                  bd=3, cursor="hand2", command=self._read_aloud).pack(side="left", padx=6)

        self.feedback = tk.Label(self.frame, text="", font=(FONT_HEB[0], 20, "bold"),
                                 bg=BG, fg=BTN_GREEN, wraplength=700)
        self.feedback.pack(pady=15)

    def _next_word(self):
        if self.pool_idx >= len(self.word_pool):
            self.word_pool = WORDS.copy()
            random.shuffle(self.word_pool)
            self.pool_idx = 0
        self.current = self.word_pool[self.pool_idx]
        self.pool_idx += 1
        self.guesses_left = self.MAX_GUESSES

        self.img_canvas.config(highlightbackground="#27AE60", highlightthickness=3)
        self.img_canvas.after(300, lambda: self.img_canvas.config(
            highlightbackground="#A9DFBF", highlightthickness=2))
        self._redraw_image()

        word = self.current[0]
        self.blanks_lbl.config(text="  _  " * len(word))
        self.hint_lbl.config(text=f"({len(word)} אוֹתִיּוֹת)")
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.feedback.config(text="")
        self.check_btn.config(state="normal")
        self._update_hearts()

    def _redraw_image(self):
        self.img_canvas.delete("all")
        self.current[3](self.img_canvas)

    def _check(self):
        if self.guesses_left <= 0:
            return
        answer = self.entry.get().strip()
        if not answer:
            return
        correct_plain  = self.current[0]
        correct_niqqud = self.current[1]
        if answer == correct_plain:
            play_sound("success")
            self.feedback.config(text=random.choice(PRAISES), fg=BTN_GREEN)
            self.blanks_lbl.config(text=correct_niqqud)
            self.guesses_left = 0
            self.entry.config(state="disabled")
            self.check_btn.config(state="disabled")
            _start_confetti(self.root, self.img_canvas, redraw_fn=self._redraw_image)
            # Auto-advance after confetti
            self.root.after(1500, self._next_word)
        else:
            self.guesses_left -= 1
            play_sound("fail")
            shake(self.root)
            _flash_border(self.img_canvas, good_color="#A9DFBF")
            self._update_hearts()
            if self.guesses_left == 0:
                self.feedback.config(
                    text=f"😔 הַמִּלָּה הַנְּכוֹנָה הִיא: {correct_niqqud}",
                    fg=BTN_ORANGE)
                self.blanks_lbl.config(text=correct_niqqud)
                self.entry.config(state="disabled")
                self.check_btn.config(state="disabled")
                # Auto-advance after showing the answer
                self.root.after(2000, self._next_word)
            else:
                self.feedback.config(text=random.choice(TRY_AGAIN), fg=BTN_RED)

    def _read_aloud(self):  say_hebrew(self.current[1])

    def _update_hearts(self):
        self.hearts_lbl.config(
            text=f"נִסְיוֹנוֹת: {hearts_str(self.guesses_left, self.MAX_GUESSES)}")

    def _back(self):
        self._outer.destroy()
        self.root.geometry("860x580")
        self.back_cb()
