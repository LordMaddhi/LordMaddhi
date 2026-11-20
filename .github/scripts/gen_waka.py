"""Pixel-art WakaTime panel -> assets/waka.svg (same style as the rest of the profile).

Top: level (from number of coding days) + main editor. No hours are shown. Middle: top languages. Bottom: 1-year activity heatmap.

Daily hours are kept in assets/waka-history.json. Every run adds the days the API
returns (last year if your plan allows it, otherwise the last 7 days), so the
heatmap keeps filling up. To fill the past right away, import a WakaTime export:
  py .github/scripts/gen_waka.py --import path/to/wakatime-export.json

Env:
  WAKATIME_API_KEY   API key
  WAKA_DEMO=1        render fake numbers (local preview only, don't commit)
  WAKA_PLACEHOLDER=1 render an empty panel
"""
import base64, contextlib, io, json, os, random, sys, urllib.error, urllib.request
from datetime import date, datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
HISTORY = os.path.join(ROOT, "assets", "waka-history.json")
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    from gen_pixel_ui import Px, WOOD, WOOD_D, WOOD_L  # noqa: E402

API = "https://wakatime.com/api/v1/users/current"
LANG_COLORS = {
    "Kotlin": "#7f52ff", "TypeScript": "#3178c6", "JavaScript": "#f7df1e", "Java": "#e76f00",
    "HTML": "#e34f26", "CSS": "#1572b6", "SCSS": "#cd6799", "SQL": "#c49a6c", "Python": "#3776ab",
    "Dart": "#0175c2", "YAML": "#cb171e", "XML": "#0060ac", "Markdown": "#9aa0b0", "JSON": "#8bc34a",
    "Docker": "#2496ed", "Bash": "#4eaa25", "Gradle": "#02303a", "TeX": "#008080",
}
FALLBACK = ["#ff4fd8", "#79c0ff", "#a8ff8a", "#ffd43b", "#ff9a5a", "#c9a0ff"]
HEAT = ["#141a33", "#1f4a3a", "#2f7a4a", "#5fbf5f", "#a8ff8a"]


# ---------------- data ----------------
def get(path):
    key = os.environ.get("WAKATIME_API_KEY", "").strip()
    if not key:
        sys.exit("WAKATIME_API_KEY missing")
    req = urllib.request.Request(API + path, headers={
        "Authorization": "Basic " + base64.b64encode(key.encode()).decode(),
        "User-Agent": "profile-readme-waka-panel/1.0",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        print(f"  {path} -> HTTP {e.code}: {body}", file=sys.stderr)
        return None


def stats():
    # all_time can be restricted (e.g. on the free plan) -> fall back to shorter ranges
    for rng in ("all_time", "last_year", "last_30_days", "last_7_days"):
        res = get(f"/stats/{rng}")
        if res and res.get("data", {}).get("languages"):
            if rng != "all_time":
                print(f"  using /stats/{rng} for languages", file=sys.stderr)
            return res["data"]
    sys.exit("could not load any WakaTime stats (see errors above)")


def load_history():
    try:
        with open(HISTORY, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


def save_history(h):
    with open(HISTORY, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dict(sorted(h.items())), fh, indent=0)
        fh.write("\n")


def add_days(hist, days):
    for d in days:
        hist[d["range"]["date"] if "range" in d else d["date"]] = round(d["grand_total"]["total_seconds"] / 3600, 2)


def fetch_days(hist):
    # Walk back to the account's creation date in 30-day chunks (the API rejects long ranges).
    # Chunks older than two weeks that are already in the history are skipped, so daily runs stay fast.
    end = date.today()
    user = (get("") or {}).get("data", {})
    created = (user.get("created_at") or "2024-01-01")[:10]
    oldest = date.fromisoformat(created)
    print(f"  account created {user.get('created_at')!r} -> fetching back to {oldest}", file=sys.stderr)
    recent = end - timedelta(days=14)
    got = 0
    while end >= oldest:
        start = max(oldest, end - timedelta(days=29))
        if end < recent and all(str(start + timedelta(days=i)) in hist for i in range((end - start).days + 1)):
            end = start - timedelta(days=1)
            continue
        res = get(f"/summaries?start={start}&end={end}")
        if not res or not res.get("data"):
            print(f"  stopped at {start}..{end}: API returned {str(res)[:200]!r}", file=sys.stderr)
            break  # older data not available (plan limit) -> keep what we have
        days = res.get("data", [])
        if os.environ.get("WAKA_DEBUG"):
            secs = sum(d["grand_total"]["total_seconds"] for d in days)
            print(f"  {start}..{end}: {len(days)} days, {secs / 3600:.1f} h", file=sys.stderr)
        add_days(hist, days)
        got += len(days)
        end = start - timedelta(days=1)
    print(f"  fetched {got} days of activity", file=sys.stderr)


def import_export(path, hist):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    days = data.get("days", data.get("data", []))
    add_days(hist, [d for d in days if "grand_total" in d])
    print(f"imported {len(days)} days from {path}")


def load():
    if os.environ.get("WAKA_DEMO"):
        random.seed(3)
        langs = [("Kotlin", 41.2), ("TypeScript", 22.5), ("Java", 9.8), ("HTML", 7.1), ("SQL", 6.4), ("YAML", 4.0)]
        hist = {}
        for i in range(372):
            d = date.today() - timedelta(days=i)
            hist[str(d)] = 0 if d.weekday() >= 5 and random.random() < .7 else round(random.random() ** 1.5 * 8, 1)
        return langs, hist, "IntelliJ IDEA"
    if os.environ.get("WAKA_PLACEHOLDER"):
        return [], {}, ""
    allt = stats()
    langs = [(l["name"], l["percent"]) for l in allt.get("languages", []) if l.get("percent", 0) > 0][:6]
    hist = load_history()
    fetch_days(hist)
    save_history(hist)
    editors = allt.get("editors") or []
    return langs, hist, editors[0]["name"] if editors else ""


# ---------------- render ----------------
def render(langs, hist, editor):
    P, GW, GH = 4, 244, 124
    p = Px(P)
    p.r(0, 0, GW, GH, WOOD_D); p.r(1, 1, GW - 2, GH - 2, WOOD); p.r(1, 1, GW - 2, 1, WOOD_L)
    p.r(4, 4, GW - 8, GH - 8, "#111"); p.r(5, 5, GW - 10, GH - 10, "#0b1020")
    for y in range(6, GH - 5, 2):
        p.r(5, y, GW - 10, 1, "#ffffff06")

    # header
    # level: every level needs more coding days (level n reached at 5*(n-1)^2 days)
    days = sum(1 for v in hist.values() if v > 0)
    lvl = int((days / 5) ** .5) + 1
    lo, hi = 5 * (lvl - 1) ** 2, 5 * lvl ** 2
    p.text("LVL", 10, 9, "#8b8bb0"); p.text(str(lvl), 24, 9, "#ffe39a", shadow="#5a4a10")
    xb = 24 + len(str(lvl)) * 4 + 4
    p.text("XP", xb, 9, "#8b8bb0")
    p.r(xb + 10, 9, 40, 5, "#1c2440")
    xw = round((days - lo) / (hi - lo) * 40)
    if xw:
        p.raw(f'<rect x="{(xb + 10) * P}" y="{9 * P}" width="0" height="{5 * P}" fill="#ff4fd8">'
              f'<animate attributeName="width" from="0" to="{xw * P}" begin=".2s" dur="1s" fill="freeze"/></rect>')
        p.r(xb + 10, 9, xw, 1, "#ffffff50")
    if editor:
        ed = editor.upper()[:20]
        p.text(ed, GW - 10 - len(ed) * 4, 9, "#ffe39a", shadow="#5a4a10")
        p.text("WEAPON", GW - 10 - len(ed) * 4 - 4 - 6 * 4, 9, "#8b8bb0")
    p.r(10, 17, GW - 20, 1, "#2a3050")

    # languages: two columns of three
    p.text("TOP LANGUAGES", 10, 21, "#ff4fd8", shadow="#5a1550")
    BWID = 46
    for i, (name, pct) in enumerate(langs or [("NO DATA YET", 0)]):
        col_x = 10 if i < 3 else 10 + (GW - 20) // 2 + 2
        y = 30 + (i % 3) * 8
        bx = col_x + 42
        p.text(name[:10], col_x, y, "#c9d1d9")
        if not langs:
            continue
        p.r(bx, y, BWID, 5, "#1c2440")
        w = max(1, round(pct / 100 * BWID))
        c = LANG_COLORS.get(name, FALLBACK[i % len(FALLBACK)])
        p.raw(f'<rect x="{bx * P}" y="{y * P}" width="0" height="{5 * P}" fill="{c}">'
              f'<animate attributeName="width" from="0" to="{w * P}" begin="{.2 + i * .12:.2f}s" dur=".6s" fill="freeze"/></rect>')
        p.text(f"{pct:.0f}%", bx + BWID + 3, y, "#8b8bb0")
    p.r(10, 55, GW - 20, 1, "#2a3050")

    # 1-year heatmap
    best = cur = 0
    for i in range(365, -1, -1):  # longest streak of coding days in the last year
        cur = cur + 1 if hist.get(str(date.today() - timedelta(days=i)), 0) > 0 else 0
        best = max(best, cur)
    p.text("LAST 12 MONTHS", 10, 59, "#79c0ff", shadow="#1a3a5a")
    if best:
        yh = f"{best} DAYS"
        p.text(yh, GW - 10 - len(yh) * 4, 59, "#ffe39a")
        p.text("BEST STREAK", GW - 10 - len(yh) * 4 - 4 - 11 * 4, 59, "#8b8bb0")
    today = date.today()
    first = today - timedelta(days=today.weekday() + 52 * 7)  # Monday, 53 columns
    GX, GY = 22, 75
    vals = [v for v in hist.values() if v > 0]
    peak = sorted(vals)[int(len(vals) * .95)] if vals else 1
    for lbl_i, lbl in ((0, "MO"), (2, "WE"), (4, "FR")):
        p.text(lbl, 10, GY + lbl_i * 4 - 1 if lbl_i else GY - 1, "#4a5070")
    last_label = -9
    for wk in range(53):
        for wd in range(7):
            d = first + timedelta(days=wk * 7 + wd)
            if d > today:
                continue
            if wd == 0 and d.day <= 7 and wk - last_label >= 4 and wk <= 50:
                p.text(d.strftime("%b").upper(), GX + wk * 4, GY - 8, "#4a5070")
                last_label = wk
            h = hist.get(str(d), 0)
            lvl = 0 if h <= 0 else min(4, 1 + int(h / peak * 3.999))
            x, y = GX + wk * 4, GY + wd * 4
            if lvl == 0:
                p.r(x, y, 3, 3, HEAT[0])
            else:
                p.raw(f'<rect x="{x * P}" y="{y * P}" width="{3 * P}" height="{3 * P}" fill="{HEAT[lvl]}" opacity="0">'
                      f'<set attributeName="opacity" to="1" begin="{.3 + wk * .025:.3f}s" fill="freeze"/></rect>')
    # legend
    lx = GW - 10 - 5 * 4 - 4 * 4 - 4 * 4
    p.text("LESS", lx - 18, GY + 31, "#4a5070")
    for i, c in enumerate(HEAT):
        p.r(lx + i * 4, GY + 31, 3, 3, c)
    p.text("MORE", lx + 5 * 4 + 2, GY + 31, "#4a5070")

    # footer
    p.raw('<g><animate attributeName="opacity" values="1;1;0;0" dur="1.2s" repeatCount="indefinite"/>')
    msg = f"NEXT LEVEL IN {hi - days} CODING DAYS" if days else "INSERT COIN"
    p.text(msg, 10, GH - 11, "#ff4fd8")
    p.raw("</g>")
    upd = f"UPDATED {datetime.now(timezone.utc):%Y-%m-%d}"
    p.text(upd, GW - 10 - len(upd) * 4, GH - 11, "#4a5070")
    p.save("waka.svg", GW, GH)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--import":
        h = load_history()
        import_export(sys.argv[2], h)
        save_history(h)
        sys.exit(0)
    render(*load())
