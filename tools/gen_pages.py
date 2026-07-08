#!/usr/bin/env python3
import re, sys, os, glob, json
sys.path.insert(0, os.path.dirname(__file__))
from brand_content import BRANDS

ROOT = "/Users/macbook/cynmedi-redesign"
VARIN = open(f"{ROOT}/work/varinpat.html", encoding="utf-8").read()

def extract(pattern, s, flags=re.S):
    m = re.search(pattern, s, flags)
    return m.group(0) if m else ""

# Reusable chunks pulled verbatim from varinpat (brand-agnostic)
HEAD = VARIN[:VARIN.index('<body class="antialiased">')]  # <!doctype>..</head> incl style
HEADER = extract(r'<header .*?</header>', VARIN)
TRUSTED = extract(r'<!-- ═+ TRUSTED BY ═+ -->\s*<section.*?</section>', VARIN)
FOOTER = extract(r'<footer .*?</footer>', VARIN)
SCRIPT = extract(r'<script>.*?</script>', VARIN)

def reels_for(slug, cat):
    files = sorted(glob.glob(f"{ROOT}/assets/client/{cat}/{slug}/reel-*.mp4"),
                   key=lambda p: int(re.search(r'reel-(\d+)', p).group(1)))
    return [f"/assets/client/{cat}/{slug}/{os.path.basename(f)}?v=1" for f in files]

# Full aesthetic-clinic showcase strip (cover clip/image), same as work.html.
# (name, src, is_image, page_slug). Links only if work/<slug>.html exists.
AESTHETIC_SHOWCASE = [
    ("Varinpat",      "/assets/varinpat.mp4", False, "varinpat"),
    ("Astell",        "/assets/astell.mp4", False, "astell"),
    ("The Bloom",     "/assets/the-bloom.jpg", True, "the-bloom"),
    ("Klear Clinic",  "/assets/client/aesthetic/klear-clinic.mp4", False, "klear"),
    ("Parapin",       "/assets/client/aesthetic/parapin-clinic.mp4", False, "parapin"),
    ("La Claire",     "/assets/la-claire.mp4", False, "la-clair"),
    ("So On",         "/assets/so-on.mp4", False, "so-on"),
    ("Chaba",         "/assets/chaba.mp4", False, "chaba"),
    ("QIS",           "/assets/qis.mp4", False, "qis"),
    ("Rapi Clinic",   "/assets/client/aesthetic/rapi-clinic.mp4", False, "rapi"),
    ("Rancha Clinic", "/assets/client/aesthetic/rancha-clinic.mp4", False, "rancha"),
    ("Dr. Fern",      "/assets/client/aesthetic/dr-fern.mp4", False, "dr-fern"),
    ("Jil Wink",      "/assets/client/aesthetic/jil-wink/reel-1.mp4", False, "jil-wink"),
]

# Dental & wellness showcase (work.html data-cat="wellness" group)
DENTAL_SHOWCASE = [
    ("Pun Smile",      "/assets/punsmile.mp4?v=2", False, "pun-smile"),
    ("Craft Dental",   "/assets/craft-dental.mp4?v=3", False, "craft-dental"),
    ("Bangkok Dental", "/assets/bangkok-dental.mp4", False, "bangkok-dental"),
    ("Double B",       "/assets/double-b.mp4", False, "double-b"),
    ("Youyen",         "/assets/client/wellness/youyen.mp4", False, "youyen"),
    ("Dr. Supparuk",   "/assets/client/wellness/dr-supparuk-clinic.mp4", False, "dr-supparuk"),
    ("Premier Ultrasound", "/assets/client/wellness/premier-ultrasound-clinic.mp4", False, "premier"),
    ("Samitivej",      "/assets/client/wellness/samitivej.mp4", False, "samitivej"),
    ("Medispine",      "/assets/client/wellness/medispine.mp4", False, "medispine"),
    ("MS Rehab",       "/assets/client/wellness/ms-rehab.mp4", False, "ms-rehab"),
]

# "Other industries" showcase (work.html data-cat="other" group)
OTHER_SHOWCASE = [
    ("Blink Babe",   "/assets/client/other/blink-babe.mp4", False, "blink-babe"),
    ("Keeree",       "/assets/client/other/keeree.mp4", False, "keeree"),
    ("The Attic",    "/assets/client/other/the-attic.mp4", False, "the-attic"),
    ("Mental Matters","/assets/client/other/mental-matters.mp4", False, "mental-matters"),
    ("Cside",        "/assets/cside.mp4", False, "cside"),
    ("Natural Joy Vision","/assets/natural-joy-vision.mp4", False, "natural-joy-vision"),
    ("Supersup",     "/assets/supersup.mp4", False, "supersup"),
    ("Zendori",      "/assets/zendori.mp4", False, "zendori"),
    ("L'ambiance Cafe","/assets/client/other/lambiance-cafe.mp4", False, "lambiance-cafe"),
    ("The Crane",    "/assets/client/other/the-crane.mp4", False, "the-crane"),
    ("Sanipa Resort","/assets/client/other/sanipa-resort.mp4", False, "sanipa-resort"),
    ("MedNinja",     "/assets/client/other/medninja.mp4", False, "medninja"),
    ("Home 369",     "/assets/client/other/home369.mp4", False, "home369"),
    ("Quality Plus", "/assets/client/other/quality-plus.mp4", False, "quality-plus"),
]

def sc_card(name, src, is_img, slug):
    media = (f'<img src="{src}" alt="{name}" class="sc-zoom-img" loading="lazy"/>' if is_img
             else f'<video class="sc-vid" autoplay muted loop playsinline preload="none"><source src="{src}" type="video/mp4"></video>')
    body = f'{media}\n                    <div class="sc-scrim"></div>\n                    <div class="sc-name">{name}</div>'
    if slug and os.path.exists(f"{ROOT}/work/{slug}.html"):
        return f'<a href="/work/{slug}.html" class="sc-card">\n                    {body}\n                </a>'
    return f'<div class="sc-card">\n                    {body}\n                </div>'

def showcase_cards(slug, cat="aesthetic"):
    strip = {"dental": DENTAL_SHOWCASE, "wellness": DENTAL_SHOWCASE, "other": OTHER_SHOWCASE}.get(cat, AESTHETIC_SHOWCASE)
    return [sc_card(n, s, img, pg) for (n, s, img, pg) in strip if pg != slug]

def build(slug):
    b = BRANDS[slug]; cat = b["category"]
    reels = reels_for(slug, cat)
    n = len(reels)
    hero3 = reels[:3] if len(reels) >= 3 else reels
    PH = "<!-- ⚠ PLACEHOLDER METRIC — replace with real data -->"
    _parts = b["name"].rsplit(" ", 1)
    name_first, name_rest = (_parts[0], _parts[1]) if len(_parts) == 2 else (b["name"], "")

    hero_vids = "\n        ".join(
        f'<video autoplay muted loop playsinline preload="auto"><source src="{r}" type="video/mp4"></video>'
        for r in hero3)

    def m_reel(r, hidden=False):
        h = ' aria-hidden="true"' if hidden else ' onclick="toggleOne(this)"'
        return (f'<div class="m-reel"{h}><video autoplay muted loop playsinline preload="auto">'
                f'<source src="{r}" type="video/mp4"></video></div>')
    marquee = "\n                ".join([m_reel(r) for r in reels] + [m_reel(r, True) for r in reels])

    def ac_slide(r, first=False):
        pl = "metadata" if first else "none"
        return (f'<div class="ac-slide"><video muted loop playsinline controls '
                f'controlslist="nofullscreen nodownload noplaybackrate" preload="{pl}" src="{r}"></video></div>')
    carousel = "\n                            ".join(ac_slide(r, i == 0) for i, r in enumerate(reels))

    results = "\n                ".join(
        f'''<div class="result-row">
                    <div class="result-num"{(' style="color:#2D4DB1"' if i==1 else '')}>{num}</div>
                    <p class="text-ink-500 text-[15px] leading-relaxed mt-3 md:mt-0">{desc}</p>
                </div>'''
        for i, (num, lab, desc) in enumerate(b["results"]))

    chips = "\n                        ".join(f'<span class="chip">{t}</span>' for t in b["tags"])

    cards = "\n                ".join(showcase_cards(slug, cat))
    morework_inner = f'''<div class="scroll-strip reveal-clip" id="moreWorkStrip">
                {cards}
            </div>
            <div class="mw-scrollbar" id="mwScrollbar" role="scrollbar" aria-label="เลื่อนดูผลงาน" tabindex="0"><span class="mw-thumb" id="mwThumb"></span></div>'''

    work_en = f' <span class="italic-serif" style="color:#94A6DB">{b["work_heading_en"]}</span>' if b["work_heading_en"] else ""

    head = HEAD.replace("Varinpat Clinic — Case Study | CYN Medical", f'{b["name"]} — Case Study | CYN Medical')
    head = re.sub(r'<meta name="description"[^>]*>',
                  f'<meta name="description" content="{b["name"]} — {b["desc"]}">', head)

    page = f'''{head}<body class="antialiased">

    {HEADER}

    <!-- HERO -->
    <section class="hero-banner">
        {hero_vids}
        <div class="hero-scrim"></div>
        <div class="hero-content">
            <div class="max-w-[1400px] mx-auto px-6 lg:px-10 pb-16 w-full">
                <nav class="flex items-center gap-2 text-[11px] tracking-[0.15em] uppercase text-white/55 mb-6">
                    <a href="/work.html" class="hover:text-white transition">Work</a>
                    <span class="text-white/30">/</span>
                    <span class="text-white/85">{b["name"].split(" Clinic")[0].split(" Dental")[0]}</span>
                </nav>
                <div class="label text-royal-300 mb-5">{b["label"]}</div>
                <h1 class="font-display text-5xl md:text-6xl lg:text-7xl leading-[1.05] tracking-[-0.02em] text-white"><span class="italic-serif" style="color:#94A6DB">{name_first}</span> {name_rest}</h1>
                <p class="mt-5 text-white/65 max-w-md text-[15px] leading-relaxed">{b["desc"]}</p>
                <div class="hero-stats">{PH}
                    <span class="hero-stat-num">{b["stat_num"]}</span><span class="txt">{b["stat_txt"]}</span>
                    <span class="sep">·</span><span class="txt">{b["stat_2"]}</span>
                </div>
            </div>
        </div>
    </section>

    <!-- THE WORK -->
    <section class="bg-ink-900 sec sec-tight-b overflow-hidden">
        <div class="max-w-[1400px] mx-auto px-6 lg:px-10 flex items-end justify-between mb-12 reveal">
            <div>
                <div class="label mb-5" style="color:#94A6DB">Selected Work</div>
                <h2 class="font-display text-4xl lg:text-5xl text-white leading-tight tracking-tight">{b["work_heading_th"]}<span class="accent-th" style="color:#94A6DB">{b["work_heading_accent"]}</span>{work_en}</h2>
            </div>
            <span class="hidden md:block label" style="color:rgba(148,166,219,.32)">{n} Reels · Content</span>
        </div>
        <div class="marquee reveal-clip">
            <div class="marquee-track">
                {marquee}
            </div>
        </div>
    </section>

    <!-- RESULTS -->
    <section class="sec bg-white">
        <div class="max-w-[1000px] mx-auto px-6 lg:px-10">
            <div class="reveal" style="margin-bottom:clamp(2.5rem,4vw,3.75rem)">
                <div class="label text-cobalt mb-6">Results</div>
                <h2 class="font-display text-4xl lg:text-5xl text-ink-800 leading-tight tracking-tight">ตัวเลขที่<span class="accent-th text-cobalt"> พูดแทนทุกอย่าง</span></h2>
            </div>
            <div class="reveal reveal-d1">{PH}
                {results}
            </div>
            <p class="mt-16 text-xs text-ink-300 reveal" style="letter-spacing:.04em">ที่มา: Meta &amp; TikTok Analytics · เทียบช่วงก่อน–หลังเริ่มงาน</p>
        </div>
    </section>

    <!-- APPROACH -->
    <section class="sec sec-feature" style="background:#F9F8F6">
        <div class="max-w-[1400px] mx-auto px-6 lg:px-10">
            <div class="grid lg:grid-cols-12 gap-12 lg:gap-16 items-center">
                <div class="lg:col-span-7 reveal">
                    <div class="label text-cobalt mb-6">The Approach</div>
                    <h2 class="font-display text-3xl lg:text-4xl text-ink-800 leading-snug tracking-tight">{b["desc"]}</h2>
                    <div class="ba-grid mt-10">
                        <div class="ba-card ba-before">
                            <div class="ba-head"><span class="ba-dot"></span><span class="ba-tag">เดิม</span><span class="ba-en">Before</span></div>
                            <p class="ba-text">{b["before"]}</p>
                        </div>
                        <div class="ba-arrow" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M5 12h14M13 5l7 7-7 7"/></svg></div>
                        <div class="ba-arrow-m" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M5 12h14M13 5l7 7-7 7"/></svg></div>
                        <div class="ba-card ba-after">
                            <div class="ba-head"><span class="ba-dot"></span><span class="ba-tag">ตอนนี้</span><span class="ba-en">After</span></div>
                            <p class="ba-text">{b["after"]}</p>
                        </div>
                    </div>
                    <div class="flex flex-wrap gap-2.5 mt-8">
                        {chips}
                    </div>
                    <div class="approach-meta mt-10 pt-8 border-t border-ink-200">
                        <div><div class="label">Client</div><div class="text-ink-700">{b["name"]}</div></div>
                        <div><div class="label">Services</div><div class="text-ink-700">Content · Ads</div></div>
                    </div>
                </div>
                <div class="lg:col-span-5 reveal reveal-d1">
                    <div class="approach-carousel">
                        <div class="ac-stage">
                            <div class="ac-track" id="approachCarousel">
                            {carousel}
                            </div>
                        </div>
                        <div class="ac-nav">
                            <span class="ac-count"><b id="acCur">1</b> / {n}</span>
                            <div class="scroll-arrows">
                                <button type="button" class="scroll-arrow" data-ac="-1" aria-label="คลิปก่อนหน้า"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M11 19l-7-7 7-7"/></svg></button>
                                <button type="button" class="scroll-arrow" data-ac="1" aria-label="คลิปถัดไป"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 5l7 7-7 7"/></svg></button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    {TRUSTED}

    <!-- MORE WORK -->
    <section class="sec" style="background:#F9F8F6">
        <div class="max-w-[1400px] mx-auto px-6 lg:px-10">
            <div class="flex items-end justify-between mb-12 reveal">
                <div>
                    <div class="label text-cobalt mb-4">More Work</div>
                    <h2 class="font-display text-4xl lg:text-5xl text-ink-800 tracking-tight">ผลงานคลินิก<span class="accent-th text-cobalt"> อื่นๆ</span></h2>
                </div>
                <div class="scroll-arrows hidden sm:flex">
                    <button type="button" class="scroll-arrow" data-dir="-1" aria-label="เลื่อนซ้าย"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M11 19l-7-7 7-7"/></svg></button>
                    <button type="button" class="scroll-arrow" data-dir="1" aria-label="เลื่อนขวา"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 5l7 7-7 7"/></svg></button>
                </div>
            </div>
            {morework_inner}
            <a href="/work.html" class="pill-btn pill-outline text-[12px] inline-flex mt-10">ดูผลงานทั้งหมด<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
        </div>
    </section>

    <!-- CTA -->
    <section class="bg-ink-900 text-white relative overflow-hidden">
        <div class="cta-glow"></div>
        <div class="relative max-w-[1400px] mx-auto px-6 lg:px-10 sec">
            <div class="grid lg:grid-cols-12 gap-8 items-center relative z-10 reveal">
                <div class="lg:col-span-7">
                    <div class="label mb-6" style="color:#94A6DB">Let's talk</div>
                    <h2 class="font-display text-4xl md:text-5xl lg:text-6xl leading-[1.08] tracking-[-0.02em] text-white">คุยกันสบายๆ<br/><span class="accent-th" style="color:#94A6DB">ก่อนตัดสินใจ</span></h2>
                    <p class="mt-6 text-white/55 max-w-md leading-relaxed">ทักมาปรึกษาได้เลย ไม่มีค่าใช้จ่าย ไม่มีข้อผูกมัด — เรายินดีช่วยดูทิศทางคอนเทนต์และโฆษณาของคลินิกคุณให้ก่อน</p>
                </div>
                <div class="lg:col-span-5 flex lg:justify-end gap-4 flex-wrap">
                    <a href="https://line.me/R/ti/p/@139yrwpi" target="_blank" rel="noopener" class="pill-btn pill-line text-[13px]"><svg width="20" height="20" viewBox="0 0 24 24" fill="#FFF"><path d="M12 2C6.48 2 2 5.64 2 10.13c0 4.02 3.55 7.39 8.34 8.03.33.07.77.22.88.5.1.26.07.66.03.92l-.14.86c-.04.26-.2 1.02.9.56 1.1-.46 5.93-3.49 8.09-5.98 1.49-1.63 2-3.3 2-5.85C24 5.64 17.52 2 12 2z"/></svg>ปรึกษาฟรี</a>
                    <a href="/contact.html" class="pill-btn pill-outline-light text-[13px]">Contact Us</a>
                </div>
            </div>
        </div>
    </section>

    {FOOTER}

    {SCRIPT}
</body>
</html>
'''
    out = f"{ROOT}/work/{slug}.html"
    open(out, "w", encoding="utf-8").write(page)
    print(f"wrote {out}  ({n} reels, {len(showcase_cards(slug, cat))} showcase cards)")

if __name__ == "__main__":
    for slug in sys.argv[1:]:
        build(slug)
