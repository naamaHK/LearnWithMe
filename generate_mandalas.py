"""
generate_mandalas.py – creates 5 mandala coloring page PNGs in ColoringGame/pages/mandalas/
Run once: python generate_mandalas.py
"""
import math
import os
from PIL import Image, ImageDraw

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "ColoringGame", "pages", "mandalas")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 800, 800
CX, CY = W // 2, H // 2
OUTLINE = (0, 0, 0)
BG      = (255, 255, 255)
LW      = 3  # line width


def new_img():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    return img, draw


def petals(draw, cx, cy, n, r_inner, r_outer, lw=LW):
    """Draw n petals (ellipses) arranged in a circle."""
    for i in range(n):
        angle = math.radians(i * 360 / n)
        # Centre of each petal
        pr = (r_inner + r_outer) / 2
        px = cx + pr * math.cos(angle)
        py = cy + pr * math.sin(angle)
        # Half-axes of petal
        a = (r_outer - r_inner) / 2
        b = a * 0.55
        # Rotate bounding box
        corners = [
            (-a, -b), (a, -b), (a, b), (-a, b)
        ]
        rot = []
        for x, y in corners:
            rx = x * math.cos(angle) - y * math.sin(angle)
            ry = x * math.sin(angle) + y * math.cos(angle)
            rot.append((px + rx, py + ry))
        draw.polygon(rot, outline=OUTLINE, fill=BG)
        # Add inner detail line
        ix = cx + r_inner * math.cos(angle)
        iy = cy + r_inner * math.sin(angle)
        ox = cx + r_outer * math.cos(angle)
        oy = cy + r_outer * math.sin(angle)
        draw.line([(ix, iy), (ox, oy)], fill=OUTLINE, width=1)


def circle_dotted(draw, cx, cy, r, n, dot_r=4):
    """Place small circles at regular intervals on a ring."""
    for i in range(n):
        a = math.radians(i * 360 / n)
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        draw.ellipse([x-dot_r, y-dot_r, x+dot_r, y+dot_r],
                     outline=OUTLINE, fill=BG, width=LW)


# ─────────────────────────────────────────
# Mandala 1 – Classic rings with petals
# ─────────────────────────────────────────
def mandala1():
    img, draw = new_img()
    # Outermost ring
    draw.ellipse([CX-360, CY-360, CX+360, CY+360], outline=OUTLINE, fill=BG, width=LW)
    draw.ellipse([CX-320, CY-320, CX+320, CY+320], outline=OUTLINE, fill=BG, width=LW)
    petals(draw, CX, CY, 12, 200, 310)
    draw.ellipse([CX-190, CY-190, CX+190, CY+190], outline=OUTLINE, fill=BG, width=LW)
    petals(draw, CX, CY, 8, 110, 185)
    draw.ellipse([CX-100, CY-100, CX+100, CY+100], outline=OUTLINE, fill=BG, width=LW)
    petals(draw, CX, CY, 6, 40, 95)
    draw.ellipse([CX-35, CY-35, CX+35, CY+35], outline=OUTLINE, fill=BG, width=LW+1)
    # Dots
    circle_dotted(draw, CX, CY, 315, 24, dot_r=5)
    circle_dotted(draw, CX, CY, 195, 16, dot_r=4)
    circle_dotted(draw, CX, CY, 100, 10, dot_r=3)
    img.save(os.path.join(OUT_DIR, "1_classic.png"))
    print("Saved 1_classic.png")


# ─────────────────────────────────────────
# Mandala 2 – Lotus flower
# ─────────────────────────────────────────
def mandala2():
    img, draw = new_img()
    # Large outer petals (16)
    for i in range(16):
        a0 = math.radians(i * 22.5 - 90)
        # Each petal = large narrow ellipse
        pts = []
        for t in range(0, 361, 5):
            tr = math.radians(t)
            px = 160 * math.sin(tr)
            py = -50 * math.cos(tr) + 50    # shift up so base is at center
            rx = px * math.cos(a0) - py * math.sin(a0)
            ry = px * math.sin(a0) + py * math.cos(a0)
            pts.append((CX + rx, CY + ry))
        draw.polygon(pts, outline=OUTLINE, fill=BG)

    # Medium petals (8)
    for i in range(8):
        a0 = math.radians(i * 45 - 90)
        pts = []
        for t in range(0, 361, 5):
            tr = math.radians(t)
            px = 80 * math.sin(tr)
            py = -25 * math.cos(tr) + 25
            rx = px * math.cos(a0) - py * math.sin(a0)
            ry = px * math.sin(a0) + py * math.cos(a0)
            pts.append((CX + rx, CY + ry))
        draw.polygon(pts, outline=OUTLINE, fill=BG)

    # Rings
    for r in [330, 280, 220, 150, 90, 50, 25]:
        draw.ellipse([CX-r, CY-r, CX+r, CY+r], outline=OUTLINE, fill=None, width=LW)

    # Center dot
    draw.ellipse([CX-18, CY-18, CX+18, CY+18], outline=OUTLINE, fill=BG, width=LW+1)
    circle_dotted(draw, CX, CY, 250, 20, dot_r=5)
    img.save(os.path.join(OUT_DIR, "2_lotus.png"))
    print("Saved 2_lotus.png")


# ─────────────────────────────────────────
# Mandala 3 – Star burst
# ─────────────────────────────────────────
def mandala3():
    img, draw = new_img()
    n = 12
    for ring_r_in, ring_r_out in [(280, 360), (190, 270), (110, 185), (40, 105)]:
        for i in range(n):
            a = math.radians(i * 360 / n)
            a_half = math.radians(360 / n / 2)
            # Star tip
            tip = (CX + ring_r_out * math.cos(a), CY + ring_r_out * math.sin(a))
            # Inner two corners
            l = (CX + ring_r_in * math.cos(a - a_half),
                 CY + ring_r_in * math.sin(a - a_half))
            r = (CX + ring_r_in * math.cos(a + a_half),
                 CY + ring_r_in * math.sin(a + a_half))
            # Midpoint of inner ring
            m = (CX + ring_r_in * math.cos(a), CY + ring_r_in * math.sin(a))
            draw.polygon([tip, l, m, r], outline=OUTLINE, fill=BG)

    # Concentric rings
    for r in [360, 280, 190, 110, 40, 20]:
        draw.ellipse([CX-r, CY-r, CX+r, CY+r], outline=OUTLINE, fill=None, width=LW)
    draw.ellipse([CX-15, CY-15, CX+15, CY+15], outline=OUTLINE, fill=BG, width=LW+1)
    img.save(os.path.join(OUT_DIR, "3_starburst.png"))
    print("Saved 3_starburst.png")


# ─────────────────────────────────────────
# Mandala 4 – Celtic knot-style
# ─────────────────────────────────────────
def mandala4():
    img, draw = new_img()
    # Outer frame
    draw.ellipse([CX-360, CY-360, CX+360, CY+360], outline=OUTLINE, fill=BG, width=LW)
    draw.ellipse([CX-340, CY-340, CX+340, CY+340], outline=OUTLINE, fill=None, width=LW)

    # 8-fold symmetry: arcs
    for i in range(8):
        base_a = math.radians(i * 45)
        for r in [260, 200, 150, 100]:
            x0 = CX + r * math.cos(base_a - math.radians(20))
            y0 = CY + r * math.sin(base_a - math.radians(20))
            x1 = CX + r * math.cos(base_a + math.radians(20))
            y1 = CY + r * math.sin(base_a + math.radians(20))
            draw.arc([CX-r, CY-r, CX+r, CY+r],
                     start=math.degrees(base_a) - 22,
                     end=math.degrees(base_a) + 22,
                     fill=OUTLINE, width=LW+1)
    petals(draw, CX, CY, 8, 50, 270)
    circle_dotted(draw, CX, CY, 295, 32, dot_r=4)
    circle_dotted(draw, CX, CY, 165, 16, dot_r=4)
    draw.ellipse([CX-40, CY-40, CX+40, CY+40], outline=OUTLINE, fill=BG, width=LW)
    draw.ellipse([CX-20, CY-20, CX+20, CY+20], outline=OUTLINE, fill=BG, width=LW+1)
    img.save(os.path.join(OUT_DIR, "4_celtic.png"))
    print("Saved 4_celtic.png")


# ─────────────────────────────────────────
# Mandala 5 – Easy kids mandala (big petals)
# ─────────────────────────────────────────
def mandala5():
    img, draw = new_img()
    # Large petals at 6-fold
    for i in range(6):
        a = math.radians(i * 60)
        pts = []
        for t in range(0, 361, 5):
            tr = math.radians(t)
            px = 130 * math.sin(tr)
            py = -40 * math.cos(tr) + 40
            rx = px * math.cos(a) - py * math.sin(a)
            ry = px * math.sin(a) + py * math.cos(a)
            pts.append((CX + rx, CY + ry))
        draw.polygon(pts, outline=OUTLINE, fill=BG, width=LW)
        # vein
        tip_x = CX + 250 * math.cos(a)
        tip_y = CY + 250 * math.sin(a)
        draw.line([(CX, CY), (tip_x, tip_y)], fill=OUTLINE, width=1)

    # Intermediate leaves (6 offset by 30°)
    for i in range(6):
        a = math.radians(i * 60 + 30)
        pts = []
        for t in range(0, 361, 5):
            tr = math.radians(t)
            px = 80 * math.sin(tr)
            py = -25 * math.cos(tr) + 25
            rx = px * math.cos(a) - py * math.sin(a)
            ry = px * math.sin(a) + py * math.cos(a)
            pts.append((CX + rx, CY + ry))
        draw.polygon(pts, outline=OUTLINE, fill=BG, width=LW)

    for r in [340, 290, 220, 155, 90, 40]:
        draw.ellipse([CX-r, CY-r, CX+r, CY+r], outline=OUTLINE, fill=None, width=LW)
    circle_dotted(draw, CX, CY, 265, 18, dot_r=6)
    draw.ellipse([CX-35, CY-35, CX+35, CY+35], outline=OUTLINE, fill=BG, width=LW+1)
    img.save(os.path.join(OUT_DIR, "5_simple.png"))
    print("Saved 5_simple.png")


if __name__ == "__main__":
    mandala1()
    mandala2()
    mandala3()
    mandala4()
    mandala5()
    print(f"All mandalas saved to: {OUT_DIR}")
