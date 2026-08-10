"""eee/magic wordmark — same box as humans&ai.
Order: size box to text → center text V+H → then sparkles on magic only.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

OUT_JPG = Path(__file__).with_name("eee-magic-logo.jpg")
OUT_PNG = Path(__file__).with_name("eee-magic-logo.png")
FONT = Path(r"C:\Windows\Fonts\cascadiamono.ttf")
SIZE = 128
PAD = 20
BORDER = 4
# room past the word for sparkles (equal left margin keeps text centered)
SIDE = 28
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
VIOLET = (139, 92, 246)
SPARK = (180, 150, 255)


def main() -> None:
    font = ImageFont.truetype(str(FONT), SIZE)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    # full string metrics (layout ignores sparkles)
    full = "eee/magic"
    fbb = probe.textbbox((0, 0), full, font=font)
    tw, th = fbb[2] - fbb[0], fbb[3] - fbb[1]

    w = tw + 2 * PAD + 2 * BORDER + 2 * SIDE
    h = th + 2 * PAD + 2 * BORDER

    img = Image.new("RGB", (w, h), BLACK)
    dr = ImageDraw.Draw(img)
    for i in range(BORDER):
        dr.rectangle([i, i, w - 1 - i, h - 1 - i], outline=VIOLET)

    # dead-center the text block (same method as humans&ai pad, but centered)
    # top-left of ink when drawn at (0,0) is (fbb[0], fbb[1])
    draw_x = (w - tw) // 2 - fbb[0]
    draw_y = (h - th) // 2 - fbb[1]

    # draw by character colors
    parts = [("eee", WHITE), ("/", GREY), ("magic", VIOLET)]
    x = draw_x
    magic_box = None
    for s, color in parts:
        bb = probe.textbbox((0, 0), s, font=font)
        if s == "magic":
            magic_box = (x + bb[0], draw_y + bb[1], x + bb[2], draw_y + bb[3])
        dr.text((x, draw_y), s, font=font, fill=color)
        x += bb[2] - bb[0]

    # sparkles after — only around magic ink; never change box or text
    if magic_box:
        random.seed(11)
        mx0, my0, mx1, my1 = magic_box
        band = 12
        spots = []
        for _ in range(11):
            spots.append(
                (
                    random.uniform(mx0, min(w - BORDER - 3, mx1 + SIDE)),
                    random.uniform(my0 - band, my1 + band),
                    random.choice((1, 1, 2, 2)),
                )
            )
        mcy = (my0 + my1) / 2
        spots += [
            (mx1 + 8, mcy - 3, 3),
            (mx1 + 14, my0 + 2, 2),
            (mx1 + 4, my1 - 2, 2),
        ]
        for sx, sy, r in spots:
            if sx < mx0 or sx > w - BORDER - 2:
                continue
            if sy < BORDER + 2 or sy > h - BORDER - 2:
                continue
            arm = 2 + r
            col = VIOLET if r >= 2 else SPARK
            dr.line([(sx - arm, sy), (sx + arm, sy)], fill=col, width=1)
            dr.line([(sx, sy - arm), (sx, sy + arm)], fill=col, width=1)
            if r >= 2:
                d = arm * 0.65
                dr.line([(sx - d, sy - d), (sx + d, sy + d)], fill=col, width=1)
                dr.line([(sx - d, sy + d), (sx + d, sy - d)], fill=col, width=1)
            dr.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=WHITE)

    img.save(OUT_JPG, quality=95)
    img.save(OUT_PNG)
    print(OUT_PNG, img.size)


if __name__ == "__main__":
    main()
