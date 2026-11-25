#!/usr/bin/env python3
"""Draw the front page for news-image-20261125 (variant A: classic broadsheet).

Canvas 1024x1024. Everything is drawn programmatically with PIL: masthead,
date, 3 headline stories with drawn illustrations, and 37 further story
blocks across 7 regions -- 40 sourced stories in total. No photos, no
network, no downloaded images.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
NAVY = (26, 42, 74)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
LIGHT_BLUE = (178, 205, 225)
SEA = (46, 90, 130)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap using real text widths."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_panel_ship(d, x, y, w, h):
    """Gulf of Finland: sea, warship, drone, explosion."""
    d.rectangle([x, y, x + w, y + h], fill=LIGHT_BLUE)
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    # waves
    for i in range(5):
        wx = x + 12 + i * 62
        d.arc([wx, y + h * 0.70, wx + 44, y + h * 0.86], 0, 180, fill=(255, 255, 255), width=2)
    # ship hull + superstructure
    d.polygon([(x + 60, y + h * 0.62), (x + 250, y + h * 0.62),
               (x + 235, y + h * 0.82), (x + 80, y + h * 0.82)], fill=(60, 60, 66))
    d.rectangle([x + 130, y + h * 0.38, x + 195, y + h * 0.62], fill=(90, 90, 96))
    d.rectangle([x + 158, y + h * 0.16, x + 166, y + h * 0.38], fill=(60, 60, 66))
    d.rectangle([x + 148, y + h * 0.22, x + 176, y + h * 0.30], fill=(60, 60, 66))
    # explosion star over the bow
    import math
    cx, cy = x + 245, y + h * 0.30
    for r, col in ((34, (255, 190, 40)), (22, (255, 120, 20)), (12, (255, 240, 120))):
        pts = []
        for k in range(12):
            ang = -math.pi / 2 + k * math.pi / 6
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    # drone quadcopter top-left
    dx, dy = x + 42, y + 22
    d.rectangle([dx, dy, dx + 26, dy + 12], fill=(30, 30, 30))
    d.ellipse([dx - 8, dy - 6, dx + 4, dy + 2], outline=(30, 30, 30), width=2)
    d.ellipse([dx + 22, dy - 6, dx + 34, dy + 2], outline=(30, 30, 30), width=2)
    d.ellipse([dx - 8, dy + 10, dx + 4, dy + 18], outline=(30, 30, 30), width=2)
    d.ellipse([dx + 22, dy + 10, dx + 34, dy + 18], outline=(30, 30, 30), width=2)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def draw_panel_tower(d, x, y, w, h):
    """Riyadh skyline: tallest tower, drone, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 180))
    d.ellipse([x + w - 52, y + 10, x + w - 14, y + 48], fill=(255, 214, 120))
    # skyline blocks
    for bx, bw, bh in ((0, 52, 46), (56, 44, 62), (240, 48, 54), (292, 20, 40)):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(120, 110, 96))
    # tallest tower, centre
    d.polygon([(x + 128, y + h), (x + 128, y + 18), (x + 156, y + 4),
               (x + 184, y + 18), (x + 184, y + h)], fill=(70, 78, 92))
    for wy in range(26, 82, 12):
        for wx in (136, 150, 164):
            d.rectangle([x + wx, y + wy, x + wx + 8, y + wy + 6], fill=(255, 220, 120))
    # smoke puffs from tower top
    for sx, sy, sr in ((150, 8, 10), (168, -2, 12), (186, 8, 9)):
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr], fill=(150, 150, 150))
    # drone
    dx, dy = x + 232, y + 20
    d.rectangle([dx, dy, dx + 26, dy + 12], fill=(30, 30, 30))
    d.ellipse([dx - 8, dy - 6, dx + 4, dy + 2], outline=(30, 30, 30), width=2)
    d.ellipse([dx + 22, dy - 6, dx + 34, dy + 2], outline=(30, 30, 30), width=2)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def draw_panel_medal(d, x, y, w, h):
    """Presidential Medal of Freedom: ribbon + gold medal on navy."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # ribbon: two straps meeting at the medal
    cx, cy = x + w // 2, y + h // 2 + 12
    d.polygon([(x + 118, y), (x + 142, y), (cx + 10, cy - 26), (cx - 10, cy - 26)],
              fill=(178, 34, 34))
    d.polygon([(x + 170, y), (x + 194, y), (cx + 10, cy - 26), (cx - 10, cy - 26)],
              fill=(255, 255, 255))
    # medal
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=GOLD, outline=(255, 220, 120), width=3)
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=(150, 110, 20), width=2)
    # star on medal
    import math
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = 18 if k % 2 == 0 else 7
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 255, 255))
    d.text((x + 12, y + h - 22), "THE PRESIDENTIAL MEDAL OF FREEDOM",
           font=font(SANS_B, 10), fill=(255, 255, 255))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


HEADLINES = [
    ("UKRAINE HITS RUSSIAN SHIP IN GULF OF FINLAND",
     "President Zelenskiy confirmed Ukrainian drones struck a Russian ship "
     "in the Gulf of Finland on Saturday. Norway urged caution as the war "
     "at sea widened to a new front.", "ship"),
    ("HOUTHI DRONE HITS RIYADH'S TALLEST TOWER",
     "A Houthi drone struck Riyadh's tallest tower, wounding 11 people, "
     "Saudi civil defence said. The attack brought Yemen's war to the "
     "Saudi capital's skyline.", "tower"),
    ("TRUMP AWARDS GIULIANI MEDAL OF FREEDOM",
     "President Trump awarded Rudy Giuliani the Presidential Medal of "
     "Freedom, the nation's highest civilian honour, at a White House "
     "ceremony on Tuesday.", "medal"),
]

# (region, title, body, sure)  sure: True = reported today, False = developing
BLOCKS = [
    # --- column 1: Ukraine & Russia (9) ---
    ("UKRAINE & RUSSIA", "● Warship sunk off Benghazi",
     "Ukraine said it sank a Russian warship off Libya's coast on Sunday.", True),
    ("UKRAINE & RUSSIA", "● Cargo vessel sunk too",
     "A Russian cargo vessel was also sunk off Benghazi in the same strike.", True),
    ("UKRAINE & RUSSIA", "● 700,000 Russians killed",
     "New analysis puts Russian soldiers killed in the war above 700,000.", True),
    ("UKRAINE & RUSSIA", "● Kyiv block hit, 11 killed",
     "A Russian drone and missile attack hit a Kyiv apartment block.", True),
    ("UKRAINE & RUSSIA", "○ NATO jets for Poland",
     "NATO plans early-warning aircraft in Poland after missiles landed there.", False),
    ("UKRAINE & RUSSIA", "● EU adds Russia sanctions",
     "The EU announced a further round of sanctions on Russia.", True),
    ("UKRAINE & RUSSIA", "○ NATO-like guarantees eyed",
     "US envoy Kushner: Trump may consider NATO-like security guarantees for Kyiv.", False),
    ("UKRAINE & RUSSIA", "● Putin: retaliation 'inevitable'",
     "Putin vowed retaliation after Ukraine hit Russian oil plants.", True),
    ("UKRAINE & RUSSIA", "● Norway urges caution",
     "Norway urged restraint after the Gulf of Finland ship strike.", True),
    # --- column 2: Middle East (6) + USA (3) ---
    ("MIDDLE EAST", "● Houthis 60 km from Aden",
     "Houthi forces pushed to within 60 km of Aden; government troops say they will not seize the city.", True),
    ("MIDDLE EAST", "● Three tankers hit in Hormuz",
     "Iran's Guard Navy said three oil tankers were hit by naval mines in Hormuz.", True),
    ("MIDDLE EAST", "● Iran faces winter gas cuts",
     "Iran braces for winter gas shortages after US and Israeli strikes damaged facilities.", True),
    ("MIDDLE EAST", "● Iran starts power rationing",
     "Electricity rationing began on 22 November as Iran's grid struggles.", True),
    ("MIDDLE EAST", "● UN warns over Gaza hardship",
     "The UN raised fresh concerns over humanitarian difficulties in Gaza.", True),
    ("MIDDLE EAST", "○ US aid to Israel in doubt",
     "A US envoy is 'not certain' military aid to Israel will end this year as Trump promised.", False),
    ("UNITED STATES", "● Turkeys spared: Freedom & Feathers",
     "Trump spared the Thanksgiving turkeys 'Freedom' and 'Feathers' at the White House.", True),
    ("UNITED STATES", "● CIA and ODNI breached",
     "The CIA and ODNI suffered a cyber breach involving some unclassified data.", True),
    ("UNITED STATES", "● Huawei guilty of trade-secret theft",
     "A US jury found Huawei guilty of stealing trade secrets and hiding its Iran business.", True),
    # --- column 3: USA (4) + Europe (4) + Asia (2) ---
    ("UNITED STATES", "● Fort Hood shooter seeks stay",
     "Nidal Hasan seeks a stay of execution set for next week.", True),
    ("UNITED STATES", "● Nvidia shares fall ~7%",
     "Nvidia shares fell about 7%; chief Huang said he violated the code of conduct.", True),
    ("UNITED STATES", "● Dell lifts forecasts on AI",
     "Dell raised forecasts after a record quarter driven by AI server demand.", True),
    ("UNITED STATES", "● Army to detonate lead azide",
     "The US Army plans to detonate lead azide in Iowa; residents were urged to evacuate.", True),
    ("EUROPE", "● Sarkozy corruption case to trial",
     "French officials ordered ex-President Sarkozy's case to trial; hearing 1 Apr 2027.", True),
    ("EUROPE", "○ Sweden to vote on PM Kristersson",
     "Parliament votes on whether Moderates leader Kristersson stays PM.", False),
    ("EUROPE", "○ UK consults on age of consent",
     "UK ministers opened a public consultation on changing the age of consent.", False),
    ("EUROPE", "● Burnham: nuclear veterans panel",
     "PM Burnham confirmed an independent panel on nuclear test veterans' health legacy.", True),
    ("ASIA", "● BJP and Akali Dal reunite",
     "BJP and Akali Dal announced a Punjab 2027 alliance, ending a six-year split.", True),
    ("ASIA", "● Nepal PM's first India visit",
     "Nepal PM Balendra Shah made his first state visit to India, 22-23 Nov, meeting PM Modi.", True),
    # --- column 4: Asia (4) + Science (1) + Sport & Markets (4) ---
    ("ASIA", "● Gukesh holds Sindarov",
     "World chess champion Gukesh weathered time pressure to hold Sindarov.", True),
    ("ASIA", "● GTA 6 out worldwide",
     "GTA 6 was released worldwide on 19 November for PS5 and Xbox.", True),
    ("ASIA", "● Sooryavanshi, 204 off 53 balls",
     "The 15-year-old hit the fastest List A double hundred.", True),
    ("ASIA", "● England beat Australia by 8 wickets",
     "England won the 2nd T20I chasing 185 against Australia.", True),
    ("SCIENCE & SPACE", "● 'Star system that should not exist'",
     "Astronomers found a cosmic mystery star system just 28 light-years away.", True),
    ("SPORT & MARKETS", "● Stokes registers for IPL auction",
     "Ben Stokes registered for the IPL 2027 auction.", True),
    ("SPORT & MARKETS", "● Man Utd fury over Yoro red card",
     "Manchester United and manager Pochettino were furious over the handling of Leny Yoro's red card.", True),
    ("SPORT & MARKETS", "● Venezuela debt: $237.5 billion",
     "Venezuela officially reported total public debt of $237.5 billion.", True),
    ("SPORT & MARKETS", "● HBO Max half off for Black Friday",
     "HBO Max offered half off a year in its Black Friday deal.", True),
]

COLUMNS = [
    BLOCKS[0:9],
    BLOCKS[9:18],
    BLOCKS[18:28],
    BLOCKS[28:37],
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 8], fill=NAVY)
    mast = font(SERIF_B, 62)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 16), title, font=mast, fill=INK)
    d.line([24, 92, W - 24, 92], fill=INK, width=3)
    d.line([24, 96, W - 24, 96], fill=INK, width=1)
    date_f = font(SANS_B, 22)
    date_s = "WEDNESDAY 25 NOVEMBER 2026"
    dw = d.textlength(date_s, font=date_f)
    d.text(((W - dw) / 2, 102), date_s, font=date_f, fill=RED)
    sub_f = font(SANS, 14)
    sub = "40 sourced stories  ·  7 regions  ·  from Kyiv to Riyadh to Washington"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 132), sub, font=sub_f, fill=INK)
    # corner notes
    small = font(SANS, 11)
    d.text((24, 104), "No. 329", font=small, fill=INK)
    d.text((W - 24 - d.textlength("One day. One page.", font=small), 104),
           "One day. One page.", font=small, fill=INK)
    d.line([24, 158, W - 24, 158], fill=INK, width=2)

    # ---------- 3 headlines ----------
    col_w, gap = 312, 20
    y0 = 168
    panel_h = 96
    for i, (head, body, kind) in enumerate(HEADLINES):
        x = 24 + i * (col_w + gap)
        if kind == "ship":
            draw_panel_ship(d, x, y0, col_w, panel_h)
        elif kind == "tower":
            draw_panel_tower(d, x, y0, col_w, panel_h)
        else:
            draw_panel_medal(d, x, y0, col_w, panel_h)
        hf = font(SERIF_B, 17)
        y = y0 + panel_h + 8
        for line in wrap(d, head, hf, col_w):
            d.text((x, y), line, font=hf, fill=INK)
            y += 21
        bf = font(SANS, 11)
        y += 2
        for line in wrap(d, body, bf, col_w):
            d.text((x, y), line, font=bf, fill=(40, 40, 40))
            y += 14
        d.line([x, y0 + 196, x + col_w, y0 + 196], fill=(150, 150, 150), width=1)
    d.line([24, 372, W - 24, 372], fill=INK, width=2)

    # ---------- story grid ----------
    grid_top, grid_bottom = 382, 976
    col_xs = [24, 272, 520, 768]
    col_w2 = 232
    title_f = font(SANS_B, 11)
    body_f = font(SANS, 9)
    region_f = font(SANS_B, 12)
    for ci, col in enumerate(COLUMNS):
        x = col_xs[ci]
        # slot height: headers share the column's vertical budget
        n_headers = len({b[0] for b in col})
        avail = grid_bottom - grid_top - n_headers * 24
        slot = avail / len(col)
        y = grid_top
        cur_region = None
        for region, t, b, _sure in col:
            if region != cur_region:
                d.rectangle([x, y, x + col_w2, y + 20], fill=NAVY)
                d.text((x + 6, y + 3), region, font=region_f, fill=(255, 255, 255))
                y += 24
                cur_region = region
            ty = y + 3
            for line in wrap(d, t, title_f, col_w2)[:2]:
                d.text((x, ty), line, font=title_f, fill=INK)
                ty += 13
            by = ty + 1
            for line in wrap(d, b, body_f, col_w2)[:2]:
                d.text((x, by), line, font=body_f, fill=(55, 55, 55))
                by += 12
            y += slot
            d.line([x, y - 4, x + col_w2, y - 4], fill=(200, 195, 180), width=1)

    # ---------- footer ----------
    d.line([24, 984, W - 24, 984], fill=INK, width=2)
    foot_f = font(SANS, 10)
    foot = ("All stories first reported on Wednesday 25 November 2026  ·  "
            "Sources: Reuters, AP, BBC, AFP  ·  ● reported today   ○ developing")
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, 992), foot, font=foot_f, fill=INK)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
