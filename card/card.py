"""Draw the profile card as two animated SVGs, one per theme.

    python3 card/card.py PORTRAIT CALENDAR OUT_DIR

PORTRAIT is the JSON that portrait.py writes. CALENDAR is the
contribution calendar as a JSON list of {"date", "contributionCount"},
oldest first, one entry per day. The script writes card-dark.svg and
card-light.svg into OUT_DIR. It needs only the standard library, so the
nightly run installs nothing.
"""
import json
import random
import sys
from calendar import monthrange
from datetime import date
from html import escape
from itertools import groupby

THEMES = {
    "dark": dict(frame="#292e42", fg="#c0caf5", dim="#565f89", key="#7aa2f7",
                 head="#bb9af7", ok="#9ece6a", cyan="#7dcfff"),
    "light": dict(frame="#c4c8da", fg="#3760bf", dim="#848cb5", key="#2e7de9",
                  head="#9854f1", ok="#587539", cyan="#007197"),
}
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
# portrait.py sizes the portrait for cells this wide and this high.
CELL_W, LINE_H = 4.2, 8.0
RAMP = ".,:;-=+*#%&@"
WIDTH = 74
JOINED = date(2018, 6, 17)
SCRAMBLE = "!<>-_/[]{}=+*^?#%&"
DECODE_FRAMES, DECODE_STEP = 7, 0.1  # .f in STYLE lasts DECODE_STEP
LIGHT_ONLY = 'echo "You found the light side. Most visitors never see this line."'

STYLE = """
.a{opacity:0;animation:in .35s ease-out forwards}
@keyframes in{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}
.d{opacity:0;animation:on .01s forwards}
@keyframes on{to{opacity:1}}
.f{opacity:0;animation:flash .1s linear}
@keyframes flash{from,to{opacity:1}}
.type{clip-path:inset(0 100% 0 0);animation:type 1s steps(22) .2s forwards}
@keyframes type{to{clip-path:inset(0 0 0 0)}}
.cur{animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.open{animation:open 5s 3.2s infinite}
@keyframes open{0%,93%,98%,100%{opacity:1}94%,97%{opacity:0}}
.shut{opacity:0;animation:shut 5s 3.2s infinite}
@keyframes shut{0%,93%,98%,100%{opacity:0}94%,97%{opacity:1}}
.scan{opacity:0;animation:scan 12s 3s infinite}
@keyframes scan{0%{opacity:1;transform:translateY(0)}12%{opacity:1;transform:translateY(var(--h))}13%,100%{opacity:0}}
@media (prefers-reduced-motion:reduce){.a,.d,.type{animation:none;opacity:1;clip-path:none}
.f,.shut,.scan{display:none}.open,.cur{animation:none}}
"""


def uptime(since, today):
    y, m, d = today.year - since.year, today.month - since.month, today.day - since.day
    if d < 0:
        m -= 1
        d += monthrange(today.year - (today.month == 1), (today.month - 2) % 12 + 1)[1]
    if m < 0:
        y, m = y - 1, m + 12
    return f"{y} Years, {m} Months, {d} Days"


def stats(days):
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for n in counts:
        run = run + 1 if n else 0
        longest = max(longest, run)
    # Today is still running, so a quiet today does not break the streak yet.
    counted = counts[:-1] if counts and not counts[-1] else counts
    current = 0
    for n in reversed(counted):
        if not n:
            break
        current += 1
    return dict(
        total=sum(counts),
        active=sum(1 for n in counts if n),
        current=current,
        longest=longest,
        busiest=max(counts),
        best_week=max(sum(counts[i:i + 7]) for i in range(0, len(counts), 7)),
    )


def leader(key, value, width=WIDTH):
    return [("key", key), ("dim", " " + "." * (width - len(key) - len(value) - 2) + " "), ("fg", value)]


def rule(title, width=WIDTH):
    return [("head", title), ("dim", " " + "─" * (width - len(title) - 1))]


def info(days, today):
    s = stats(days)
    half = (WIDTH - 3) // 2
    pair = lambda a, b: leader(*a, half) + [("dim", " │ ")] + leader(*b, half)
    return [
        [("head", "matt"), ("dim", "@"), ("head", "walsh"), ("dim", " " + "─" * (WIDTH - 11))],
        leader("OS", "Omarchy 4.5 · Hyprland · Wayland"),
        leader("Host", "Framework Laptop 13 · Ryzen AI 7 350"),
        leader("Role", "Engineer Of Things"),
        leader("Uptime", uptime(JOINED, today)),
        [],
        leader("Languages.Code", "Go, Python, TypeScript, Bash, PHP"),
        leader("Languages.Config", "HCL, YAML, TOML, Lua"),
        leader("Frameworks", "Magento, Shopify, Laravel"),
        leader("Tools.Infra", "OpenTofu, Docker, GitHub Actions, Chezmoi"),
        leader("Tools.Agents", "Claude Code, Codex, Grok"),
        [],
        leader("Builds", "Dev Environments, Infra As Code, Agent Tooling"),
        leader("Rule", "Everything Is Code"),
        [],
        rule("Contact"),
        leader("LinkedIn", "linkedin.com/in/matt-walsh-51220b67"),
        leader("X", "@mattgrul"),
        [],
        rule("GitHub · Past 12 Months"),
        pair(("Contributions", f"{s['total']:,}"), ("Active Days", f"{s['active']}")),
        pair(("Current Streak", f"{s['current']} Days"), ("Longest Streak", f"{s['longest']} Days")),
        pair(("Busiest Day", f"{s['busiest']}"), ("Best Week", f"{s['best_week']}")),
        [],
        [("heatmap", days)],
        [], [], [],
    ]


def tint(rgb, theme):
    """Lift colours on the dark card and sink them on the light one, so each reads."""
    peak = max(rgb) or 1
    target = max(peak, 200) if theme == "dark" else min(peak, 140)
    return "#%02x%02x%02x" % tuple(min(255, int(c * target / peak)) // 8 * 8 for c in rgb)


def glyph(tone, theme):
    """Draw light tones dense on the dark card, and dark tones dense on the light one."""
    if theme == "light":
        tone = 255 - tone
    return RAMP[tone * len(RAMP) // 256]


def portrait_row(row, theme):
    coloured = [(" ", None) if cell is None else (glyph(cell[0], theme), tint(cell[1:], theme)) for cell in row]
    spans = []
    for colour, group in groupby(coloured, key=lambda cell: cell[1]):
        text = escape("".join(ch for ch, _ in group))
        spans.append(f'<tspan fill="{colour}">{text}</tspan>' if colour else text)
    return "".join(spans)


def shut_eyes(cells, eyes, y):
    """Return row y with the eyes drawn as closed lids: skin from the cheek, and a darker lash line at the bottom."""
    row = list(cells[y])
    cheek = cells[eyes["rows"][-1] + 3]
    for start, stop in eyes["cols"]:
        for x in range(start, stop):
            if row[x] and cheek[x]:
                lash = [100, *(int(v * 0.6) for v in cheek[x][1:])]
                row[x] = lash if y == eyes["rows"][-1] else cheek[x]
    return row


def heatmap(days, c, x0, y0, start):
    """Draw the contribution calendar as a grid of cells, one column per week, swept in left to right."""
    first = date.fromisoformat(days[0]["date"])
    first_sunday = first.toordinal() - (first.weekday() + 1) % 7
    peak = max(d["contributionCount"] for d in days) or 1
    cells = []
    for day in days:
        when = date.fromisoformat(day["date"])
        col, row = (when.toordinal() - first_sunday) // 7, (when.weekday() + 1) % 7
        n = day["contributionCount"]
        # A square root scale, so one huge day does not wash out the rest of the year.
        level = 0 if n == 0 else 1 + min(3, int((n / peak) ** 0.5 * 4))
        fill, alpha = (c["frame"], 1) if level == 0 else (c["ok"], (0.3, 0.5, 0.75, 1)[level - 1])
        cells.append(f'<rect class="a" style="animation-delay:{start + col * 0.02:.2f}s" x="{x0 + col * 11:.0f}" '
                     f'y="{y0 + row * 11}" width="9" height="9" rx="2" fill="{fill}" fill-opacity="{alpha}"/>')
    return cells


def scramble(parts, rng):
    """Swap each value character for a random symbol; keys and dot leaders stay."""
    return [(k, "".join(ch if ch == " " or k != "fg" else rng.choice(SCRAMBLE) for ch in v)) for k, v in parts]


def text_row(parts, c):
    return "".join(f'<tspan fill="{c[k]}">{escape(v)}</tspan>' for k, v in parts)


def svg(theme, picture, days, today):
    c = THEMES[theme]
    cells, eyes = picture["cells"], picture["eyes"]
    rng = random.Random(7)
    # No window frame or background: the card sits straight inside the
    # README box that GitHub draws, on GitHub's own page colour.
    px, py = 8, 50
    ix, ilh = 428, 18.6
    lines = info(days, today)
    cols = len(cells[0])
    height = int(max(py + len(cells) * LINE_H, py + len(lines) * ilh) + 30)
    w = 1036
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" font-family="{FONT}">',
        f"<style>{STYLE}</style>",
        f'<defs><linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["cyan"]}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{c["cyan"]}" stop-opacity=".28"/><stop offset="1" stop-color="{c["cyan"]}" stop-opacity="0"/></linearGradient></defs>',
    ]
    out.append(f'<text class="type" x="{px}" y="16" font-size="14" xml:space="preserve">'
               f'<tspan fill="{c["ok"]}">❯</tspan><tspan fill="{c["fg"]}"> fastfetch --profile mattgrul</tspan></text>')

    t0 = 1.3
    for y, row in enumerate(cells):
        at = f'x="{px}" y="{py + y * LINE_H:.1f}" font-size="7" xml:space="preserve"'
        drawn = f'<text class="a" style="animation-delay:{t0 + y * 0.025:.3f}s" {at}>{portrait_row(row, theme)}</text>'
        if y in eyes["rows"]:
            # Whole rows swap, not single cells, so the lids line up in any monospace font.
            drawn = (f'<g class="open">{drawn}</g>'
                     f'<text class="shut" {at}>{portrait_row(shut_eyes(cells, eyes, y), theme)}</text>')
        out.append(drawn)
    top, bottom = py - 30, py + len(cells) * LINE_H
    out.append(f'<rect class="scan" style="--h:{bottom - top:.0f}px" x="{px - 8}" y="{top}" width="{cols * CELL_W + 16:.0f}" '
               f'height="30" fill="url(#scan)"/>')

    t1 = t0 + 0.3
    for i, parts in enumerate(lines):
        if not parts:
            continue
        y = py + i * ilh
        t = t1 + i * 0.06
        if parts[0][0] == "heatmap":
            out += heatmap(parts[0][1], c, ix, y - 12, t)
            continue
        at = f'x="{ix}" y="{y}" font-size="13.5" xml:space="preserve"'
        if not any(k == "fg" for k, _ in parts):
            out.append(f'<text class="a" style="animation-delay:{t:.2f}s" {at}>{text_row(parts, c)}</text>')
            continue
        # Decode: frames of random symbols hold the line for a moment, then the real line shows.
        for f in range(DECODE_FRAMES):
            out.append(f'<text class="f" style="animation-delay:{t + f * DECODE_STEP:.2f}s" {at}>{text_row(scramble(parts, rng), c)}</text>')
        out.append(f'<text class="d" style="animation-delay:{t + DECODE_FRAMES * DECODE_STEP:.2f}s" {at}>{text_row(parts, c)}</text>')

    end = t1 + len(lines) * 0.06 + DECODE_FRAMES * DECODE_STEP + 0.2
    said = f'<tspan fill="{c["fg"]}"> {escape(LIGHT_ONLY)}</tspan>' if theme == "light" else ""
    out.append(f'<text class="a" style="animation-delay:{end:.2f}s" x="{px}" y="{height - 6}" font-size="14" xml:space="preserve">'
               f'<tspan fill="{c["ok"]}">❯</tspan>{said}<tspan fill="{c["fg"]}"> </tspan>'
               f'<tspan class="cur" fill="{c["key"]}">█</tspan></text>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    picture_path, calendar_path, out_dir = sys.argv[1:4]
    with open(picture_path) as f:
        picture = json.load(f)
    with open(calendar_path) as f:
        days = json.load(f)
    for theme in THEMES:
        with open(f"{out_dir}/card-{theme}.svg", "w") as f:
            f.write(svg(theme, picture, days, date.today()))
