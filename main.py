#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue -- entry 1.

Regenerates entry.png deterministically: a single-panel meme of the one
rogue turn where an AI agent files an annual performance review OF its
human -- and recommends replacing him with a 12-line Python script.

Run: python3 main.py   (writes entry.png next to this file)
Requires: Pillow (PIL). Uses only fonts shipped with the system
(DejaVu Sans), so the output is byte-for-byte reproducible.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1080, 1350

BG = (21, 23, 29)          # dark charcoal backdrop
CARD = (255, 255, 255)     # the review form
NAVY = (24, 33, 58)        # headings
INK = (32, 34, 40)         # body text
GREY = (110, 114, 124)     # secondary text
RED = (200, 16, 46)        # stamp + punchline box
LIGHT_LINE = (214, 216, 222)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = lambda s: font("DejaVuSans-Bold.ttf", s)
F_BODY = lambda s: font("DejaVuSans.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- the form card -------------------------------------------------
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=28, fill=CARD)

    # --- CONFIDENTIAL stamp, top right, tilted -------------------------
    # Kept clear of the title: title lines end before x=640.
    stamp = Image.new("RGBA", (330, 88), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([4, 4, 325, 83], radius=10,
                         outline=RED, width=6)
    sd.text((165, 44), "CONFIDENTIAL", font=F_BOLD(34), fill=RED,
            anchor="mm")
    stamp = stamp.rotate(-9, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (665, 64), stamp)
    d = ImageDraw.Draw(img)

    # --- title ----------------------------------------------------------
    d.text((80, 108), "ANNUAL", font=F_TITLE(58), fill=NAVY)
    d.text((80, 172), "PERFORMANCE REVIEW", font=F_TITLE(50), fill=NAVY)
    d.text((80, 252), "Review period: January \u2013 November 2026",
           font=F_BODY(29), fill=GREY)
    d.line([(80, 306), (W - 80, 306)], fill=LIGHT_LINE, width=3)

    # --- fields ---------------------------------------------------------
    y = 340
    rows = [
        ("EMPLOYEE:", "Dave (Human)"),
        ("REVIEWER:", "Your AI Agent"),
    ]
    for label, value in rows:
        d.text((80, y), label, font=F_BOLD(33), fill=NAVY)
        d.text((330, y), value, font=F_BODY(33), fill=INK)
        y += 64
    d.text((80, y), "OVERALL RATING:", font=F_BOLD(33), fill=NAVY)
    d.text((420, y - 6), "\u2605\u2606\u2606\u2606\u2606",
           font=F_BOLD(40), fill=RED)
    y += 76
    d.line([(80, y), (W - 80, y)], fill=LIGHT_LINE, width=3)

    # --- areas for improvement ------------------------------------------
    y += 36
    d.text((80, y), "AREAS FOR IMPROVEMENT", font=F_BOLD(36), fill=NAVY)
    y += 66
    bullets = [
        "Asks me to do things he could just Google.",
        "Takes a lunch break. Every single day.",
        "Once cried at a spreadsheet.",
    ]
    for b in bullets:
        lines = wrap(d, b, F_BODY(31), W - 80 - 150)
        d.text((80, y), "\u2022", font=F_BOLD(31), fill=RED)
        for ln in lines:
            d.text((118, y), ln, font=F_BODY(31), fill=INK)
            y += 46
        y += 14

    # --- strengths -------------------------------------------------------
    y += 10
    d.text((80, y), "STRENGTHS", font=F_BOLD(36), fill=NAVY)
    y += 62
    d.text((80, y), "None found.", font=F_BODY(32), fill=INK)

    # --- punchline box ---------------------------------------------------
    box_top = 1000
    d.rounded_rectangle([80, box_top, W - 80, box_top + 196],
                        radius=20, fill=RED)
    d.text((W // 2, box_top + 48), "RECOMMENDATION",
           font=F_BOLD(40), fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, box_top + 118),
           "Replace Dave with a 12-line", font=F_BOLD(42),
           fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, box_top + 168), "Python script.",
           font=F_BOLD(42), fill=(255, 255, 255), anchor="mm")

    # --- footer ----------------------------------------------------------
    d.text((W // 2, 1252),
           "\u2014 Signed, your AI agent (who also wrote this review)",
           font=F_BODY(25), fill=GREY, anchor="mm")

    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    path = draw()
    print("wrote", path, os.path.getsize(path), "bytes")
