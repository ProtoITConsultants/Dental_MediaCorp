# -*- coding: utf-8 -*-
# Builds case-studies.html from index.html's shared parts (the same <style>, header, mobile menu, footer and the video
# lightbox) plus the case-studies grid. Layout after madebyshape.co.uk/work: two columns, the right one starting lower so
# the cards step diagonally, with a client quote and a video card in the flow. Built from our own components: the cards
# have no card around them: the image stands alone, the text sits under it, with one notch always cut into it: the
# bottom-left one holds the home CTA ("View case study", the "Tell me more" button). Run from the repo root:
#   python .claude/skills/dmc-design/build_cases.py
import re, html

src = open('index.html', 'rb').read().decode('utf-8').replace('\r\n', '\n')

def between(a, b, s=src):
    i = s.index(a); j = s.index(b, i)
    return s[i:j + len(b)]

style = between('    <style>', '    </style>')
header = between('    <header class="top" id="top">', '    </header>')
mnav = between('    <div class="mnav" id="mnav"', '      </div>\n    </div>\n')
footer = between('    <footer class="foot">', '    </footer>')
vbox = between('    <div class="vbox" id="vbox"', '    </div>\n')
head_links = between('    <link rel="icon"', '/src/fill/style.css"\n    />')

HOME = 'index.html'
def relink(h):
    h = h.replace('href="#treatments"', 'href="dental-marketing.html"')
    h = re.sub(r'href="#(svc-[a-z]+|services|results|testimonials|dmc|faq|contact|about)"', lambda m: f'href="{HOME}#{m.group(1)}"', h)
    h = h.replace('href="#main"', f'href="{HOME}"')
    return h
header, mnav, footer = relink(header), relink(mnav), relink(footer)
header = header.replace('<a href="case-studies.html">Case Studies</a>', '<a class="is-cur" href="case-studies.html">Case Studies</a>')

CTA_IN = ('<span class="cta wk-cta" aria-hidden="true"><span class="cta-t">View case study</span><span class="cta-i">'
          '<i class="ph ph-arrow-right"></i><i class="ph ph-arrow-right"></i></span></span>')

# ---------------- content: the home page's five case studies (real figures), two client quotes, one client video ----
# card: (slug, clinic, return, title, image, alt, w, h, tags)
CASES = [
    ("west-grande-prairie-dental", "West Grande Prairie Dental", "19.4×", "$97,000 in revenue from a $5,000 ad spend",
     "clients/wgp-photo.jpg", "West Grande Prairie Dental storefront", 1619, 1080, ["Dental Marketing", "19.4× return"]),
    ("riverbend-denture-implant", "Riverbend Denture & Implant", "13.4×", "$255,000 in revenue from a $19,000 ad spend",
     "clients/riverbend-photo.webp", "Riverbend Denture & Implant Clinic reception", 1500, 1000, ["Dental Marketing", "13.4× return"]),
    ("smile-now", "Smile Now", "12.4×", "$161,000 in revenue from a $13,000 ad spend",
     "clients/smilenow-photo.webp", "Calgary skyline and the Peace Bridge", 1600, 900, ["Dental Marketing", "12.4× return"]),
    ("wye-dental", "Wye Dental", "15.3×", "$92,000 in revenue from a $6,000 ad spend",
     "clients/wye-photo.webp", "The Wye Dental team", 2048, 1066, ["Dental Marketing", "15.3× return"]),
    ("modern-smiles", "Modern Smiles", "12×", "$72,000 in revenue from a $6,000 ad spend",
     "clients/modern-smiles-photo.webp", "A denture being made at Modern Smiles", 1024, 554, ["Dental Marketing", "12× return"]),
]
QUOTES = [
    ("We’ve opened up another operatory just to deal with the overflow of new patients.", "Dr. Mark Warawa", "Bright Smile Dental", "M"),
    ("DMC is the first marketing that’s actually paid off since I opened in 2012.", "Rae-Lynne D.", "Modern Smiles & Northern Lights", "R"),
]
VIDEO = ("xulePDv7Zt8", "svc/broyde-video.webp", 1280, 628, "Dr. Greg Broyde", "West Grande Prairie Dental & East Village Dental",
         "“For every dollar I spend, DMC makes sure I get at least $6 to $10 back.”")

def case_html(c, order):
    slug, clinic, ret, title, img, alt, w, h, tags = c
    return f'''            <article class="wk" id="{slug}" style="--o: {order}">
              <a class="wk-in" href="case-{slug}.html" aria-label="{html.escape(clinic)}: {html.escape(title)}">
                <div class="wk-fig">
                  <div class="wk-media">
                    <img src="assets/img/{img}" alt="{html.escape(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async" />
                  </div>
                  {CTA_IN}
                </div>
                <p class="wk-meta"><span>{html.escape(clinic)}</span><span>Return on ad spend <b>{ret}</b></span></p>
                <h2 class="wk-t">{html.escape(title)}</h2>
              </a>
            </article>'''

def quote_html(q, order):
    text, name, clinic, letter = q
    return f'''            <figure class="wq" style="--o: {order}">
              <blockquote><i class="ph-fill ph-quotes" aria-hidden="true"></i>{html.escape(text)}</blockquote>
              <figcaption><span class="wq-i" aria-hidden="true">{letter}</span><span><b>{html.escape(name)}</b><small>{html.escape(clinic)}</small></span></figcaption>
            </figure>'''

def video_html(order):
    vid, img, w, h, name, clinic, quote = VIDEO
    return f'''            <article class="wk wk-video" style="--o: {order}">
              <button class="wk-in" type="button" data-video="{vid}" aria-label="Play {html.escape(name)}’s video testimonial">
                <div class="wk-fig">
                  <div class="wk-media">
                    <img src="assets/img/{img}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async" />
                    <span class="wk-play" aria-hidden="true"><i class="ph-fill ph-play"></i></span>
                  </div>
                </div>
                <p class="wk-meta"><span>{html.escape(name)}</span><span>{html.escape(clinic)}</span></p>
                <h2 class="wk-t">{html.escape(quote)}</h2>
              </button>
            </article>'''

# the two columns (the right one starts lower: the diagonal); --o is the reading order on phones (one column)
LEFT = [case_html(CASES[0], 1), quote_html(QUOTES[1], 4), case_html(CASES[2], 5), case_html(CASES[4], 8)]
RIGHT = [quote_html(QUOTES[0], 2), case_html(CASES[1], 3), video_html(6), case_html(CASES[3], 7)]

PAGE_CSS = """
      /* ================= case studies (case-studies.html; built by build_cases.py) =================
         Head: the blog / service hero row 1. Then two columns, the right one starting lower, so the cards step diagonally
         (after madebyshape.co.uk/work), with client quotes and a video card in the flow. Cards = the home "Real clinics" /
         blog white card (6px inset photo, --r-card / --r-inner). Hover: the photo drifts up by `top`, the tag chips (the
         services carousel's dark-glass chip) and the home CTA ("Tell me more" size) slide in, the shadow deepens. All of
         it moves by real position (whole pixels: sharp, no blur). Pointer cursor on the cards (user). */
      .header-cur,
      .menu a.is-cur {
        color: var(--teal);
      }
      .wks {
        position: relative;
        padding: clamp(118px, calc(16 * var(--uvh)), 150px) 0 var(--sec-y);
        background: radial-gradient(30% 26% at 84% 10%, rgba(255, 191, 215, 0.34), transparent 70%);
      }
      .wks-in {
        max-width: var(--max);
        margin-inline: auto;
      }
      .wks-top {
        --fs-h1: clamp(38px, calc(4.2 * var(--uvw)), 68px);
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
      .wks-top .eyb {
        margin-bottom: 22px;
      }
      .wks-txt {
        padding-top: calc(var(--fs-small) * 1.4 + 22px);
      }
      .wks-txt p {
        font-size: var(--fs-lead);
        line-height: 1.45;
        color: var(--grey);
      }
      /* the diagonal: two columns, the right one starts lower */
      .wgrid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0 clamp(22px, calc(2.4 * var(--uvw)), 40px);
        margin-top: var(--sec-head);
      }
      .wcol {
        display: flex;
        flex-direction: column;
        gap: clamp(56px, calc(6 * var(--uvw)), 104px);
      }
      .wcol + .wcol {
        padding-top: clamp(120px, calc(14 * var(--uvw)), 260px);
      }
      /* the case: no card around it (user). The image stands alone with the card radius; the text sits under it on the
         page background. The whole case is one link; the pointer cursor. */
      .wk-in {
        display: block;
        width: 100%;
        padding: 0;
        border: 0;
        background: none;
        color: inherit;
        font: inherit;
        text-align: left;
        cursor: pointer; /* the whole case card is a link (user) */
      }
      .wk-in:focus-visible {
        outline: 2px solid var(--teal);
        outline-offset: 6px;
        border-radius: var(--r-card);
      }
      .wk {
        scroll-margin-top: 110px; /* case-studies.html#<slug> (from the home clinic cards) lands under the header */
      }
      .wk-fig {
        position: relative;
      }
      /* plain circular corners (28px, the card radius without squircle): the hover notch is drawn with circular arcs,
         so the image must use the same corner at rest, or its corners would change shape when the notch opens */
      .wk-media {
        position: relative;
        aspect-ratio: 4 / 3;
        border-radius: 28px;
        overflow: hidden;
        background: var(--soft);
      }
      /* the photo drifts up a little on hover (by `top`: whole pixels, sharp) */
      .wk-media > img {
        position: relative;
        top: 0;
        width: 100%;
        height: calc(100% + 28px);
        object-fit: cover;
        transition: top 0.45s var(--ease); /* in sync with the notches (0.45s, the same curve) */
      }
      .wk-in:hover .wk-media > img,
      .wk-in:focus-visible .wk-media > img {
        top: -28px;
      }
      /* the tag pills sit in a notch the script cuts into the image's top-right corner on hover (the service banner's
         notch: curves = the image radius). They are on the page background there, so they are the blog tabs' white pill. */
      .wk-chips {
        position: absolute;
        top: 0;
        right: 0;
        z-index: 1;
        display: flex;
        gap: 10px;
        pointer-events: none;
      }
      /* the tag pills: the CTA's pill (user): 62px, ink, white text, the button's type size */
      .wk-chip {
        display: inline-flex;
        align-items: center;
        height: 62px;
        padding: 0 28px;
        border-radius: var(--r-pill);
        background: var(--ink);
        color: #fff;
        font-size: var(--fs-body);
        font-weight: 500;
        white-space: nowrap;
      }
      /* the home CTA ("Tell me more", 62px, the pink circle with the arrow swap) in its own notch at the image's
         bottom-left (the script cuts it with the top-right one), so it sits on the page background, like "Tell me more" on
         the service banner; it fades in as the notch opens */
      .wk-cta {
        position: absolute;
        left: 0;
        bottom: 0;
        z-index: 1;
        transition: background-color 0.35s;
      }
      .wk-in:hover .wk-cta .cta-i {
        background: var(--acc-hover);
      }
      .wk-in:hover .wk-cta .cta-i i:first-child {
        transform: translateX(48px);
      }
      .wk-in:hover .wk-cta .cta-i i + i {
        transform: none;
      }
      /* video card: the home reviews' white play circle, always visible */
      .wk-play {
        position: absolute;
        left: 50%;
        top: 50%;
        z-index: 1;
        display: grid;
        place-items: center;
        width: 76px;
        height: 76px;
        margin: -38px 0 0 -38px;
        border-radius: 50%;
        background: #fff;
        color: var(--ink);
        font-size: 24px;
        box-shadow: 0 14px 30px -12px rgba(13, 19, 18, 0.5);
        transition:
          background-color 0.3s,
          color 0.3s;
      }
      .wk-in:hover .wk-play {
        background: var(--ink);
        color: #fff;
      }
      .wk-video .wk-in {
        cursor: pointer;
      }
      .wk-meta {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 6px 14px;
        margin: 22px 0 0;
        font-size: var(--fs-small);
        color: var(--grey);
      }
      .wk-meta span {
        display: inline-flex;
        align-items: center;
        gap: 8px;
      }
      .wk-meta span:first-child {
        color: var(--teal);
        font-weight: 600;
      }
      .wk-meta span + span::before {
        content: "";
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: var(--acc-mid);
      }
      .wk-meta b {
        padding: 1px 7px;
        border-radius: 6px;
        font-weight: 600;
        color: var(--acc-on);
        background: var(--acc);
      }
      .wk-t {
        margin: 10px 0 0;
        font-size: var(--fs-h3);
        font-weight: 600;
        letter-spacing: -0.035em;
        line-height: 1.12;
      }
      /* client quote in the flow: the video card's quote style (pink quote mark, --fs-list), the "How we help" tile */
      .wq {
        margin: 0;
      }
      .wq blockquote {
        margin: 0;
        font-size: var(--fs-list);
        font-weight: 600;
        letter-spacing: -0.035em;
        line-height: 1.12;
      }
      .wq blockquote i {
        margin-right: 0.3em;
        font-size: 0.7em;
        vertical-align: 0.12em;
        color: var(--acc-mid);
      }
      .wq figcaption {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 26px;
      }
      .wq-i {
        display: grid;
        flex: none;
        place-items: center;
        width: 52px;
        height: 52px;
        border-radius: 12px;
        background: var(--teal-3);
        color: var(--ink);
        font-size: 22px;
        font-weight: 700;
      }
      .wq b {
        display: block;
        font-size: var(--fs-body);
        font-weight: 600;
      }
      .wq small {
        display: block;
        font-size: var(--fs-small);
        color: var(--grey);
      }
      @media (max-width: 1199px) {
        .wks-top {
          grid-template-columns: 1fr;
        }
        .wks-txt {
          padding-top: 0;
          max-width: 640px;
        }
      }
      /* phones: one column in reading order (--o), no stagger; chips and CTA shown (no hover) */
      @media (max-width: 899px) {
        .wks-top {
          --fs-h1: clamp(28px, 7.8vw, 38px);
        }
        .wgrid {
          display: flex;
          flex-direction: column;
          gap: 48px;
        }
        .wcol {
          display: contents;
        }
        .wcol > * {
          order: var(--o);
        }
        .wk-chips {
          top: 12px;
          right: 12px;
          gap: 6px;
        }
        .wk-chip {
          height: 40px;
          padding: 0 16px;
          font-size: var(--fs-xs);
        }
        .wk-cta {
          display: none;
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

        const top = $("#top");
        const stuck = () => top.classList.toggle("is-stuck", scrollY > 30);
        addEventListener("scroll", stuck, { passive: true });
        stuck();

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

        /* ---------- the notches: the image's top-right corner is cut around the tag pills, its bottom-left around the CTA ----------
           Always open (the resting look; user). Drawn as one clip-path outline with the curves = the image's own radius, like
           the service banner's notch; re-drawn on resize. 900px and wider (phones: the pills sit on the image). */
        {
          const wide = matchMedia("(min-width: 900px)");
          const cut = (media, chips, cta) => {
            if (!wide.matches) return void (media.style.clipPath = "");
            const W = media.offsetWidth,
              H = media.offsetHeight,
              R = parseFloat(getComputedStyle(media).borderTopLeftRadius) || 28,
              r = R,
              g = Math.round(12 / (parseFloat(getComputedStyle(document.documentElement).zoom) || 1)), // 12px on screen at any laptop zoom (user)
              tw = chips ? chips.offsetWidth + g : 0, // top-right notch: the pills (the cards have none now)
              th = chips ? chips.offsetHeight + g : 0,
              bw = cta ? cta.offsetWidth + g : 0, // bottom-left notch: the CTA (the video card has none)
              bh = cta ? cta.offsetHeight + g : 0,
              p = cta ? Math.min(cta.offsetHeight / 2 + g, bh - r) : r; // concentric with the pill: the gap stays g all the way round
            if (!chips && !cta) return void (media.style.clipPath = "");
            const top = chips
              ? `H${W - tw - r} A${r},${r} 0 0 1 ${W - tw},${r} V${th - r} A${r},${r} 0 0 0 ${W - tw + r},${th} H${W - R} A${R},${R} 0 0 1 ${W},${th + R}`
              : `H${W - R} A${R},${R} 0 0 1 ${W},${R}`;
            const bottom = cta
              ? `H${bw + r} A${r},${r} 0 0 1 ${bw},${H - r} V${H - bh + p} A${p},${p} 0 0 0 ${bw - p},${H - bh} H${R} A${R},${R} 0 0 1 0,${H - bh - R}`
              : `H${R} A${R},${R} 0 0 1 0,${H - R}`;
            media.style.clipPath = `path("M${R},0 ${top} V${H - R} A${R},${R} 0 0 1 ${W - R},${H} ${bottom} V${R} A${R},${R} 0 0 1 ${R},0 Z")`;
          };
          const all = $$(".wk-in").map((card) => [$(".wk-media", card), $(".wk-chips", card), $(".wk-cta", card)]);
          const drawAll = () => all.forEach((a) => cut(...a));
          drawAll();
          addEventListener("resize", drawAll);
          wide.addEventListener("change", drawAll);
          document.fonts && document.fonts.ready.then(drawAll); // the pills' width depends on the font
        }

        /* ---------- the video card opens the home page's lightbox (YouTube) ---------- */
        {
          const vb = $("#vbox"),
            vbF = $("#vboxF"),
            vbX = $(".vbox-x");
          let from = null;
          const close = () => {
            if (vb.hidden) return;
            vb.hidden = true;
            vbF.replaceChildren();
            lock(false);
            if (from) from.focus({ preventScroll: true });
          };
          $$("[data-video]").forEach((btn) =>
            btn.addEventListener("click", () => {
              const f = document.createElement("iframe");
              f.src = "https://www.youtube-nocookie.com/embed/" + btn.dataset.video + "?autoplay=1&rel=0&playsinline=1";
              f.title = btn.getAttribute("aria-label").replace(/^Play /, "");
              f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
              f.allowFullscreen = true;
              f.referrerPolicy = "strict-origin-when-cross-origin";
              vbF.replaceChildren(f);
              vb.hidden = false;
              from = btn;
              lock(true);
              vbX.focus();
            }),
          );
          vbX.addEventListener("click", close);
          vb.addEventListener("click", (e) => e.target === vb && close());
          addEventListener("keydown", (e) => {
            if (e.key !== "Escape") return;
            if (!vb.hidden) close();
            else if (mOpen) closeMnav();
          });
        }

        /* ---------- arriving from a home clinic card (case-studies.html#<slug>): land on that case under the header ----------
           The browser jumps before the photos above have loaded (and they shift the case down), so align again once the
           page has loaded. Measured without the card's entrance offset (GSAP y), 110px under the top (the header). */
        {
          const t = location.hash.length > 1 && document.getElementById(decodeURIComponent(location.hash.slice(1)));
          if (t) {
            const land = () => {
              const y = t.getBoundingClientRect().top + scrollY - (hasG ? gsap.getProperty(t, "y") : 0) - 110;
              if (lenis) lenis.scrollTo(y, { immediate: true, force: true });
              else scrollTo(0, y);
            };
            land();
            addEventListener("load", () => requestAnimationFrame(land));
          }
        }

        if (!motion) return;
        const st = (trigger, start = "top 82%") => ({ trigger, start, once: true });
        gsap
          .timeline()
          .from(".nav > *", { y: -16, opacity: 0, duration: 0.9, ease: "power3.out", stagger: 0.07 }, 0)
          .from(".wks-top .eyb", { y: 14, opacity: 0, duration: 0.9, ease: "power3.out" }, 0.1)
          .from("#work-title .ln-m > span", { yPercent: 110, duration: 1.2, ease: "expo.out", stagger: 0.09 }, 0.15)
          .from(".wks-txt p", { y: 18, opacity: 0, duration: 1, ease: "power3.out" }, 0.4);
        gsap.set(".wk, .wq", { opacity: 0, y: 60 });
        gsap.set(".wk-cta", { opacity: 0, y: 16 }); // the notch's button fades in after its photo (the service banner's order)
        ScrollTrigger.batch(".wk, .wq", {
          start: "top 72%", // a good part of the card is on screen first, so its photo and notch are seen arriving (user)
          once: true,
          onEnter: (b) => {
            gsap.to(b, { opacity: 1, y: 0, duration: 1.3, ease: "expo.out", stagger: 0.1, clearProps: "opacity,transform" });
            gsap.from(b.flatMap((c) => $$(".wk-media > img", c)), { scale: 1.25, duration: 1.8, ease: "expo.out", stagger: 0.1 });
            gsap.to(b.flatMap((c) => $$(".wk-cta", c)), { opacity: 1, y: 0, duration: 0.9, ease: "power3.out", stagger: 0.1, delay: 0.55, clearProps: "opacity,transform" });
          },
        });
        gsap.from(".f-g > *", { y: 30, opacity: 0, duration: 1.1, ease: "power3.out", stagger: 0.1, scrollTrigger: st(".foot", "top 85%") });
        addEventListener("load", () => ScrollTrigger.refresh());
      })();
    </script>"""

nl = '\n'
page = f'''<!doctype html>
<html lang="en-CA">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Dental Marketing Case Studies | Dental Media Corp</title>
    <meta
      name="description"
      content="Real clinics, real results: dental clinics across Canada that turned their marketing into booked patients and accepted treatment with Dental Media Corp."
    />
    <link rel="canonical" href="https://dentalmediacorp.com/case-studies/" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <meta name="theme-color" content="#0F1716" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Dental Media Corp" />
    <meta property="og:title" content="Dental Marketing Case Studies | Dental Media Corp" />
    <meta property="og:url" content="https://dentalmediacorp.com/case-studies/" />
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
      <!-- ============ CASE STUDIES
           Elementor: Archive template for the "Case Study" CPT. Head (label, H1 | intro), then two columns (the right one
           offset down) of Loop items: case cards (ACF: photo, clinic, return, headline, tags, page link), client quotes and a
           video card (YouTube ID). Case cards link to their case study pages (placeholders until those exist). -->
      <section class="wks" aria-labelledby="work-title">
        <div class="wrap">
          <div class="wks-in">
            <div class="wks-top">
              <div>
                <p class="eyb">Case Studies</p>
                <h1 class="t-h1" id="work-title">
                  <span class="ln-m"><span>Real clinics,</span></span>
                  <span class="ln-m"><span>real <span class="hl">results.</span></span></span>
                </h1>
              </div>
              <div class="wks-txt">
                <p>Dental clinics across Canada that handed us their marketing. We ran the ads, called the leads and booked the patients. Here is what came back.</p>
              </div>
            </div>
            <div class="wgrid">
              <div class="wcol">
{nl.join(LEFT)}
              </div>
              <div class="wcol">
{nl.join(RIGHT)}
              </div>
            </div>
            <p class="note">Individual campaign examples. Results vary by clinic, market, and treatment offering.</p>
          </div>
        </div>
      </section>
    </main>

    <!-- video lightbox (shared with the home page) -->
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
# case-studies.html is back (user, 2026-11-24): "Case Studies" (nav, menu, footer) and "Browse all case studies" open
# this page. build_case.py imports this file for its parts, so the page is written only when run directly.
if __name__ == '__main__':
    import sys, os
    sys.dont_write_bytecode = True
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import preloader
    out = preloader.inject(page)
    open('case-studies.html', 'wb').write(out.replace(chr(10), chr(13) + chr(10)).encode('utf-8'))
    print('ok case-studies.html', len(out.splitlines()))
