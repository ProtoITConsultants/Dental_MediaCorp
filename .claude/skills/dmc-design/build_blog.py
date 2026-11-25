# -*- coding: utf-8 -*-
# Builds blog.html (the blog listing) from index.html's shared parts: the same <style>, header, mobile menu and footer,
# plus the blog head, topic filter and post cards. Layout after madebyshape.co.uk/web-design-blog (filter tabs, a grid of
# cards with the author avatar in a notch and an arrow circle that pops on hover), built from our own components: the
# cards are the home page's "Real clinics" white cards. Posts live in POSTS below. Run from the repo root:
#   python .claude/skills/dmc-design/build_blog.py
import re, os, html, json
import sys as _sys, os as _os
_sys.dont_write_bytecode = True
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import preloader  # the home page's preloader on every page

src = open('index.html', 'rb').read().decode('utf-8').replace('\r\n', '\n')

def between(a, b, s=src):
    i = s.index(a); j = s.index(b, i)
    return s[i:j + len(b)]

style = between('    <style>', '    </style>')
header = between('    <header class="top" id="top">', '    </header>')
mnav = between('    <div class="mnav" id="mnav"', '      </div>\n    </div>\n')
footer = between('    <footer class="foot">', '    </footer>')
head_links = between('    <link rel="icon"', '/src/fill/style.css"\n    />')

HOME = 'index.html'
def relink(h):
    h = h.replace('href="#treatments"', 'href="dental-marketing.html"')
    h = re.sub(r'href="#(svc-[a-z]+|services|results|testimonials|dmc|faq|contact|about)"', lambda m: f'href="{HOME}#{m.group(1)}"', h)
    h = h.replace('href="#main"', f'href="{HOME}"')
    return h
header, mnav, footer = relink(header), relink(mnav), relink(footer)
header = header.replace('<a class="nav-txt" href="blog.html">', '<a class="nav-txt is-cur" href="blog.html">')

# ---------------- posts (placeholders until the real articles exist; each will link to its post page) ----------------
# (slug, topic, minutes, title, image, image alt)
TOPICS = ["Patient Acquisition", "Video", "SEO & AI Search", "Websites", "Your Team", "Results"]
TOPIC_ICON = {"Patient Acquisition": "ph-crosshair", "Video": "ph-film-slate", "SEO & AI Search": "ph-map-pin",
              "Websites": "ph-layout", "Your Team": "ph-headset", "Results": "ph-presentation-chart"}
POSTS = [
    ("attract-implant-patients", "Patient Acquisition", 6, "How to attract more dental implant patients this year", "svc/dental-marketing-card.webp", "A bright, modern dental surgery"),
    ("clinic-video-builds-trust", "Video", 4, "Why videos filmed in your own clinic build more trust than stock footage", "svc/dental-video-marketing-card.webp", "A professional video camera in a studio"),
    ("found-on-maps-and-ai", "SEO & AI Search", 5, "How patients find a dentist on Google Maps and in ChatGPT", "svc/dental-seo-card.webp", "Push pins marking places on a map"),
    ("website-that-books", "Websites", 4, "Five things every dental website needs to turn visitors into bookings", "svc/dental-website-design-card.webp", "A bright, minimal desk with a laptop"),
    ("every-lead-called", "Your Team", 3, "What changes when every new lead gets a call back", "svc/dental-call-centre-card.webp", "A smiling call centre agent with a headset"),
    ("presenting-treatment", "Your Team", 5, "Presenting treatment with confidence: a guide for coordinators", "svc/treatment-coordinator-training-card.webp", "A tablet showing a dental X-ray"),
    ("read-your-results", "Results", 4, "Which ads bring in patients? Reading your marketing results", "svc/dental-reporting-dashboard-card.webp", "A tablet showing a rising chart"),
    ("invisalign-marketing", "Patient Acquisition", 4, "Invisalign marketing that reaches the right patients", "v5/patient-laugh.webp", "A patient laughing in the dental chair"),
    ("full-arch-decisions", "Patient Acquisition", 6, "Full-arch implants: helping patients through a big decision", "clients/riverbend-photo.webp", "A calm, modern clinic reception"),
]
def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', html.unescape(t).lower()).strip('-')

def cards():
    out = []
    for slug, topic, mins, title, img, alt in POSTS:
        t = html.escape(title, quote=False)
        out.append(f'''            <article class="bc" data-topic="{slugify(topic)}">
              <a class="bc-in" href="#{slug}" aria-label="{html.escape(title)} ({mins} min read)">
                <div class="bc-media">
                  <img src="assets/img/{img}" alt="{alt}" loading="lazy" decoding="async" />
                  <span class="bc-by" aria-hidden="true"><span class="bc-i"><i class="ph-fill {TOPIC_ICON[topic]}"></i></span></span>
                </div>
                <p class="bc-meta"><span>{topic}</span><span>{mins} min read</span></p>
                <h3>{t}</h3>
              </a>
            </article>''')
    return '\n'.join(out)

def tabs():
    t = ['<button class="bt on" type="button" data-topic="all" aria-pressed="true">All posts <span>' + str(len(POSTS)) + '</span></button>']
    for topic in TOPICS:
        n = sum(1 for p in POSTS if p[1] == topic)
        t.append(f'<button class="bt" type="button" data-topic="{slugify(topic)}" aria-pressed="false">{html.escape(topic)} <span>{n}</span></button>')
    return '\n              '.join(t)

PAGE_CSS = """
      /* ================= blog listing (blog.html; built by build_blog.py) =================
         Head: the service hero's row 1 (dot label + H1 | intro). Then topic tabs (pills), then a 3-column grid of the home
         page's "Real clinics" white cards (6px inset photo, --r-card / --r-inner, --fs-h4 title, --fs-small meta). On
         hover the author avatar notch grows out of the photo's bottom-left corner (the photo is whole at rest) and the card's
         shadow deepens; no arrow circle, the normal cursor. Nothing slides or changes height. */
      .nav-txt.is-cur {
        color: var(--teal);
      }
      .blg {
        position: relative;
        padding: clamp(118px, calc(16 * var(--uvh)), 150px) 0 var(--sec-y);
        background: radial-gradient(30% 26% at 84% 10%, rgba(255, 191, 215, 0.34), transparent 70%);
      }
      .blg-in {
        max-width: var(--max);
        margin-inline: auto;
      }
      .blg-top {
        --fs-h1: clamp(38px, calc(4.2 * var(--uvw)), 68px); /* the home hero's size */
        display: grid;
        grid-template-columns: minmax(0, 7fr) minmax(0, 5fr);
        gap: 40px clamp(40px, calc(6 * var(--uvw)), 120px);
        align-items: start;
      }
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
      .blg-top .eyb {
        margin-bottom: 22px;
      }
      .blg-txt {
        padding-top: calc(var(--fs-small) * 1.4 + 22px);
      }
      .blg-txt p {
        font-size: var(--fs-lead);
        line-height: 1.45;
        color: var(--grey);
      }
      /* topic tabs: pills, the active one ink (the nav's dark pill vocabulary) */
      .btabs {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: clamp(48px, calc(5 * var(--uvw)), 72px);
      }
      .bt {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        height: 46px;
        padding: 0 18px 0 20px;
        border: 1px solid rgba(13, 19, 18, 0.1);
        border-radius: var(--r-pill);
        background: #fff;
        color: var(--ink);
        font: inherit;
        font-size: var(--fs-small);
        font-weight: 500;
        cursor: pointer;
        transition:
          background-color 0.3s,
          color 0.3s,
          border-color 0.3s;
      }
      .bt span {
        font-size: var(--fs-xs);
        color: var(--grey);
        font-variant-numeric: tabular-nums;
        transition: color 0.3s;
      }
      .bt:hover {
        border-color: rgba(27, 127, 115, 0.45);
      }
      .bt.on {
        background: var(--ink);
        border-color: var(--ink);
        color: #fff;
      }
      .bt.on span {
        color: var(--acc);
      }
      .bt:focus-visible {
        outline: 2px solid var(--teal);
        outline-offset: 3px;
      }
      /* the grid */
      .bgrid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 22px;
        margin-top: 28px;
      }
      .bc[hidden] {
        display: none;
      }
      .bc-in {
        position: relative;
        display: flex;
        flex-direction: column;
        height: 100%;
        padding: 6px 6px 26px;
        border-radius: var(--r-card);
        background: #fff;
        box-shadow: 0 1px 0 rgba(13, 19, 18, 0.03);
        color: inherit;
        cursor: default; /* the normal arrow cursor (user request) */
        transition: box-shadow 0.5s var(--ease);
      }
      .bc-in:hover,
      .bc-in:focus-visible {
        box-shadow: 0 24px 50px -26px rgba(13, 19, 18, 0.32);
      }
      .bc-in:focus-visible {
        outline: 2px solid var(--teal);
        outline-offset: 4px;
      }
      .bc-media {
        position: relative;
        aspect-ratio: 16 / 11;
        border-radius: var(--r-inner);
        overflow: hidden;
        background: var(--soft);
      }
      /* on hover the photo drifts up a little inside its frame (no zoom). It moves by `top`, not transform: the browser
         snaps a real position to whole pixels every frame, so the photo stays sharp while it moves (a transform lands on
         fractional pixels and is blended, i.e. soft, until it stops) */
      .bc-media > img {
        position: relative;
        top: 0;
        width: 100%;
        height: calc(100% + 28px);
        object-fit: cover;
        transition: top 0.6s var(--ease); /* quicker (user) */
      }
      .bc-in:hover .bc-media > img,
      .bc-in:focus-visible .bc-media > img {
        top: -28px;
      }
      /* the topic tile in a notch: a white tab in the photo's bottom-left corner with two concave corners, so the photo
         appears to curve around it (the card is white, so the tab simply matches it). It is always full size: at rest it
         waits just past the photo's bottom-left corner (the photo clips it, so the photo is whole), and on hover it slides
         in on the diagonal into place. Moving it never re-sizes or re-draws it, so the motion is smooth and the edges stay sharp (growing it
         by scale blurred the curves; growing it by real size stepped frame to frame). */
      .bc-by {
        --r: 22px;
        position: absolute;
        /* at rest: out past the photo's bottom-left corner (curves included). It slides by left/bottom, not transform,
           so every frame sits on whole pixels and the icon is 100% sharp throughout (no soft-then-sharp) */
        left: -110px;
        bottom: -110px;
        z-index: 1;
        padding: 11px 10px 1px 1px;
        border-top-right-radius: var(--r);
        background: #fff;
        transition:
          left 0.35s var(--ease),
          bottom 0.35s var(--ease); /* quick (user) */
      }
      /* on hover it slides in on the diagonal and lands 1px past the photo's edges (the photo clips that pixel, so no
         sliver of photo shows along them) */
      .bc-in:hover .bc-by,
      .bc-in:focus-visible .bc-by {
        left: -1px;
        bottom: -1px;
      }
      .bc-by::before,
      .bc-by::after {
        content: "";
        position: absolute;
        width: var(--r);
        height: var(--r);
        /* the concave corner: a hard edge with a 1px blend, smooth but sharp */
        background: radial-gradient(circle at 100% 0, transparent calc(var(--r) - 0.5px), #fff calc(var(--r) + 0.5px));
      }
      /* the two curved corners overlap the tab by 1px, so there is no seam for the photo to show through as a dark
         line while the notch moves (the extra pixel is plain white, under the curve) */
      .bc-by::before {
        left: 0;
        bottom: calc(100% - 1px);
        height: calc(var(--r) + 1px);
      }
      .bc-by::after {
        left: calc(100% - 1px);
        bottom: 0;
        width: calc(var(--r) + 1px);
      }
      /* the "How we help" tile: solid brand green, black filled icon, radius 24% (service pages, .hp-i) */
      .bc-i {
        display: grid;
        place-items: center;
        width: 72px;
        height: 72px;
        border-radius: calc(72px * 0.24);
        background: var(--teal-3);
        color: var(--ink);
        font-size: 40px;
      }
      .bc-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 6px 14px;
        margin: 22px 14px 0;
        font-size: var(--fs-small);
        color: var(--grey);
      }
      .bc-meta span {
        display: inline-flex;
        align-items: center;
        gap: 8px;
      }
      .bc-meta span:first-child {
        color: var(--teal);
        font-weight: 600;
      }
      .bc-meta span + span::before {
        content: "";
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: var(--acc-mid);
      }
      .bc h3 {
        margin: 10px 14px 0;
        font-size: var(--fs-h4);
        font-weight: 600;
        letter-spacing: -0.035em;
        line-height: 1.18;
      }
      .bempty {
        margin-top: 40px;
        font-size: var(--fs-lead);
        color: var(--grey);
      }
      @supports (corner-shape: squircle) {
        .bc-in,
        .bc-media {
          corner-shape: squircle;
        }
      }
      @media (max-width: 1199px) {
        .blg-top {
          grid-template-columns: 1fr;
        }
        .blg-txt {
          padding-top: 0;
          max-width: 640px;
        }
        .bgrid {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }
      }
      @media (max-width: 899px) {
        .blg-top {
          --fs-h1: clamp(28px, 7.8vw, 38px);
        }
        .btabs {
          flex-wrap: nowrap;
          overflow-x: auto;
          margin-inline: calc(-1 * var(--side));
          padding-inline: var(--side);
          scrollbar-width: none;
        }
        .btabs::-webkit-scrollbar {
          display: none;
        }
        .bt {
          flex: none;
        }
        .bgrid {
          grid-template-columns: 1fr;
        }
      }
"""
style_out = style.replace('    </style>', PAGE_CSS + '    </style>')

JS = r"""
    <script>
      (() => {
        const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
        const hasG = !!(window.gsap && window.ScrollTrigger);
        if (hasG) gsap.registerPlugin(ScrollTrigger);
        const $ = (s, r = document) => r.querySelector(s);
        const $$ = (s, r = document) => [...r.querySelectorAll(s)];
        const root = document.documentElement;
        const motion = hasG && !reduce;

        /* ---------- smooth scroll (as on the home page) ---------- */
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
        function closeMnav() {
          const done = () => {
            mOpen = false;
            mnav.hidden = true;
            mnav.classList.remove("open");
            burger.setAttribute("aria-expanded", "false");
            lock(false);
            burger.focus();
          };
          if (motion) gsap.to(mnav, { clipPath: "circle(0% at 92% 5%)", duration: 0.6, ease: "expo.in", onComplete: done });
          else done();
        }
        burger.addEventListener("click", openMnav);
        $(".mnav-x").addEventListener("click", closeMnav);
        {
          const tg = $(".mnav-tg"),
            sub = $("#mnSub");
          tg.addEventListener("click", () => {
            const open = tg.getAttribute("aria-expanded") !== "true";
            tg.setAttribute("aria-expanded", open);
            sub.hidden = !open;
          });
        }
        addEventListener("keydown", (e) => e.key === "Escape" && mOpen && closeMnav());

        /* ---------- topic tabs: show the posts of one topic (cards fade back in) ---------- */
        {
          const tabs = $$(".bt"),
            cards = $$(".bc"),
            empty = $(".bempty");
          tabs.forEach((t) =>
            t.addEventListener("click", () => {
              const topic = t.dataset.topic;
              tabs.forEach((x) => {
                x.classList.toggle("on", x === t);
                x.setAttribute("aria-pressed", x === t);
              });
              const shown = cards.filter((c) => {
                const on = topic === "all" || c.dataset.topic === topic;
                c.hidden = !on;
                return on;
              });
              empty.hidden = shown.length > 0;
              if (motion) gsap.fromTo(shown, { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: "expo.out", stagger: 0.05, clearProps: "opacity,transform" });
              if (hasG) ScrollTrigger.refresh();
            }),
          );
        }

        /* ---------- choreography (the home page's values) ---------- */
        if (!motion) return;
        const st = (trigger, start = "top 82%") => ({ trigger, start, once: true });
        gsap
          .timeline()
          .from(".nav > *", { y: -16, opacity: 0, duration: 0.9, ease: "power3.out", stagger: 0.07 }, 0)
          .from(".blg-top .eyb", { y: 14, opacity: 0, duration: 0.9, ease: "power3.out" }, 0.1)
          .from("#blog-title .ln-m > span", { yPercent: 110, duration: 1.2, ease: "expo.out", stagger: 0.09 }, 0.15)
          .from(".blg-txt p", { y: 18, opacity: 0, duration: 1, ease: "power3.out" }, 0.4)
          .from(".bt", { y: 16, opacity: 0, duration: 0.8, ease: "power3.out", stagger: 0.04 }, 0.5);
        gsap.set(".bc", { opacity: 0, y: 60 });
        ScrollTrigger.batch(".bc", { start: "top 94%", once: true, onEnter: (b) => gsap.to(b, { opacity: 1, y: 0, duration: 1.1, ease: "expo.out", stagger: 0.1, clearProps: "opacity,transform" }) });
        gsap.from(".f-g > *", { y: 30, opacity: 0, duration: 1.1, ease: "power3.out", stagger: 0.1, scrollTrigger: st(".foot", "top 85%") });
        addEventListener("load", () => ScrollTrigger.refresh());
      })();
    </script>"""

page = f'''<!doctype html>
<html lang="en-CA">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Dental Marketing Blog | Dental Media Corp</title>
    <meta
      name="description"
      content="Plain-language guides for dental clinics: attracting implant and Invisalign patients, clinic video, Google Maps and AI search, websites, and turning enquiries into booked patients."
    />
    <link rel="canonical" href="https://dentalmediacorp.com/blog/" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <meta name="theme-color" content="#0F1716" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Dental Media Corp" />
    <meta property="og:title" content="Dental Marketing Blog | Dental Media Corp" />
    <meta property="og:url" content="https://dentalmediacorp.com/blog/" />
    <meta property="og:locale" content="en_CA" />
{head_links}
{style_out}
  </head>
  <body>
    <a class="skip" href="#main">Skip to content</a>

    <!-- ============ HEADER (shared with the home page) ============ -->
{header}

    <!-- ============ MOBILE MENU ============ -->
{mnav}
    <main id="main">
      <!-- ============ BLOG LISTING
           Elementor: Archive template. Head (label, H1 | intro), then the category filter (Taxonomy Filter widget) and a
           Loop Grid over Posts, 3 columns, card skin = the "Real clinics" white card with the author avatar notch and the
           hover arrow. (Posts below are placeholders until the articles are written.) -->
      <section class="blg" aria-labelledby="blog-title">
        <div class="wrap">
          <div class="blg-in">
            <div class="blg-top">
              <div>
                <p class="eyb">The Blog</p>
                <h1 class="t-h1" id="blog-title">
                  <span class="ln-m"><span>Dental marketing,</span></span>
                  <span class="ln-m"><span>explained <span class="hl">simply.</span></span></span>
                </h1>
              </div>
              <div class="blg-txt">
                <p>Short, practical guides for dental clinics: how patients find you, what makes them trust you, and how more enquiries become booked patients.</p>
              </div>
            </div>
            <div class="btabs" role="group" aria-label="Filter posts by topic">
              {tabs()}
            </div>
            <div class="bgrid">
{cards()}
            </div>
            <p class="bempty" hidden>No posts in this topic yet.</p>
          </div>
        </div>
      </section>
    </main>

    <div class="sbreak" aria-hidden="true"></div>
    <!-- ============ FOOTER (shared with the home page) ============ -->
{footer}

    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>{JS}
  </body>
</html>
'''
page = preloader.inject(page)
open('blog.html', 'wb').write(page.replace('\n', '\r\n').encode('utf-8'))
print('ok blog.html', len(page.splitlines()))
