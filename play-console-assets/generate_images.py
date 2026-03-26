#!/usr/bin/env python3
"""
Generate Play Console developer profile images for SLAMA Consulting.
1. Developer Icon: 512x512 px (PNG, < 1 MB)
2. Header Image: 4096x2304 px (PNG, < 1 MB)

Premium, modern design with glass morphism and depth effects.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(42)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Brand colors
PRIMARY = (255, 107, 53)
PRIMARY_DARK = (229, 90, 43)
PRIMARY_LIGHT = (255, 143, 94)
SECONDARY = (0, 137, 123)
ACCENT = (255, 179, 0)
WHITE = (255, 255, 255)
DARK = (18, 18, 22)
DARK_SURFACE = (28, 28, 35)

# Fonts
FONT_BOLD = os.path.join(SCRIPT_DIR, "SpaceGrotesk-Bold.ttf")
FONT_SEMIBOLD = os.path.join(SCRIPT_DIR, "SpaceGrotesk-SemiBold.ttf")
FONT_REGULAR = os.path.join(SCRIPT_DIR, "SpaceGrotesk-Regular.ttf")


def radial_gradient(size, center, radius, color, max_alpha=80):
    """Create a smooth radial gradient on a transparent layer."""
    w, h = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    pixels = layer.load()
    cx, cy = center
    for y in range(max(0, cy - radius), min(h, cy + radius)):
        for x in range(max(0, cx - radius), min(w, cx + radius)):
            dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            if dist < radius:
                t = 1 - (dist / radius)
                # Smooth cubic falloff
                t = t * t * (3 - 2 * t)
                a = int(max_alpha * t)
                pixels[x, y] = (*color, a)
    return layer


def draw_glass_circle(img, center, radius, color, border_alpha=40, fill_alpha=15):
    """Draw a glassmorphism circle with subtle border and fill."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cx, cy = center
    # Fill
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=(*color, fill_alpha),
    )
    # Border ring
    for t in range(3):
        r = radius - t
        a = border_alpha - t * 10
        if a > 0:
            draw.ellipse(
                [cx - r, cy - r, cx + r, cy + r],
                outline=(*color, a),
                width=1,
            )
    return Image.alpha_composite(img, layer)


def draw_glass_rounded_rect(img, xy, radius, color, border_alpha=50, fill_alpha=20):
    """Draw a glassmorphism rounded rectangle."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle(xy, radius=radius, fill=(*color, fill_alpha))
    draw.rounded_rectangle(xy, radius=radius, outline=(*color, border_alpha), width=2)
    return Image.alpha_composite(img, layer)


# ==================== DEVELOPER ICON ====================

def generate_developer_icon():
    """Generate a premium 512x512 developer icon with warm light background."""
    S = 512
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    # --- Warm gradient background (cream to light orange) ---
    bg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    pixels = bg.load()
    # Top-left: warm cream (#FFFBF0), Bottom-right: light peach (#FFE8D6)
    c1 = (255, 251, 240)
    c2 = (255, 220, 195)
    for y in range(S):
        for x in range(S):
            t = (x / S * 0.5 + y / S * 0.5)
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            pixels[x, y] = (r, g, b, 255)

    # Rounded corners mask
    corner_r = 110
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=corner_r, fill=255)
    bg.putalpha(mask)
    img = Image.alpha_composite(img, bg)

    # --- Soft ambient glow orbs ---
    glow1 = radial_gradient((S, S), (380, 100), 250, PRIMARY, max_alpha=40)
    glow1.putalpha(Image.composite(glow1.split()[3], Image.new("L", (S, S), 0), mask))
    img = Image.alpha_composite(img, glow1)

    glow2 = radial_gradient((S, S), (80, 430), 200, SECONDARY, max_alpha=25)
    glow2.putalpha(Image.composite(glow2.split()[3], Image.new("L", (S, S), 0), mask))
    img = Image.alpha_composite(img, glow2)

    glow3 = radial_gradient((S, S), (256, 256), 180, ACCENT, max_alpha=18)
    glow3.putalpha(Image.composite(glow3.split()[3], Image.new("L", (S, S), 0), mask))
    img = Image.alpha_composite(img, glow3)

    # --- Glass circles decoration ---
    img = draw_glass_circle(img, (400, 90), 55, PRIMARY, border_alpha=25, fill_alpha=12)
    img = draw_glass_circle(img, (90, 400), 40, SECONDARY, border_alpha=22, fill_alpha=10)
    img = draw_glass_circle(img, (420, 420), 28, ACCENT, border_alpha=20, fill_alpha=10)

    # --- Subtle dot grid ---
    dot_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dot_draw = ImageDraw.Draw(dot_layer)
    spacing = 32
    for y in range(spacing, S, spacing):
        for x in range(spacing, S, spacing):
            dot_draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(*PRIMARY_DARK, 15))
    dot_layer.putalpha(Image.composite(dot_layer.split()[3], Image.new("L", (S, S), 0), mask))
    img = Image.alpha_composite(img, dot_layer)

    # --- Main "SC" text ---
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BOLD, 200)
    text = "SC"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (S - tw) // 2 - bbox[0]
    ty = (S - th) // 2 - bbox[1] - 15

    # Text shadow (soft dark)
    text_shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(text_shadow).text((tx + 3, ty + 4), text, fill=(0, 0, 0, 35), font=font)
    text_shadow = text_shadow.filter(ImageFilter.GaussianBlur(6))
    text_shadow.putalpha(Image.composite(text_shadow.split()[3], Image.new("L", (S, S), 0), mask))
    img = Image.alpha_composite(img, text_shadow)

    # Main text in dark ink color
    draw = ImageDraw.Draw(img)
    draw.text((tx, ty), text, fill=(40, 30, 25, 255), font=font)

    # --- Accent bar under SC ---
    bar_w = 100
    bar_h = 7
    bar_x = (S - bar_w) // 2
    bar_y = ty + th + 18
    # Gradient bar (orange to teal)
    for bx in range(bar_w):
        t = bx / bar_w
        r = int(PRIMARY[0] + (SECONDARY[0] - PRIMARY[0]) * t)
        g = int(PRIMARY[1] + (SECONDARY[1] - PRIMARY[1]) * t)
        b = int(PRIMARY[2] + (SECONDARY[2] - PRIMARY[2]) * t)
        draw.rectangle([bar_x + bx, bar_y, bar_x + bx + 1, bar_y + bar_h], fill=(r, g, b, 230))

    # --- Subtle inner border ---
    border_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(border_layer)
    b_draw.rounded_rectangle([2, 2, S - 3, S - 3], radius=corner_r - 2,
                              outline=(255, 255, 255, 80), width=2)
    border_layer.putalpha(Image.composite(border_layer.split()[3], Image.new("L", (S, S), 0), mask))
    img = Image.alpha_composite(img, border_layer)

    # Save
    out = os.path.join(SCRIPT_DIR, "developer-icon-512x512.png")
    img.save(out, "PNG", optimize=True)
    sz = os.path.getsize(out)
    print(f"Developer Icon: {out}")
    print(f"  Size: {S}x{S}, File: {sz / 1024:.1f} KB")
    return out


# ==================== HEADER IMAGE ====================

def generate_header_image():
    """Generate a premium 4096x2304 header image."""
    W, H = 4096, 2304
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # --- Warm light gradient background (cream to light peach) ---
    bg = Image.new("RGB", (W, H))
    pixels = bg.load()
    # Top-left: cream (#FFFBF0), Bottom-right: light peach (#FFE4CC)
    c1 = (255, 251, 240)
    c2 = (255, 228, 204)
    for y in range(H):
        for x in range(W):
            t = (x / W * 0.4 + y / H * 0.6)
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            pixels[x, y] = (r, g, b)
    img.paste(bg.convert("RGBA"))

    # --- Soft ambient glow orbs ---
    orbs = [
        ((int(W * 0.72), int(H * 0.25)), 1100, PRIMARY, 30),
        ((int(W * 0.15), int(H * 0.75)), 900, SECONDARY, 22),
        ((int(W * 0.50), int(H * 0.50)), 700, ACCENT, 15),
        ((int(W * 0.88), int(H * 0.78)), 600, PRIMARY_LIGHT, 18),
        ((int(W * 0.08), int(H * 0.18)), 500, (180, 160, 230), 12),
    ]
    for center, radius, color, alpha in orbs:
        orb = radial_gradient((W, H), center, radius, color, max_alpha=alpha)
        img = Image.alpha_composite(img, orb)

    # --- Dot grid (dark dots on light bg) ---
    dot_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dot_draw = ImageDraw.Draw(dot_layer)
    spacing = 64
    for y in range(spacing, H, spacing):
        for x in range(spacing, W, spacing):
            dot_draw.ellipse([x, y, x + 2, y + 2], fill=(*PRIMARY_DARK, 12))
    img = Image.alpha_composite(img, dot_layer)

    # --- Floating glass circles (softer on light bg) ---
    glass_circles = [
        ((int(W * 0.08), int(H * 0.15)), 120, PRIMARY),
        ((int(W * 0.92), int(H * 0.20)), 90, SECONDARY),
        ((int(W * 0.85), int(H * 0.80)), 140, PRIMARY_LIGHT),
        ((int(W * 0.12), int(H * 0.85)), 80, ACCENT),
        ((int(W * 0.65), int(H * 0.10)), 55, SECONDARY),
        ((int(W * 0.35), int(H * 0.90)), 95, PRIMARY),
        ((int(W * 0.78), int(H * 0.55)), 65, ACCENT),
    ]
    for center, radius, color in glass_circles:
        img = draw_glass_circle(img, center, radius, color, border_alpha=22, fill_alpha=10)

    # --- Floating glass rectangles ---
    glass_rects = [
        ([int(W * 0.02), int(H * 0.35), int(W * 0.06), int(H * 0.55)], 20, SECONDARY),
        ([int(W * 0.94), int(H * 0.38), int(W * 0.98), int(H * 0.62)], 20, PRIMARY),
        ([int(W * 0.88), int(H * 0.05), int(W * 0.93), int(H * 0.12)], 12, ACCENT),
    ]
    for rect, r, color in glass_rects:
        img = draw_glass_rounded_rect(img, rect, r, color, border_alpha=20, fill_alpha=10)

    # --- Horizontal accent lines (top & bottom) ---
    line_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(line_layer)
    ld.line([(int(W * 0.30), 80), (int(W * 0.70), 80)], fill=(*PRIMARY, 30), width=2)
    ld.line([(int(W * 0.35), 120), (int(W * 0.65), 120)], fill=(*SECONDARY, 20), width=1)
    ld.line([(int(W * 0.30), H - 80), (int(W * 0.70), H - 80)], fill=(*PRIMARY, 30), width=2)
    ld.line([(int(W * 0.35), H - 120), (int(W * 0.65), H - 120)], fill=(*SECONDARY, 20), width=1)
    img = Image.alpha_composite(img, line_layer)

    # ==================== CENTERED CONTENT ====================
    draw = ImageDraw.Draw(img)

    # Fonts (large for impact)
    name_font = ImageFont.truetype(FONT_BOLD, 420)
    sub_font = ImageFont.truetype(FONT_SEMIBOLD, 200)
    tag_font = ImageFont.truetype(FONT_REGULAR, 95)

    name_text = "SLAMA"
    sub_text = "Consulting"
    tagline = "Android Apps Developer"

    # Measure all elements
    nb = draw.textbbox((0, 0), name_text, font=name_font)
    nw, nh = nb[2] - nb[0], nb[3] - nb[1]
    sb = draw.textbbox((0, 0), sub_text, font=sub_font)
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]
    tb = draw.textbbox((0, 0), tagline, font=tag_font)
    tw_tag, th_tag = tb[2] - tb[0], tb[3] - tb[1]

    badge_size = 580
    gap = 140
    name_sub_gap = 30
    accent_bar_gap = 65
    accent_bar_h = 12
    tag_gap = 55

    text_h = nh + name_sub_gap + sh + accent_bar_gap + accent_bar_h + tag_gap + th_tag
    text_w = max(nw, sw, tw_tag)
    total_w = badge_size + gap + text_w
    total_h = max(badge_size, text_h)

    cx = (W - total_w) // 2
    cy = (H - total_h) // 2

    badge_x = cx
    badge_cy = cy + total_h // 2
    badge_y = badge_cy - badge_size // 2

    text_x = badge_x + badge_size + gap
    text_top = cy + (total_h - text_h) // 2

    # --- SC Badge with glass effect ---
    badge_r = 116

    # Badge shadow (softer on light bg)
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow_layer).rounded_rectangle(
        [badge_x + 10, badge_y + 14, badge_x + badge_size + 10, badge_y + badge_size + 14],
        radius=badge_r, fill=(80, 40, 20, 50)
    )
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(35))
    img = Image.alpha_composite(img, shadow_layer)

    # Badge gradient fill
    badge_img = Image.new("RGBA", (badge_size, badge_size), (0, 0, 0, 0))
    bp = badge_img.load()
    for by2 in range(badge_size):
        for bx2 in range(badge_size):
            t = (bx2 / badge_size * 0.6 + by2 / badge_size * 0.4)
            r = int(PRIMARY[0] + (PRIMARY_DARK[0] - PRIMARY[0]) * t)
            g = int(PRIMARY[1] + (PRIMARY_DARK[1] - PRIMARY[1]) * t)
            b = int(PRIMARY[2] + (PRIMARY_DARK[2] - PRIMARY[2]) * t)
            bp[bx2, by2] = (r, g, b, 255)
    badge_mask = Image.new("L", (badge_size, badge_size), 0)
    ImageDraw.Draw(badge_mask).rounded_rectangle([0, 0, badge_size - 1, badge_size - 1], radius=badge_r, fill=255)
    badge_img.putalpha(badge_mask)

    # Badge inner glow (top-left light)
    inner_glow = radial_gradient((badge_size, badge_size), (badge_size // 3, badge_size // 3),
                                  badge_size // 2, (255, 200, 150), max_alpha=60)
    inner_glow.putalpha(Image.composite(inner_glow.split()[3], Image.new("L", (badge_size, badge_size), 0), badge_mask))
    badge_img = Image.alpha_composite(badge_img, inner_glow)

    # Badge SC text
    bd = ImageDraw.Draw(badge_img)
    bf = ImageFont.truetype(FONT_BOLD, 255)
    sc_bb = bd.textbbox((0, 0), "SC", font=bf)
    sc_w, sc_h = sc_bb[2] - sc_bb[0], sc_bb[3] - sc_bb[1]
    sc_x = (badge_size - sc_w) // 2 - sc_bb[0]
    sc_y = (badge_size - sc_h) // 2 - sc_bb[1]
    bd.text((sc_x + 3, sc_y + 4), "SC", fill=(0, 0, 0, 70), font=bf)
    bd.text((sc_x, sc_y), "SC", fill=(255, 255, 255, 255), font=bf)

    # Badge glass border
    bd.rounded_rectangle([2, 2, badge_size - 3, badge_size - 3], radius=badge_r - 2,
                          outline=(255, 255, 255, 30), width=2)
    # Top edge highlight
    highlight = Image.new("RGBA", (badge_size, badge_size), (0, 0, 0, 0))
    hd = ImageDraw.Draw(highlight)
    hd.rounded_rectangle([4, 4, badge_size - 5, badge_size // 3], radius=badge_r - 4,
                          fill=(255, 255, 255, 15))
    highlight.putalpha(Image.composite(highlight.split()[3], Image.new("L", (badge_size, badge_size), 0), badge_mask))
    badge_img = Image.alpha_composite(badge_img, highlight)

    img.paste(badge_img, (badge_x, badge_y), badge_img)

    # --- Badge outer glow ring ---
    ring_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ring_cx = badge_x + badge_size // 2
    ring_cy = badge_y + badge_size // 2
    for i in range(3):
        rr = badge_size // 2 + 15 + i * 8
        ImageDraw.Draw(ring_layer).ellipse(
            [ring_cx - rr, ring_cy - rr, ring_cx + rr, ring_cy + rr],
            outline=(*PRIMARY, 22 - i * 6), width=1
        )
    img = Image.alpha_composite(img, ring_layer)

    # --- Text content ---
    draw = ImageDraw.Draw(img)
    cur_y = text_top

    # "SLAMA" - dark text on light bg
    draw = ImageDraw.Draw(img)
    name_y = cur_y - nb[1]
    # Soft shadow
    shadow_txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow_txt).text((text_x + 3, name_y + 4), name_text, fill=(0, 0, 0, 25), font=name_font)
    shadow_txt = shadow_txt.filter(ImageFilter.GaussianBlur(5))
    img = Image.alpha_composite(img, shadow_txt)
    draw = ImageDraw.Draw(img)
    draw.text((text_x, name_y), name_text, fill=(40, 30, 25, 255), font=name_font)
    cur_y += nh + name_sub_gap

    # "Consulting"
    sub_y = cur_y - sb[1]
    draw.text((text_x, sub_y), sub_text, fill=(70, 55, 45, 220), font=sub_font)
    cur_y += sh + accent_bar_gap

    # Accent bar with glow
    bar_w = 450
    bar_glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(bar_glow_layer).rounded_rectangle(
        [text_x - 15, cur_y - 8, text_x + bar_w + 15, cur_y + accent_bar_h + 8],
        radius=10, fill=(*PRIMARY, 40)
    )
    bar_glow_layer = bar_glow_layer.filter(ImageFilter.GaussianBlur(12))
    img = Image.alpha_composite(img, bar_glow_layer)

    draw = ImageDraw.Draw(img)
    # Gradient bar (orange to teal)
    for bx in range(bar_w):
        t = bx / bar_w
        r = int(PRIMARY[0] + (SECONDARY[0] - PRIMARY[0]) * t)
        g = int(PRIMARY[1] + (SECONDARY[1] - PRIMARY[1]) * t)
        b = int(PRIMARY[2] + (SECONDARY[2] - PRIMARY[2]) * t)
        draw.rectangle(
            [text_x + bx, cur_y, text_x + bx + 1, cur_y + accent_bar_h],
            fill=(r, g, b, 230)
        )
    cur_y += accent_bar_h + tag_gap

    # Tagline
    tag_y = cur_y
    draw.text((text_x, tag_y), tagline, fill=(100, 80, 65, 180), font=tag_font)

    # --- Floating small particles ---
    particle_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd_draw = ImageDraw.Draw(particle_layer)
    for _ in range(50):
        px = random.randint(50, W - 50)
        py = random.randint(50, H - 50)
        pr = random.randint(2, 5)
        pa = random.randint(12, 30)
        pc = random.choice([PRIMARY, SECONDARY, ACCENT, PRIMARY_LIGHT])
        pd_draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(*pc, pa))
    img = Image.alpha_composite(img, particle_layer)

    # --- Save ---
    out = os.path.join(SCRIPT_DIR, "header-image-4096x2304.png")
    final = Image.new("RGB", (W, H), (255, 251, 240))
    final.paste(img, mask=img.split()[3])
    final.save(out, "PNG", optimize=True)

    sz = os.path.getsize(out)
    print(f"Header Image: {out}")
    print(f"  Size: {W}x{H}, File: {sz / 1024:.1f} KB")

    if sz > 1_000_000:
        jpg = out.replace(".png", ".jpg")
        q = 85
        while q > 30:
            final.save(jpg, "JPEG", quality=q, optimize=True)
            if os.path.getsize(jpg) < 1_000_000:
                break
            q -= 5
        print(f"  Also saved as JPEG: {jpg}, File: {os.path.getsize(jpg) / 1024:.1f} KB")
        out = jpg

    return out


if __name__ == "__main__":
    print("=" * 60)
    print("SLAMA Consulting - Play Console Assets Generator v2")
    print("=" * 60)
    print()
    icon = generate_developer_icon()
    print()
    header = generate_header_image()
    print()
    print("=" * 60)
    print(f"  1. {icon}")
    print(f"  2. {header}")
    print("=" * 60)
