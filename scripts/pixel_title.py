"""Generate hero.svg and the README section cards: every text line drawn as flat pixel blocks (one <rect> per lit pixel).

Real geometry, not fonts, because GitHub's image proxy blocks web fonts in SVGs.
Glyphs are a hand-drawn 5x7 grid (lowercase descenders use two extra rows): Pillow's built-in
bitmap font is a 6px serif whose letters touch, which reads as noise.
One convention for every line: a block is 7/8 of its grid pitch; only the pitch changes per line.
Run from the repo root: python scripts/pixel_title.py
"""
from pathlib import Path

W, H = 1200, 340
FILL_RATIO = 7 / 8

G = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "j": ["..#", "...", ".##", "..#", "..#", "..#", "..#", "#.#", ".#."],
    "k": ["#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."],
    "-": ["...", "...", "...", "###", "...", "...", "..."],
    "'": ["#", "#", ".", ".", ".", ".", "."],
    "(": ["..#", ".#.", "#..", "#..", "#..", ".#.", "..#"],
    ")": ["#..", ".#.", "..#", "..#", "..#", ".#.", "#.."],
    "%": ["##...", "##..#", "...#.", "..#..", ".#...", "#..##", "...##"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    ":": ["..", "..", "##", "##", "..", "##", "##"],
    "b": ["#....", "#....", "####.", "#...#", "#...#", "#...#", "####."],
    "f": ["..##.", ".#..#", ".#...", "###..", ".#...", ".#...", ".#..."],
    "h": ["#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"],
    "o": [".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."],
    "u": [".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"],
    "v": [".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "w": [".....", ".....", "#...#", "#...#", "#.#.#", "#.#.#", ".#.#."],
    "x": [".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"],
    "’": [".#", ".#", "#.", "..", "..", "..", ".."],
    "“": [".#.#", "#.#.", "....", "....", "....", "....", "...."],
    "”": [".#.#", "#.#.", "....", "....", "....", "....", "...."],
    "—": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["###", ".#.", ".#.", ".#.", ".#.", ".#.", "###"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "a": [".....", ".....", ".###.", "....#", ".####", "#...#", ".####"],
    "c": [".....", ".....", ".###.", "#....", "#....", "#...#", ".###."],
    "d": ["....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"],
    "e": [".....", ".....", ".###.", "#...#", "#####", "#....", ".###."],
    "g": [".....", ".....", ".####", "#...#", "#...#", "#...#", ".####", "....#", ".###."],
    "i": [".#.", "...", "##.", ".#.", ".#.", ".#.", "###"],
    "l": ["##.", ".#.", ".#.", ".#.", ".#.", ".#.", "###"],
    "m": [".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"],
    "n": [".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"],
    "p": [".....", ".....", "####.", "#...#", "#...#", "#...#", "####.", "#....", "#...."],
    "r": [".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."],
    "s": [".....", ".....", ".####", "#....", ".###.", "....#", "####."],
    "t": [".#...", ".#...", "####.", ".#...", ".#...", ".#..#", "..##."],
    "y": [".....", ".....", "#...#", "#...#", "#...#", "#...#", ".####", "....#", ".###."],
    "/": ["....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."],
    "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    ",": ["..", "..", "..", "..", "..", ".#", ".#", "#."],
    ".": ["..", "..", "..", "..", "..", "##", "##"],
    " ": ["...", "...", "...", "...", "...", "...", "..."],
}

# (text, x, top, pitch, colour, extra columns between letters). Pitches are ~15% over the previous
# rendered sizes; the two small lines are floored at 2px so they stay legible at GitHub's ~0.7x scale.
LINES = [
    ("AI / ML ENGINEER", 64, 64, 2.0, "#6b7f99", 1),
    ("PRANJAL H DOHARE", 64, 100, 9.2, "#dfe4ea", 0),
    ("Deep learning, LLMs, RAG and agentic AI systems.", 64, 188, 2.6, "#8d98a8", 0),
]
QUOTE = ("“The complexity and magnitude of both today’s opportunities and challenges demand the collaborative "
         "efforts of the world’s very best researchers.” — Geoffrey Hinton")
QUOTE_X, QUOTE_TOP, QUOTE_PITCH, QUOTE_LEADING, QUOTE_MAX_X = 64, 234, 2.0, 26, 900
G[" "] = G[" "]  # non-breaking space keeps the attribution on one line


def wrap(text, max_cols, tracking=0):
    width = lambda t: sum(len(G[ch][0]) + 1 + tracking for ch in t) - 1 - tracking
    lines = [""]
    for word in text.split(" "):
        trial = f"{lines[-1]} {word}".strip()
        if width(trial) <= max_cols or not lines[-1]:
            lines[-1] = trial
        else:
            lines.append(word)
    return lines


LINES += [(t, QUOTE_X, QUOTE_TOP + i * QUOTE_LEADING, QUOTE_PITCH, "#c9a66b", 0)
          for i, t in enumerate(wrap(QUOTE, int((QUOTE_MAX_X - QUOTE_X) / QUOTE_PITCH)))]

# Background: a sparse, seeded scatter of single blocks on the title's pixel grid, denser toward the right edge.
SCATTER_N, SCATTER_SEED, SCATTER_OPACITY = 22, 7, 0.2
TINTS = ["#7c9fd0", "#6fae98", "#a08ed4", "#c98088", "#b07a52"]
GRID_X0, GRID_Y0, GRID_PITCH = 64, 114, 9.2  # the title's grid, so the scatter lines up with its blocks


def scatter(text_boxes, clearance=24, min_gap=3):
    import random
    rng = random.Random(SCATTER_SEED)
    b = round(GRID_PITCH * FILL_RATIO, 2)
    cells = []
    while len(cells) < SCATTER_N:
        # right band (x 930-1170) with sqrt bias toward the edge, plus a thin bottom strip (y 285-310)
        x = 930 + 240 * rng.random() ** 0.5 if rng.random() < 0.75 else 720 + 450 * rng.random()
        y = 30 + 280 * rng.random() if x >= 930 else 285 + 25 * rng.random()
        c = (round((x - GRID_X0) / GRID_PITCH), round((y - GRID_Y0) / GRID_PITCH))
        x, y = GRID_X0 + c[0] * GRID_PITCH, GRID_Y0 + c[1] * GRID_PITCH
        if not (24 <= x and x + b <= W - 24 and 24 <= y and y + b <= H - 24):
            continue  # snapping pushed it into the edge margin
        if any(x0 - clearance < x + b and x < x1 + clearance and y0 - clearance < y + b and y < y1 + clearance
               for x0, y0, x1, y1 in text_boxes):
            continue  # too close to a text line
        if any(abs(c[0] - d[0]) < min_gap and abs(c[1] - d[1]) < min_gap for d in cells):
            continue  # keep blocks apart so they never clump into shapes
        cells.append(c)
    groups = {t: [] for t in TINTS}
    for i, (cx, cy) in enumerate(cells):
        x, y = GRID_X0 + cx * GRID_PITCH, GRID_Y0 + cy * GRID_PITCH
        groups[TINTS[i % len(TINTS)]].append(f'<rect x="{x:g}" y="{y:g}" width="{b:g}" height="{b:g}"/>')
    return "\n".join(f'  <g fill="{t}" fill-opacity="{SCATTER_OPACITY}">{"".join(r)}</g>' for t, r in groups.items())

def pixels(text, tracking):
    col = 0
    for ch in text:
        g = G[ch]
        assert len({len(r) for r in g}) == 1 and len(g) in (7, 8, 9), ch
        for y, row in enumerate(g):
            for x, c in enumerate(row):
                if c == "#":
                    yield col + x, y
        col += len(g[0]) + 1 + tracking


def line(text, x0, top, pitch, colour, tracking):
    px = list(pixels(text, tracking))
    b = round(pitch * FILL_RATIO, 2)
    rects = "".join(f'<rect x="{x0 + x * pitch:g}" y="{top + y * pitch:g}" width="{b:g}" height="{b:g}"/>' for x, y in px)
    box = (x0, top, x0 + max(x for x, _ in px) * pitch + b, top + max(y for _, y in px) * pitch + b)
    return f'  <g fill="{colour}">{rects}</g>', box


def build():
    parts, boxes = [], []
    for spec in LINES:
        svg, box = line(*spec)
        parts.append(svg)
        boxes.append(box)
    for x0, y0, x1, y1 in boxes:  # self-check: inside the banner with a margin
        assert 24 <= x0 and x1 <= W - 24 and 24 <= y0 and y1 <= H - 24, (x0, y0, x1, y1)
    for a, b in zip(boxes, boxes[1:]):  # and lines stacked without overlap
        assert a[3] + 8 <= b[1], (a, b)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
  <title id="t">Pranjal H Dohare</title>
  <desc id="d">AI/ML engineer working across deep learning, LLMs, RAG and agentic AI. Quote: “The complexity and magnitude of both today’s opportunities and challenges demand the collaborative efforts of the world’s very best researchers.” — Geoffrey Hinton.</desc>
  <!-- Generated by scripts/pixel_title.py. Palette from the portfolio's App.css; text is pixel geometry because web fonts can't load here. -->
  <rect width="{W}" height="{H}" rx="12" fill="#0a0e16"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="#6b7f99" stroke-opacity="0.3"/>
  <!-- Background: a sparse scatter of faint pixel blocks, clear of the text. -->
{scatter(boxes)}
{chr(10).join(parts[:3])}
  <!-- The single accent use: the quote. -->
{chr(10).join(parts[3:])}
</svg>
""", boxes


# 9x9 pixel icons for the contact card, same block convention as the text.
ICONS = {
    "email":     [".........", "#########", "##.....##", "#.#...#.#", "#..#.#..#", "#...#...#", "#.......#", "#########", "........."],
    "github":    [".##...##.", ".###.###.", ".#######.", "#########", "##.###.##", "#########", ".#######.", "..##.##..", "..#...#.."],
    "linkedin":  [".#######.", "##.######", "#########", "##.#...##", "##.#.#.##", "##.#.#.##", "##.#.#.##", "##.#.#.##", ".#######."],
    "x":         ["##.....##", ".##...##.", "..##.##..", "...###...", "....#....", "...###...", "..##.##..", ".##...##.", "##.....##"],
    "portfolio": ["..#####..", ".#..#..#.", "#..#.#..#", "#########", "#..#.#..#", "#..#.#..#", "#########", ".#..#..#.", "..#####.."],
}

# Section cards: same canvas, glyphs and block rule as the banner, so the whole README reads as one system.
X0, MARGIN, LEAD = 64, 36, 12  # LEAD: line advance in grid rows (7 caps + 2 descender + 3 air)
INK, MUTED, SLATE = "#dfe4ea", "#8d98a8", "#6b7f99"


def icon(rows, x0, top, pitch, colour):
    b = round(pitch * FILL_RATIO, 2)
    rects = "".join(f'<rect x="{x0 + x * pitch:g}" y="{top + y * pitch:g}" width="{b:g}" height="{b:g}"/>'
                    for y, row in enumerate(rows) for x, c in enumerate(row) if c == "#")
    return f'  <g fill="{colour}">{rects}</g>', x0 + len(rows[0]) * pitch


def card(items, label, text_max_x=W - X0):
    """items: ("text", str, pitch, colour, tracking) wrapped at text_max_x; ("words", [str], pitch, colour, gap);
    ("contacts", [(icon, label)], pitch, gap); ("gap", px)."""
    out, y = [], MARGIN
    for kind, *a in items:
        if kind == "gap":
            y += a[0]
            continue
        if kind == "text":
            text, pitch, colour, tracking, *hl = a
            colours = [colour] * len(text)  # per-character colour, so highlighted phrases survive wrapping
            for phrase, c in (hl[0] if hl else ()):
                i = text.index(phrase)
                colours[i:i + len(phrase)] = [c] * len(phrase)
            start = 0
            for t in wrap(text, int((text_max_x - X0) / pitch), tracking):
                cols, col, run = colours[start:start + len(t)], 0, 0
                for k in range(1, len(t) + 1):  # draw each same-colour run at its column offset
                    if k == len(t) or cols[k] != cols[run]:
                        seg = t[run:k]
                        if seg.strip():
                            svg, box = line(seg, X0 + col * pitch, y, pitch, cols[run], tracking)
                            assert box[2] <= text_max_x, (t, box)  # self-check: wrapped text stays inside the margin
                            out.append(svg)
                        col += sum(len(G[ch][0]) + 1 + tracking for ch in seg)
                        run = k
                start += len(t) + 1  # wrap() joins words with single spaces
                y += LEAD * pitch
            continue
        x = X0
        if kind == "words":
            words, pitch, colour, gap = a
            for word in words:
                svg, box = line(word, x, y, pitch, colour, 0)
                out.append(svg)
                x = box[2] + gap
        else:  # contacts: muted pixel icon, then the label in ink
            pairs, pitch, gap = a
            for name, text in pairs:
                svg, x = icon(ICONS[name], x, y - pitch, pitch, MUTED)  # 9-row icon centred on 7-row caps
                out.append(svg)
                svg, box = line(text, x + 3 * pitch, y, pitch, INK, 0)
                out.append(svg)
                x = box[2] + gap
        assert x - gap <= W - X0, a  # self-check: row fits the canvas
        y += LEAD * pitch
    h = round(y - 2 * pitch + MARGIN)  # drop the last row's trailing air
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{label}">
  <!-- Generated by scripts/pixel_title.py. Dark canvas so the ink text stays readable on GitHub's light theme. -->
  <rect width="{W}" height="{h}" rx="12" fill="#0a0e16"/>
{chr(10).join(out)}
</svg>
"""


ABOUT = ("I train neural networks, deep learning models and reinforcement learning agents that act on their own. "
         "I'm focused on deep learning research and applied ML. I also work on LLMs, RAG, MCP and agentic AI systems.")
SRE = ("Agentic SRE OpenEnv",
       "A reinforcement learning environment that drops agents into simulated production incidents and scores their "
       "response the way an on-call rotation would judge a human.",
       "The policy model is GLM-5.2 (open-weight). It uses hybrid memory (pgvector plus a Postgres causal graph), "
       "tools wrapped in MCP, and a ToRA-style planning loop.")
ORAL = ("Tri-Branch Fusion CNN: Oral Cancer Screening",
        "Validation accuracy: 72.02%.",
        "My capstone (BAI685): non-invasive oral cancer screening that pairs autofluorescence imaging (AFI) with edge AI. "
        "It fuses three branches (a WLI RGB CNN, an AFI grayscale CNN and a metadata MLP) and targets sub-200 ms INT8 "
        "TFLite inference on an ESP32-S3.")
BLUE, TEAL, VIOLET, ROSE, CLAY = "#7c9fd0", "#6fae98", "#a08ed4", "#c98088", "#b07a52"
SKILL_ROWS = [(BLUE, ["Deep Learning", "Machine Learning", "LLMs", "RAG", "MCP", "Agentic AI"]), (TEAL, ["Python", "Java"])]
CONTACTS = [("email", "Email"), ("github", "GitHub"), ("linkedin", "LinkedIn"), ("x", "X"), ("portfolio", "Portfolio")]


def kicker(text):
    return [("text", text, 2.0, SLATE, 1), ("gap", 14)]


def project(title, metric, desc, metric_colour, heading=()):
    return [*heading, ("text", title, 3.6, INK, 0), ("gap", 10), ("text", metric, 2.6, metric_colour, 0), ("gap", 8),
            ("text", desc, 2.6, MUTED, 0)]


def cards():
    return {
        "about.svg": card([*kicker("ABOUT"), ("text", ABOUT, 2.6, INK, 0)], f"About. {ABOUT}"),
        "project-sre.svg": card(project(*SRE, VIOLET, heading=kicker("PROJECTS")), "Projects. " + " ".join(SRE)),
        "project-oral.svg": card(project(*ORAL, ROSE), " ".join(ORAL)),
        "skills.svg": card([*kicker("SKILLS"), *(("words", row, 2.6, c, 48) for c, row in SKILL_ROWS)],
                           "Skills: " + ", ".join(n for _, row in SKILL_ROWS for n in row)),
        "contact.svg": card([*kicker("CONTACT"), ("contacts", CONTACTS, 2.6, 44)],
                            "Contact: " + ", ".join(t for _, t in CONTACTS)),
    }


if __name__ == "__main__":
    svg, boxes = build()
    root = Path(__file__).resolve().parent.parent
    (root / "hero.svg").write_text(svg, encoding="utf-8", newline="\n")
    for name, body in cards().items():
        (root / name).write_text(body, encoding="utf-8", newline="\n")
        print("wrote", name)
