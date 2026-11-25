# -*- coding: utf-8 -*-
# Builds every service page (dental-marketing.html, dental-video-marketing.html, ...) from index.html's shared parts
# (the same <style>, header, mobile menu, footer, review cards and motion code) plus the service-page sections.
# Layout, photos, video, fonts, sizes and spacing come from this one template; each page's TEXT comes from
# services_content.py (next to this file). Run from the repo root:  python .claude/skills/dmc-design/build_service.py
import re, json, os, html
import sys as _sys, os as _os
_sys.dont_write_bytecode = True
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import preloader  # the home page's preloader on every page
_here = os.path.dirname(os.path.abspath(__file__))
_ns = {}
exec(open(os.path.join(_here, 'services_content.py'), encoding='utf-8').read(), _ns)
SERVICES = _ns['SERVICES']

src = open('index.html', 'rb').read().decode('utf-8').replace('\r\n', '\n')

def between(a, b, s=src):
    i = s.index(a); j = s.index(b, i)
    return s[i:j + len(b)]

style = between('    <style>', '    </style>')
header = between('    <header class="top" id="top">', '    </header>')
mnav = between('    <div class="mnav" id="mnav"', '      </div>\n    </div>\n')
footer = between('    <footer class="foot">', '    </footer>')
symbols = between('    <svg width="0" height="0"', '    </svg>')
cases = between('        <!-- Elementor: Loop Carousel over the "Case Study" CPT', '<p class="note">Individual campaign examples. Results vary by clinic, market, and treatment offering.</p>')
# the hero's review cards (the row, its cards and play buttons) and the video lightbox they open
_q0 = src.index('        <div class="q-row" id="qRow">')
_q1 = src.index('        </div>\n        </div>\n      </section>', _q0) + len('        </div>\n')
reviews = src[_q0:_q1]
vbox = between('    <div class="vbox" id="vbox"', '    </div>\n')
# the scripts: --qs (cards keep their share of the screen) and the drift / drag / lightbox
fitq_js = between('        /* ---------- reviews: the cards keep their share of the SCREEN', '        addEventListener("resize", fitQ);')
drift_js = between('        /* ---------- testimonials: glass cards drift, drag to scrub ---------- */', '          qRow.addEventListener("pointercancel", end);\n        }')
meth = between('          <!-- Elementor: two columns. Left: the hero mark (sticky).', '          </div>\n        </div>\n      </section>')
meth = meth[: meth.rindex('        </div>\n      </section>')]

HOME = 'index.html'
SVC_FILE = {sv['svc']: sv['file'] for sv in SERVICES}
def relink(h):
    # every service links to its own page; the treatment links open Dental Marketing; other sections go to the home page
    for k, f in SVC_FILE.items():
        h = h.replace(f'href="#{k}"', f'href="{f}"')
    h = h.replace('href="#treatments"', 'href="dental-marketing.html"')
    h = re.sub(r'href="#(svc-[a-z]+|services|results|testimonials|dmc|faq|contact|about)"',
               lambda m: f'href="{HOME}#{m.group(1)}"', h)
    h = h.replace('href="#main"', f'href="{HOME}"')
    return h
header, mnav, footer = relink(header), relink(mnav), relink(footer)
# on this page the nav's "Case Studies", "DMC Method" and "FAQ" have their own sections here
for k in ('faq', 'testimonials'):
    header = header.replace(f'href="{HOME}#{k}"', f'href="#{k}"')
    mnav = mnav.replace(f'href="{HOME}#{k}"', f'href="#{k}"')
header = header.replace('<a class="dd-t" href="index.html#services"', '<a class="dd-t is-cur" href="index.html#services"')

# ---------------- per-page content helpers (text comes from services_content.py) ----------------
def faq_html(FAQ):
    out = []
    for i, (q, ps) in enumerate(FAQ, 1):
        n = f'{i:02d}'
        body = ''.join(f'<p>{p}</p>' for p in ps)
        out.append(f'''            <div class="fq">
              <h3><button class="fq-q" type="button" id="fqq{n}" aria-expanded="false" aria-controls="fqa{n}"><span class="fq-n">{n}</span><span class="fq-t">{q}</span><span class="fq-i" aria-hidden="true"><i class="ph ph-plus"></i></span></button></h3>
              <div class="fq-a" id="fqa{n}" role="region" aria-labelledby="fqq{n}"><div class="fq-in">{body}</div></div>
            </div>''')
    return '\n'.join(out)

def help_html(HELP):
    return '\n'.join(f'''            <article class="hp"><h3><span class="hp-i" aria-hidden="true"><i class="ph-fill {ic}"></i></span>{t}</h3><p>{p}</p></article>''' for ic, t, p in HELP)

def hero_img(sv):
    img = (f'<img src="assets/img/svc/{sv['photo']}" alt="{sv['photo_alt']}" width="3840" height="2560" '
           f'style="--pos: {sv['photo_pos']}; --pos-m: {sv['photo_pos_m']}" fetchpriority="high" decoding="async" />')
    if sv.get('photo_m'):  # a separate phone version: a banner-shaped desktop image would lose its subject on a tall phone crop
        return f'<picture><source media="(max-width: 899px)" srcset="assets/img/svc/{sv['photo_m']}" />{img}</picture>'
    return img

def ck_html(items):
    return '\n'.join(f'                  <li><i class="ph-bold ph-check" aria-hidden="true"></i>{t}</li>' for t in items)

def plain(t):
    return html.unescape(re.sub(r'<[^>]+>', '', t)).replace('’', "'")

def ld_txt(sv):
    url = f"https://dentalmediacorp.com/{sv['slug']}/"
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Service", "name": plain(sv['name']), "serviceType": plain(sv['name']), "url": url,
             "description": plain(sv['desc']),
             "provider": {"@type": "ProfessionalService", "name": "Dental Media Corp", "url": "https://dentalmediacorp.com/"},
             "areaServed": {"@type": "Country", "name": "Canada"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://dentalmediacorp.com/"},
                {"@type": "ListItem", "position": 2, "name": "Services", "item": "https://dentalmediacorp.com/#services"},
                {"@type": "ListItem", "position": 3, "name": plain(sv['name']), "item": url}]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(" ".join(ps))}} for q, ps in sv['faq']]},
        ],
    }
    return json.dumps(ld, ensure_ascii=False, indent=2).replace('\n', '\n      ')

CTA = ('<a class="cta mag" href="index.html#contact"><span class="cta-t">Book a Strategy Call</span><span class="cta-i">'
       '<i class="ph ph-arrow-right" aria-hidden="true"></i><i class="ph ph-arrow-right" aria-hidden="true"></i></span></a>')

PAGE_CSS = """
      /* ================= service page (template: dental-marketing.html; the other six reuse it) =================
         Built only from the home page's vocabulary: section heads, the CTA pill, white cards with mint chips, a hairline
         list, the services carousel's glyph panel, case studies, the DMC Method and the FAQ. Shared CSS above is a copy of
         index.html's; page-only rules live here. */
      .dd-t.is-cur {
        color: var(--teal);
      }
      /* ---------- service hero (inspo: madebyshape.co.uk SEO page, in our light theme) ----------
         Row 1: a dot label and the H1 on the left, two short paragraphs on the right.
         Row 2: one wide photo; a small CTA sits in a notch cut out of its top-left corner (a clip-path the script
         draws, so the notch follows the button's real size), a glass panel holds the numbers.
         Row 3 (#more): the statement and the CTA on the left, a checklist on the right. */
      .svh {
        position: relative;
        --fs-h1: clamp(38px, calc(4.2 * var(--uvw)), 68px); /* the home hero's size */
        padding: clamp(118px, calc(16 * var(--uvh)), 150px) 0 var(--sec-y); /* every section ends with --sec-y, as on the home page */
        background: radial-gradient(30% 26% at 84% 12%, rgba(255, 191, 215, 0.34), transparent 70%);
      }
      .svh-in {
        max-width: var(--max);
        margin-inline: auto;
      }
      .svh-top {
        display: grid;
        grid-template-columns: minmax(0, 7fr) minmax(0, 5fr);
        gap: 40px clamp(40px, calc(6 * var(--uvw)), 120px);
        align-items: start;
      }
      /* the small label with a pink dot (row 1 and row 3) */
      .eyb {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: var(--fs-small);
        font-weight: 500;
        color: var(--ink);
      }
      .eyb::before {
        content: "";
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--acc-mid);
      }
      .svh-top .eyb {
        margin-bottom: 22px;
      }
      .svh-txt {
        padding-top: calc(var(--fs-small) * 1.4 + 22px); /* level with the H1, under the label */
      }
      /* the same as the home hero's subline (.h-side p): lead size, 1.45, grey */
      .svh-txt p {
        font-size: var(--fs-lead);
        line-height: 1.45;
        color: var(--grey);
      }
      .svh-txt p + p {
        margin-top: 18px;
      }
      /* row 2: the banner */
      .svb-w {
        position: relative;
        margin-top: clamp(48px, calc(5 * var(--uvw)), 80px);
      }
      .svb {
        position: relative;
        height: clamp(300px, calc(26 * var(--uvw)), 500px);
        border-radius: var(--r-card);
        overflow: hidden;
        background: var(--soft);
      }
      .svb-img {
        position: absolute;
        inset: 0;
        overflow: hidden;
      }
      .svb-img picture {
        display: contents; /* the img inside lays out exactly as a plain img does */
      }
      .svb-img img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: var(--pos, 50% 40%); /* each page's focus point (services_content.py: photo_pos) */
      }
      .svb-tab {
        position: absolute;
        top: 0;
        left: 0;
        z-index: 2;
      }
      /* every button on the page is the home page's CTA as it is: same height, its width follows its text */
      /* the numbers: the home hero's stats panel (.h-stat: glass, two figures with the pink highlighter, a hairline
         between them), placed on the photo's quiet side */
      .svb-stat {
        position: absolute;
        left: 24px;
        bottom: 24px;
        z-index: 1;
      }
      /* row 3 (#more): the statement and its CTA on the left, the checklist on the right (no label: user request) */
      .svs {
        display: grid;
        grid-template-columns: minmax(0, 8fr) minmax(0, 4fr);
        gap: 48px clamp(40px, calc(6 * var(--uvw)), 120px);
        align-items: start;
        padding-top: var(--sec-y);
      }
      .svs-q {
        font-size: var(--fs-h2); /* the home section headings' size */
        font-weight: 700;
        letter-spacing: -0.035em;
        line-height: 1.09;
      }
      .svs-q .hl {
        line-height: 1;
      }
      .svs-l .cta {
        margin-top: 36px;
      }
      .ck-cap {
        font-size: var(--fs-small);
        color: var(--grey);
      }
      .ck {
        display: grid;
        gap: 16px;
        margin: 20px 0 0;
        padding: 0;
        list-style: none;
      }
      .ck li {
        display: flex;
        align-items: center;
        gap: 14px;
        font-size: var(--fs-lead); /* the hero text size (user request) */
        line-height: 1.45;
        font-weight: 500;
      }
      /* the tick circle: the How we help tile's green, a black tick (user request) */
      .ck i {
        display: grid;
        flex: none;
        place-items: center;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: var(--teal-3);
        color: var(--ink);
        font-size: 16px;
      }

      /* what we handle (inspo: madebyshape.co.uk): a left-aligned head with the dot label and a small CTA on the right,
         then a 3-column grid; each item has a mint icon tile, a title and one line, and a hairline under it that turns
         teal on hover (the tile turns pink, like the FAQ icon) */
      .help {
        padding: var(--sec-y) 0;
      }
      .help-in {
        max-width: var(--max);
        margin-inline: auto;
      }
      .help-hd {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 32px;
      }
      .help-hd .eyb {
        margin-bottom: 20px;
      }
      .hp-g {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        column-gap: clamp(24px, calc(2.4 * var(--uvw)), 48px);
        margin-top: var(--sec-head);
      }
      .hp {
        position: relative;
        padding: clamp(40px, calc(7 * var(--uvh)), 64px) 0;
        border-bottom: 1px solid rgba(13, 19, 18, 0.1);
      }
      .hp::after {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        bottom: -1px;
        height: 1px;
        background: var(--teal);
        transform: scaleX(0);
        transform-origin: right;
        transition: transform 0.6s var(--ease);
      }
      .hp:hover::after {
        transform: scaleX(1);
        transform-origin: left;
      }
      /* the DMC Method's sizes (user request): the tile is as tall as a step number (--fs-stat), the title is a step
         title (--fs-list), the line is the step text (--fs-lead, 1.45, --body). Icons: Phosphor Fill (solid, modern; duotone read as thin outlines on the green tile). */
      .hp-i {
        display: grid;
        flex: none;
        place-items: center;
        width: var(--fs-stat);
        height: var(--fs-stat);
        border-radius: calc(var(--fs-stat) * 0.24); /* crisp rounded square (user: 38% was too round) */
        background: var(--teal-3);
        color: var(--ink);
        font-size: calc(var(--fs-stat) * 0.56);
      }
      .hp h3 {
        display: flex;
        align-items: center;
        gap: clamp(14px, calc(1.2 * var(--uvw)), 22px);
        font-size: var(--fs-list);
        font-weight: 600;
        letter-spacing: -0.035em;
        line-height: 1.09;
      }
      .hp p {
        max-width: 34rem;
        margin-top: 14px;
        font-size: var(--fs-lead); /* the same as the hero text (.svh-txt p) */
        line-height: 1.45;
        color: var(--grey);
      }

      /* client video (inspo: madebyshape.co.uk): one wide card on the content width, the still fills it. The quote is set
         on black label boxes (one per line, box-decoration-break), the name chip under it, the home reviews' white play
         circle (bigger) bottom-left, and the two buttons in a notch cut from the bottom-right corner (the script draws it,
         like the hero banner's). Playing swaps the still for the YouTube player and the card opens to 16:9. */
      .vt {
        padding: 0 0 var(--sec-y); /* no space of its own on top: it follows How we help directly (user request) */
      }
      .vt-in {
        max-width: var(--max);
        margin-inline: auto;
      }
      .vt-w {
        position: relative;
      }
      .vt-box {
        position: relative;
        scroll-margin-top: 96px; /* when the video starts, the card scrolls to just under the header */
        height: clamp(420px, calc(34 * var(--uvw)), 640px);
        border-radius: var(--r-card);
        overflow: hidden;
        background: var(--ink);
      }
      .vt-media {
        position: absolute;
        inset: 0;
        overflow: hidden;
      }
      .vt-media img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: 50% 22%;
      }
      .vt-media iframe {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        border: 0;
        background: var(--ink);
      }
      .vt-say {
        position: absolute;
        top: 32px;
        left: 32px;
        z-index: 1;
        max-width: min(760px, calc(100% - 64px));
        margin: 0;
      }
      .vt-q {
        margin: 0;
        font-size: var(--fs-list);
        font-weight: 600;
        letter-spacing: -0.035em;
        line-height: 1.24;
      }
      .vt-q span {
        padding: 0.06em 0.32em;
        border-radius: 14px;
        background: var(--ink);
        color: #fff;
        -webkit-box-decoration-break: clone;
        box-decoration-break: clone;
      }
      .vt-q i {
        margin-right: 0.3em;
        font-size: 0.7em;
        vertical-align: 0.12em;
        color: var(--acc);
      }
      /* the home reviews' play circle, bigger */
      .vt-play {
        position: absolute;
        left: 32px;
        bottom: 32px;
        z-index: 1;
        display: grid;
        place-items: center;
        width: 76px;
        height: 76px;
        border-radius: 50%;
        background: #fff;
        color: var(--ink);
        font-size: 24px;
        box-shadow: 0 14px 30px -12px rgba(13, 19, 18, 0.5);
        transition:
          transform 0.4s var(--ease),
          background-color 0.3s,
          color 0.3s;
      }
      .vt-play:hover {
        transform: scale(1.1);
        background: var(--ink);
        color: #fff;
      }
      .vt-say,
      .vt-play {
        transition:
          opacity 0.5s var(--ease),
          transform 0.4s var(--ease),
          background-color 0.3s,
          color 0.3s;
      }
      .vt.is-on .vt-say,
      .vt.is-on .vt-play {
        opacity: 0;
        pointer-events: none;
      }
      .vt-tab {
        position: absolute;
        right: 0;
        bottom: 0;
        z-index: 2;
        display: flex;
        gap: 10px;
      }
      .vt-tab .cta {
        border: 0;
        font-family: inherit;
        cursor: pointer;
      }
      /* while the video plays it is just the video (user request): the buttons and the notch go away (the script
         drops the clip), and a small white circle with an x, the play circle's style, closes it from the top-left */
      .vt.is-on .vt-tab {
        display: none;
      }
      .vt-x {
        position: absolute;
        top: 20px;
        left: 20px; /* top-left: the Drive player keeps its own button in the top-right corner */
        z-index: 3;
        display: grid;
        place-items: center;
        width: 52px;
        height: 52px;
        border: 0;
        border-radius: 50%;
        background: #fff;
        color: var(--ink);
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 14px 30px -12px rgba(13, 19, 18, 0.5);
        opacity: 0;
        pointer-events: none;
        transform: scale(0.8);
        transition:
          opacity 0.4s var(--ease),
          transform 0.4s var(--ease),
          background-color 0.3s,
          color 0.3s;
      }
      .vt.is-on .vt-x {
        opacity: 1;
        pointer-events: auto;
        transform: none;
        transition-delay: 0.5s, 0.5s, 0s, 0s; /* after the card has opened */
      }
      .vt.is-on .vt-x:hover {
        transform: scale(1.1);
        background: var(--ink);
        color: #fff;
        transition-delay: 0s;
      }
      .vt-tab .cta.light {
        box-shadow: inset 0 0 0 1px rgba(13, 19, 18, 0.08);
      }

      /* reviews: the home hero's cards and drift, under a centred section head; the cards sit on a soft glow (they are
         glass) and the row runs to the screen edge like on the home page */
      .rvw {
        position: relative;
        padding: var(--sec-y) 0;
      }
      .rvw-row {
        margin-top: var(--sec-head);
      }

      @supports (corner-shape: squircle) {
        .svb,
        .vt-box,
        .hp-i {
          corner-shape: squircle;
        }
      }
      @media (max-width: 1199px) {
        .svh-top,
        .svs {
          grid-template-columns: 1fr;
        }
        .svh-txt {
          padding-top: 0;
          max-width: 640px;
        }
        .hp-g {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }
      }
      @media (max-width: 899px) {
        /* phones: the headline keeps its two lines; the statement's label sits above it instead of in its indent */
        .svh {
          --fs-h1: clamp(28px, 7.8vw, 38px);
        }
        .svb {
          height: auto;
          aspect-ratio: 4 / 5;
        }
        .svb-img img {
          object-position: var(--pos-m, 50% 50%);
        }
        .svb-stat {
          left: 12px;
          right: 12px;
          bottom: 12px;
        }
        .help-hd {
          flex-direction: column;
          align-items: flex-start;
        }
        .hp-g {
          grid-template-columns: 1fr;
        }
        /* phones: a taller card, the buttons sit under it (no notch) */
        .vt-box {
          height: auto;
          aspect-ratio: 4 / 5;
        }
        .vt-media img {
          object-position: 50% 30%;
        }
        .vt-say {
          top: 14px;
          left: 14px;
          max-width: calc(100% - 28px);
        }
        .vt-q {
          font-size: 22px;
        }
        .vt-x {
          top: 12px;
          left: 12px;
          width: 44px;
          height: 44px;
          font-size: 18px;
        }
        .vt-play {
          left: 14px;
          bottom: 14px;
          width: 60px;
          height: 60px;
          font-size: 20px;
        }
        .vt-tab {
          position: static;
          flex-direction: column;
          margin-top: 12px;
        }
        .vt-tab .cta {
          width: 100%;
          justify-content: space-between; /* full-width buttons on phones: the circle sits at the end */
        }
        .hp {
          padding: 32px 0;
        }
        .hp-i {
          width: 52px;
          height: 52px;
          border-radius: 12px; /* 24%, as on desktop */
          font-size: 29px;
        }
      }
"""
style_out = style.replace('    </style>', PAGE_CSS + '    </style>')

JS = r"""
    <script>
      (() => {
        const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
        const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
        const hasG = !!(window.gsap && window.ScrollTrigger);
        if (hasG) gsap.registerPlugin(ScrollTrigger);
        const $ = (s, r = document) => r.querySelector(s);
        const $$ = (s, r = document) => [...r.querySelectorAll(s)];
        const root = document.documentElement;
        const motion = hasG && !reduce;

        /* ---------- smooth scroll (same as the home page) ---------- */
        let lenis = null;
        if (!reduce && window.Lenis) {
          lenis = new Lenis({ lerp: 0.08, wheelMultiplier: 0.8 });
          if (hasG) {
            lenis.on("scroll", ScrollTrigger.update);
            gsap.ticker.add((t) => lenis.raf(t * 1000));
            gsap.ticker.lagSmoothing(0);
          } else {
            const raf = (t) => (lenis.raf(t), requestAnimationFrame(raf));
            requestAnimationFrame(raf);
          }
        }
        const lock = (on) => {
          if (lenis) on ? lenis.stop() : lenis.start();
          else root.style.overflow = on ? "hidden" : "";
        };
        const goTo = (t) => {
          if (lenis) lenis.scrollTo(t, { duration: 1.4, offset: -90 });
          else t.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
        };
        $$('a[href^="#"]').forEach((a) =>
          a.addEventListener("click", (e) => {
            const id = a.getAttribute("href");
            const t = id.length > 1 && $(id);
            if (!t) return;
            e.preventDefault();
            if (document.activeElement) document.activeElement.blur();
            if (mOpen) closeMnav(() => goTo(t));
            else goTo(t);
          }),
        );

        /* ---------- header ---------- */
        const top = $("#top");
        const stuck = () => top.classList.toggle("is-stuck", scrollY > 30);
        addEventListener("scroll", stuck, { passive: true });
        stuck();

        /* ---------- mobile menu ---------- */
        const mnav = $("#mnav"),
          burger = $(".burger");
        let mOpen = false;
        function openMnav() {
          mOpen = true;
          mnav.hidden = false;
          mnav.classList.add("open");
          burger.setAttribute("aria-expanded", "true");
          lock(true);
          if (motion) {
            gsap.fromTo(mnav, { clipPath: "circle(0% at 92% 5%)" }, { clipPath: "circle(150% at 92% 5%)", duration: 0.9, ease: "expo.inOut" });
            gsap.from($$(".mnav-cap, .mnav-list li, .mnav-rule, .mnav-foot", mnav), { y: 26, opacity: 0, duration: 0.7, ease: "power3.out", stagger: 0.035, delay: 0.25 });
          }
          $(".mnav-x").focus();
        }
        function closeMnav(then) {
          const done = () => {
            mOpen = false;
            mnav.hidden = true;
            mnav.classList.remove("open");
            burger.setAttribute("aria-expanded", "false");
            lock(false);
            if (then) then();
            else burger.focus();
          };
          if (motion) gsap.to(mnav, { clipPath: "circle(0% at 92% 5%)", duration: 0.6, ease: "expo.in", onComplete: done });
          else done();
        }
        burger.addEventListener("click", openMnav);
        $(".mnav-x").addEventListener("click", () => closeMnav());
        {
          const tg = $(".mnav-tg"),
            sub = $("#mnSub");
          tg.addEventListener("click", () => {
            const open = tg.getAttribute("aria-expanded") !== "true";
            tg.setAttribute("aria-expanded", open);
            tg.setAttribute("aria-label", (open ? "Hide" : "Show") + " Dental Marketing treatments");
            sub.hidden = !open;
          });
        }
        addEventListener("keydown", (e) => e.key === "Escape" && mOpen && closeMnav());

        /* ---------- service banner: cut the notch for the button ---------- */
        {
          const box = $("#svb"),
            tab = $(".svb-tab");
          const cut = () => {
            const W = box.offsetWidth,
              H = box.offsetHeight,
              R = parseFloat(getComputedStyle(box).borderTopLeftRadius) || 28,
              r = R, // the notch's curves match the card's corners (user request)
              g = 10,
              tw = tab.offsetWidth + g,
              th = tab.offsetHeight + g;
            box.style.clipPath = `path("M${tw + r},0 H${W - R} A${R},${R} 0 0 1 ${W},${R} V${H - R} A${R},${R} 0 0 1 ${W - R},${H} H${R} A${R},${R} 0 0 1 0,${H - R} V${th + r} A${r},${r} 0 0 1 ${r},${th} H${tw - r} A${r},${r} 0 0 0 ${tw},${th - r} V${r} A${r},${r} 0 0 1 ${tw + r},0 Z")`;
          };
          cut();
          new ResizeObserver(cut).observe(box);
        }

        /* ---------- client video: the bottom-right notch for the buttons, and play in the card ---------- */
        {
          const box = $("#vtBox"),
            tab = $(".vt-tab"),
            sec = box.closest(".vt");
          const cut = () => {
            // no notch while the video plays (just the video) or when the buttons sit under the card (phones)
            if (sec.classList.contains("is-on") || getComputedStyle(tab).position !== "absolute") return void (box.style.clipPath = "");
            const W = box.offsetWidth,
              H = box.offsetHeight,
              R = parseFloat(getComputedStyle(box).borderTopLeftRadius) || 28,
              r = R, // the notch's curves match the card's corners (user request)
              g = Math.round(12 / (parseFloat(getComputedStyle(document.documentElement).zoom) || 1)), // 12px on screen at any laptop zoom (user)
              tw = tab.offsetWidth + g,
              th = tab.offsetHeight + g,
              p = Math.min(tab.offsetHeight / 2 + g, th - r); // concentric with the pill: the gap stays g all the way round
            box.style.clipPath = `path("M${R},0 H${W - R} A${R},${R} 0 0 1 ${W},${R} V${H - th - r} A${r},${r} 0 0 1 ${W - r},${H - th} H${W - tw + p} A${p},${p} 0 0 0 ${W - tw},${H - th + p} V${H - r} A${r},${r} 0 0 1 ${W - tw - r},${H} H${R} A${R},${R} 0 0 1 0,${H - R} V${R} A${R},${R} 0 0 1 ${R},0 Z")`;
          };
          cut();
          new ResizeObserver(cut).observe(box);
          new ResizeObserver(cut).observe(tab);
          const go = $(".vt-go"),
            label = $(".cta-t", go),
            media = $(".vt-media", box),
            still = $("img", media),
            x = $(".vt-x", box);
          let frame = null;
          const play = () => {
            if (frame) return stop();
            sec.classList.add("is-on");
            cut();
            x.tabIndex = 0;
            label.textContent = "Close video";
            go.querySelectorAll(".cta-i i").forEach((i) => (i.className = "ph-bold ph-x"));
            // 16:9, but never taller than the screen (the root zoom turns screen px into CSS px)
            const z = parseFloat(getComputedStyle(root).zoom) || 1;
            const to = Math.max(box.offsetHeight, Math.min((box.offsetWidth * 9) / 16, (innerHeight * 0.86) / z));
            if (motion) gsap.to(box, { height: to, duration: 0.9, ease: "expo.inOut" });
            else box.style.height = to + "px";
            frame = document.createElement("iframe");
            frame.src = box.dataset.embed;
            frame.allow = "autoplay; fullscreen; encrypted-media; picture-in-picture";
            frame.allowFullscreen = true;
            frame.referrerPolicy = "strict-origin-when-cross-origin";
            frame.title = "Service video";
            media.appendChild(frame);
            still.style.opacity = "0";
            x.focus({ preventScroll: true });
            // bring the whole card into view, just under the header (the header would hide the close button)
            if (lenis) lenis.scrollTo(box, { offset: -96, duration: 1.1 });
            else box.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
          };
          const stop = () => {
            frame.remove();
            frame = null;
            still.style.opacity = "";
            sec.classList.remove("is-on");
            x.tabIndex = -1;
            label.textContent = "Play video";
            go.querySelectorAll(".cta-i i").forEach((i) => (i.className = "ph-fill ph-play"));
            // back to the card's own (CSS) height
            const cur = box.style.height;
            box.style.height = "";
            const h = box.offsetHeight;
            box.style.height = cur;
            if (motion) gsap.to(box, { height: h, duration: 0.9, ease: "expo.inOut", clearProps: "height", onComplete: cut });
            else box.style.height = "";
            cut();
            go.focus({ preventScroll: true });
          };
          $(".vt-play").addEventListener("click", play);
          go.addEventListener("click", play);
          x.addEventListener("click", stop);
          addEventListener("keydown", (e) => e.key === "Escape" && frame && stop());
        }

{fitq_js}

{drift_js}

        /* ---------- FAQ: one answer open at a time ---------- */
        {
          root.classList.add("js-fq");
          const items = $$(".fq");
          const setOpen = (f, on, now) => {
            const a = $(".fq-a", f);
            f.classList.toggle("open", on);
            $(".fq-q", f).setAttribute("aria-expanded", on);
            if (motion && !now)
              gsap.to(a, { height: on ? "auto" : 0, duration: on ? 0.6 : 0.4, ease: on ? "expo.out" : "power3.inOut", overwrite: true, onComplete: () => ScrollTrigger.refresh() });
            else a.style.height = on ? "auto" : "0px";
          };
          items.forEach((f) =>
            $(".fq-q", f).addEventListener("click", () => {
              const on = !f.classList.contains("open");
              items.forEach((x) => x !== f && x.classList.contains("open") && setOpen(x, false));
              setOpen(f, on);
            }),
          );
          if (items[0]) setOpen(items[0], true, true);
        }

        /* ---------- magnetic buttons ---------- */
        if (motion && fine)
          $$(".mag").forEach((el) => {
            const xTo = gsap.quickTo(el, "x", { duration: 0.6, ease: "power3" }),
              yTo = gsap.quickTo(el, "y", { duration: 0.6, ease: "power3" });
            el.addEventListener("mousemove", (e) => {
              const r = el.getBoundingClientRect();
              xTo((e.clientX - r.left - r.width / 2) * 0.22);
              yTo((e.clientY - r.top - r.height / 2) * 0.35);
            });
            el.addEventListener("mouseleave", () => (xTo(0), yTo(0)));
          });

        /* ---------- choreography (the home page's values) ---------- */
        if (!motion) return;
        const st = (trigger, start = "top 82%") => ({ trigger, start, once: true });

        // hero: label and headline rise, the paragraphs follow, the banner opens from the middle and its photo settles
        gsap
          .timeline()
          .from(".nav > *", { y: -16, opacity: 0, duration: 0.9, ease: "power3.out", stagger: 0.07 }, 0)
          .from(".svh-top .eyb", { y: 14, opacity: 0, duration: 0.9, ease: "power3.out" }, 0.1)
          .from("#svc-title .ln-m > span", { yPercent: 110, duration: 1.2, ease: "expo.out", stagger: 0.09 }, 0.15)
          .from(".svh-txt p", { y: 18, opacity: 0, duration: 1, ease: "power3.out", stagger: 0.1 }, 0.4)
          .from(".svb", { y: 60, opacity: 0, duration: 1.3, ease: "expo.out" }, 0.45)
          .from(".svb-img img", { scale: 1.25, duration: 1.8, ease: "expo.out" }, 0.45)
          .from([".svb-tab", ".svb-stat"], { y: 16, opacity: 0, duration: 0.9, ease: "power3.out", stagger: 0.1 }, 1);

        gsap.from([".svs-l > *", ".svs > div:last-child > *"], { y: 30, opacity: 0, duration: 1.1, ease: "expo.out", stagger: 0.08, scrollTrigger: st(".svs", "top 86%") });
        $$(".t-h2").forEach((h) => gsap.from($$(".ln-m > span", h), { yPercent: 110, duration: 1.2, ease: "expo.out", stagger: 0.09, scrollTrigger: st(h, "top 86%") }));
        $$(".sh-rule").forEach((r) => gsap.from(r, { scaleX: 0, duration: 1.4, ease: "expo.inOut", scrollTrigger: st(r, "top 90%") }));

        gsap.from([".help-hd .eyb", ".help-hd .cta"], { y: 16, opacity: 0, duration: 0.9, ease: "power3.out", stagger: 0.1, scrollTrigger: st(".help-hd", "top 88%") });
        gsap.set(".hp", { opacity: 0, y: 50 });
        ScrollTrigger.batch(".hp", { start: "top 94%", once: true, onEnter: (b) => gsap.to(b, { opacity: 1, y: 0, duration: 1.1, ease: "expo.out", stagger: 0.08, clearProps: "opacity,transform" }) });

        // client video: the card rises, the still settles, the quote and buttons follow
        gsap.from(".vt-box", { y: 60, opacity: 0, duration: 1.3, ease: "expo.out", scrollTrigger: st(".vt", "top 85%") });
        gsap.from(".vt-media img", { scale: 1.25, duration: 1.8, ease: "expo.out", scrollTrigger: st(".vt", "top 85%") });
        gsap.from([".vt-say", ".vt-play", ".vt-tab"], { y: 20, opacity: 0, duration: 1, ease: "power3.out", stagger: 0.1, delay: 0.4, scrollTrigger: st(".vt", "top 85%"), clearProps: "opacity,transform" });

        gsap.from(".q-track > .q:nth-child(-n+6)", { x: 260, opacity: 0, duration: 1.4, ease: "expo.out", stagger: 0.07, scrollTrigger: st(".rvw-row", "top 88%") });
        gsap.set(".fq", { opacity: 0, y: 30 });
        ScrollTrigger.batch(".fq", { start: "top 94%", once: true, onEnter: (bt) => gsap.to(bt, { opacity: 1, y: 0, duration: 0.9, ease: "power3.out", stagger: 0.06 }) });
        gsap.from(".f-g > *", { y: 30, opacity: 0, duration: 1.1, ease: "power3.out", stagger: 0.1, scrollTrigger: st(".foot", "top 85%") });

        addEventListener("load", () => ScrollTrigger.refresh());
      })();
    </script>"""

JS = JS.replace('{fitq_js}', fitq_js).replace('{drift_js}', drift_js)
head_links = between('    <link rel="icon"', '/src/fill/style.css"\n    />')

def render(sv):
    url = f"https://dentalmediacorp.com/{sv['slug']}/"
    return f'''<!doctype html>
<html lang="en-CA">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{sv['title']}</title>
    <meta
      name="description"
      content="{sv['desc']}"
    />
    <link rel="canonical" href="{url}" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <meta name="theme-color" content="#0F1716" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Dental Media Corp" />
    <meta property="og:title" content="{sv['name']} | Dental Media Corp" />
    <meta property="og:description" content="{sv['desc']}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:locale" content="en_CA" />
    <meta name="twitter:card" content="summary_large_image" />
{head_links}
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/bold/style.css" />

    <script type="application/ld+json">
      {ld_txt(sv)}
    </script>
{style_out}
  </head>
  <body>
    <a class="skip" href="#main">Skip to content</a>
{symbols}

    <!-- ============ HEADER (Elementor: Theme Builder > Header, shared with the home page) ============ -->
{header}

    <!-- ============ MOBILE MENU ============ -->
{mnav}
    <main id="main">
      <!-- ============ 1. SERVICE HERO (inspo: madebyshape.co.uk, our light theme) ============
           Elementor: Single "Service" template. Row 1: label, H1 | two paragraphs (ACF: label, headline, intro x2).
           Row 2: banner (ACF: photo) with the notch button and the glass numbers. Row 3: statement + CTA | checklist (Repeater). -->
      <section class="svh" aria-labelledby="svc-title">
        <div class="wrap">
          <div class="svh-in">
            <div class="svh-top">
              <div>
                <p class="eyb">{sv['name']}</p>
                <h1 class="t-h1" id="svc-title">
                  <span class="ln-m"><span>{sv['h1a']}</span></span>
                  <span class="ln-m"><span>{sv['h1b']}</span></span>
                </h1>
              </div>
              <div class="svh-txt">
                <p>{sv['p1']}</p>
                <p>{sv['p2']}</p>
              </div>
            </div>
            <div class="svb-w">
            <div class="svb" id="svb">
              <div class="svb-img">{hero_img(sv)}</div>
              <div class="h-stat svb-stat">
                <div class="h-num"><b><em>5,000+</em></b><small>Consultations attended</small></div>
                <div class="h-num"><b><em>$10M+</em></b><small>In accepted treatment</small></div>
              </div>
            </div>
              <!-- the button sits outside the clipped banner, in the notch the script cuts for it -->
            <div class="svb-tab"><a class="cta" href="#more"><span class="cta-t">Tell me more</span><span class="cta-i"><i class="ph ph-arrow-right" aria-hidden="true"></i><i class="ph ph-arrow-right" aria-hidden="true"></i></span></a></div>
            </div>
            <div class="svs" id="more">
              <div class="svs-l">
                <p class="svs-q">{sv['statement']}</p>
                {CTA}
              </div>
              <div>
                <p class="ck-cap">What we handle for you</p>
                <ul class="ck">
{ck_html(sv['checklist'])}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div class="sbreak" aria-hidden="true"></div>

      <!-- ============ 2. WHAT WE HANDLE (inspo: madebyshape.co.uk "What we can help you with")
           Elementor: Container. Head: label, H2 | small CTA. Then a Repeater (icon, title, text) in a 3-column grid with hairlines. -->
      <section class="help" id="help" aria-labelledby="help-title">
        <div class="wrap">
          <div class="help-in">
            <div class="help-hd">
              <div>
                <p class="eyb">How we help</p>
                <h2 class="t-h2" id="help-title">
                  <span class="ln-m"><span>One complete team,</span></span>
                  <span class="ln-m"><span>working for <span class="hl">your clinic.</span></span></span>
                </h2>
              </div>
              <a class="cta mag" href="index.html#contact"><span class="cta-t">Book a Strategy Call</span><span class="cta-i"><i class="ph ph-arrow-right" aria-hidden="true"></i><i class="ph ph-arrow-right" aria-hidden="true"></i></span></a>
            </div>
            <div class="hp-g">
{help_html(sv['help'])}
            </div>
          </div>
        </div>
      </section>

      <!-- ============ 3. CLIENT VIDEO (inspo: madebyshape.co.uk testimonial card)
           Elementor: Container + HTML widget. ACF: video embed URL (data-embed: Google Drive /preview, shared as "anyone
           with the link"; a YouTube or Vimeo embed URL works the same), cover still, headline.
           The quote sits on black label boxes top-left, the play circle bottom-left; "Play video" and "View all
           testimonials" sit in a notch cut out of the bottom-right corner. A click plays the video inside the card. -->
      <section class="vt" aria-label="Client video">
        <div class="wrap">
          <div class="vt-in">
            <div class="vt-w">
              <div class="vt-box" id="vtBox" data-embed="https://drive.google.com/file/d/13MqhWz0r0u-TySTFtp3yZwiZIhq83WXe/preview">
                <div class="vt-media"><img src="assets/img/svc/marketing-video.webp" alt="A Dental Media Corp presenter inside a dental clinic" width="2880" height="1620" loading="lazy" decoding="async" /></div>
                <div class="vt-say">
                  <p class="vt-q"><span>{sv['video']}</span></p>
                </div>
                <button class="vt-play" type="button" aria-label="Play the {sv['name']} video"><i class="ph-fill ph-play" aria-hidden="true"></i></button>
                <button class="vt-x" type="button" aria-label="Close the video" tabindex="-1"><i class="ph-bold ph-x" aria-hidden="true"></i></button>
              </div>
              <div class="vt-tab">
                <button class="cta vt-go" type="button"><span class="cta-t">Play video</span><span class="cta-i"><i class="ph-fill ph-play" aria-hidden="true"></i><i class="ph-fill ph-play" aria-hidden="true"></i></span></button>
                <a class="cta light" href="#testimonials"><span class="cta-t">View all testimonials</span><span class="cta-i"><i class="ph ph-arrow-right" aria-hidden="true"></i><i class="ph ph-arrow-right" aria-hidden="true"></i></span></a>
              </div>
            </div>
          </div>
        </div>
      </section>


      <div class="sbreak" aria-hidden="true"></div>

      <!-- ============ 5. REVIEWS (the home hero's moving cards: same markup, same script)
           Elementor: Loop Carousel over the "Testimonial" CPT, as on the home page. -->
      <section class="rvw" id="testimonials" aria-labelledby="rvw-title">
        <div class="wrap">
          <div class="sh">
            <h2 class="t-h2" id="rvw-title">
              <span class="ln-m"><span>What dentists say</span></span>
              <span class="sh-l2"><span class="sh-rule" aria-hidden="true"></span><span class="ln-m"><span class="hl">about working with us.</span></span></span>
            </h2>
          </div>
        </div>
        <div class="rvw-row">
{reviews}        </div>
      </section>

      <div class="sbreak" aria-hidden="true"></div>

      <!-- ============ 6. FAQ (keep in sync with the FAQPage JSON-LD in <head>) ============ -->
      <section class="faq" id="faq" aria-labelledby="faq-title">
        <div class="wrap">
          <div class="sh">
            <h2 class="t-h2" id="faq-title">
              <span class="ln-m"><span>{sv['faq_head']}</span></span>
              <span class="sh-l2"><span class="sh-rule" aria-hidden="true"></span><span class="ln-m"><span class="hl">answered.</span></span></span>
            </h2>
          </div>
          <div class="fq-list">
{faq_html(sv['faq'])}
          </div>
        </div>
      </section>

    </main>

    <!-- video lightbox: the review cards' play buttons fill it with a YouTube embed -->
{vbox}
    <div class="sbreak" aria-hidden="true"></div>
    <!-- ============ FOOTER (shared with the home page) ============ -->
{footer}

    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>{JS}
  </body>
</html>
'''
if __name__ == '__main__':  # build_case.py imports this file for its parts; only a direct run writes the pages
    for sv in SERVICES:
        page = render(sv)
        page = preloader.inject(page)
        open(sv['file'], 'wb').write(page.replace('\n', '\r\n').encode('utf-8'))
        print('ok', sv['file'], len(page.splitlines()))
