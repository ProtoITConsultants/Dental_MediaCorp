# -*- coding: utf-8 -*-
# Builds one page per case study (case-<slug>.html), after madebyshape.co.uk/work/this-is-digital (the order of the
# sections only; every size, button, card and motion is ours). Reuses the service template (build_service.py) and the
# case cards (build_cases.py), so nothing here is a new pattern:
#   1. hero: the clinic + H1 in a notch cut into the banner's top-right corner (the service banner and its notch
#      technique), the home glass numbers on the photo
#   2. the project: H2 left | intro + Client / Service / Ad spend (row 3 of the service hero)
#   3. the service page's video card + "Play video": the clinic's own testimonial video (name + words on it) where one
#      exists, otherwise the Dental Marketing video with its line
#   4. the home reviews row, 5. "What next?" (the "What we book" photo row was removed, user 2026-11-25; BOOK and
#   book_html are kept unused)
#   (no challenge | result, no how-we-did-it list, no closing ask: user): two more case cards (the case-studies card) + Browse all case studies
#   (no How we help, no video card, no results panels: user)
# Every clinic card (home "Real clinics" and What next) opens these pages; "Browse all case studies" opens case-studies.html.
# Run from the repo root:  python .claude/skills/dmc-design/build_case.py
import os, sys, json, html
import sys as _sys, os as _os
_sys.dont_write_bytecode = True
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import preloader  # the home page's preloader on every page
sys.dont_write_bytecode = True  # no __pycache__ next to the builders
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_service as bs
import build_cases as bc

MKT = next(sv for sv in bs.SERVICES if sv['file'] == 'dental-marketing.html')
HL = '<span class="hl">{}</span>'

# per case: the logo (the home "Real clinics" card's), the overview copy, the results copy.
# Copy voice (skill 2b): we do it all, the clinic's team sees the patients. Only real figures (from the home page).
STORY = {
    "west-grande-prairie-dental": dict(
        logo=("clients/case-wgp.webp", 900, 695),
        o1="A busy clinic that wanted", o2="more " + HL.format("booked patients."),
        intro="West Grande Prairie Dental wanted more new patients without adding work for the front desk. We created the ads, filmed the videos, called every lead and booked qualified patients into their schedule. Their team just saw the patients who walked in."),
    "riverbend-denture-implant": dict(
        logo=("clients/riverbend.png", 714, 183),
        o1="Implant patients,", o2="booked " + HL.format("for the team."),
        intro="Riverbend Denture & Implant wanted more patients ready for dentures and implants. We ran the campaigns, contacted every enquiry and booked the right patients straight into their calendar, so the team could focus on treatment."),
    "smile-now": dict(
        logo=("clients/case-smilenow.webp", 900, 215),
        o1="A growing clinic", o2="in a " + HL.format("busy city."),
        intro="Smile Now wanted to stand out in a crowded Calgary market. We created ads people trust, followed up with every lead and booked qualified patients into their schedule. Their team just met the patients who came in."),
    "wye-dental": dict(
        logo=("clients/case-wye.webp", 800, 640),
        o1="A friendly team that", o2="wanted " + HL.format("more patients."),
        intro="Wye Dental wanted a steady flow of new patients without chasing leads. We ran their ads, filmed their team, called every enquiry and booked patients into their schedule, so the team could do what it does best."),
    "modern-smiles": dict(
        logo=("clients/case-modern-smiles.webp", 900, 675),
        o1="Denture patients,", o2="ready for " + HL.format("treatment."),
        intro="Modern Smiles wanted marketing that finally paid off. We created the ads, contacted every lead and booked patients ready for dentures into their schedule. Their team just welcomed the patients who walked in."),
}

# where each hero photo is anchored in the tall banner (so the clinic's sign clears the notch)
POS = {"west-grande-prairie-dental": "50% 0%", "wye-dental": "50% 22%"}

# "What we book": four photos per case, picked for what each clinic does (the clinic's own photo where its size allows,
# then treatment photos). (file, w, h, alt, caption, object-position). Slots: 1 tall 9:16, 2 5:6, 3 big 9:10, 4 square.
BOOK = {
    "west-grande-prairie-dental": [  # their windows: Sedation, Invisalign, Family, Esthetics, Implants
        ("implant.webp", 900, 1350, "A gloved hand holding a dental implant and crown", "Implants", "50% 50%"),
        ("sedation.webp", 900, 600, "A patient relaxed in the chair under sedation", "Sedation", "50% 50%"),
        ("smile.webp", 900, 1350, "A woman smiling after cosmetic treatment", "Esthetics", "50% 30%"),
        ("family.webp", 900, 1350, "A dentist with a young patient, family dental care", "Family care", "50% 40%"),
    ],
    "riverbend-denture-implant": [
        ("implant.webp", 900, 1350, "A gloved hand holding a dental implant and crown", "Implants", "50% 50%"),
        ("clients/riverbend-photo.webp", 1500, 1000, "Riverbend Denture & Implant Clinic, the treatment room", "Their clinic", "72% 50%"),
        ("case1.webp", 1400, 1050, "A clinician talking a patient through treatment", "Denture consultations", "40% 50%"),
        ("case3.webp", 1400, 936, "A treatment room ready for the next patient", "A full schedule", "50% 50%"),
    ],
    "smile-now": [
        ("smile.webp", 900, 1350, "A woman smiling after cosmetic treatment", "Smile makeovers", "50% 30%"),
        ("aligner.webp", 900, 675, "A patient fitting clear aligners", "Clear aligners", "50% 50%"),
        ("case1.webp", 1400, 1050, "A clinician talking a patient through treatment", "Consultations", "40% 50%"),
        ("clients/smilenow-photo.webp", 1600, 900, "Calgary skyline and the Peace Bridge", "Calgary", "40% 50%"),
    ],
    "wye-dental": [
        ("family.webp", 900, 1350, "A dentist with a young patient, family dental care", "Family care", "50% 40%"),
        ("clients/wye-photo.webp", 2048, 1066, "The Wye Dental team", "The Wye team", "50% 40%"),
        ("case2.webp", 1400, 2100, "A patient in the chair at a new patient visit", "New patients", "50% 45%"),
        ("smile.webp", 900, 1350, "A woman smiling after treatment", "Healthy smiles", "50% 30%"),
    ],
    "modern-smiles": [  # dentures: none of Riverbend's photos twice
        ("case2.webp", 1400, 2100, "A patient in the chair on treatment day", "Treatment day", "50% 45%"),
        ("clients/modern-smiles-photo.webp", 1024, 554, "A denture being made at Modern Smiles", "Dentures, made in house", "50% 50%"),
        ("smile.webp", 900, 1350, "A woman smiling with her new teeth", "New smiles", "50% 30%"),
        ("case3.webp", 1400, 936, "A treatment room ready for the next patient", "A full schedule", "50% 50%"),
    ],
}

# the client video: the clinic's own testimonial (from the home reviews row) where there is one, otherwise the Dental
# Marketing video with its service-page line. (embed, still, w, h, alt, position, name or None, line)
YT = "https://www.youtube-nocookie.com/embed/{}?autoplay=1&rel=0&playsinline=1"
MKT_VIDEO = ("https://drive.google.com/file/d/13MqhWz0r0u-TySTFtp3yZwiZIhq83WXe/preview", "svc/marketing-video.webp", 2880, 1620,
             "A Dental Media Corp presenter inside a dental clinic", "50% 50%", None, "See how we turn your clinic into ads that book patients.")
VIDEOS = {
    "west-grande-prairie-dental": (YT.format("xulePDv7Zt8"), "svc/broyde-video.webp", 1280, 628, "Dr. Greg Broyde in his clinic",
                                   "50% 35%", "Dr. Greg Broyde", "“For every dollar I spend, DMC makes sure that I get at least $6 to $10 back.”"),
    "modern-smiles": (YT.format("NgVZUXrVF44"), "svc/rae-lynne-video.webp", 1280, 630, "Rae-Lynne from Modern Smiles in conversation",
                      "50% 30%", "Rae-Lynne D.", "“DMC is the first marketing that’s actually paid off since I opened in 2012.”"),
}

def video_html(slug):
    e = html.escape
    emb, img, w, h, alt, pos, name, line = VIDEOS.get(slug, MKT_VIDEO)
    say = (f'<p class="vt-q"><span>{e(name)}</span></p>' + chr(10) + f'                  <p class="vt-d"><span>{e(line)}</span></p>' if name
           else f'<p class="vt-q"><span>{e(line)}</span></p>')
    label = f"Play {name}’s video" if name else "Play the Dental Marketing video"
    return f'''              <div class="vt-box" id="vtBox" data-embed="{e(emb)}">
                <div class="vt-media"><img src="assets/img/{img}" alt="{e(alt)}" width="{w}" height="{h}" style="object-position: {pos}" loading="lazy" decoding="async" /></div>
                <div class="vt-say">
                  {say}
                </div>
                <button class="vt-play" type="button" aria-label="{e(label)}"><i class="ph-fill ph-play" aria-hidden="true"></i></button>
                <button class="vt-x" type="button" aria-label="Close the video" tabindex="-1"><i class="ph-bold ph-x" aria-hidden="true"></i></button>
              </div>
'''

def book_html(slug):
    e = html.escape
    return ''.join(f'''            <figure class="cst-i">
              <div class="cst-m"><img src="assets/img/{f}" alt="{e(a)}" width="{w}" height="{h}" style="object-position: {pos}" loading="lazy" decoding="async" /></div>
              <figcaption>{e(c)}</figcaption>
            </figure>
''' for f, w, h, a, c, pos in BOOK[slug])

def page_file(slug):
    return f'case-{slug}.html'

CASE_CSS = """
      /* ================= case study page (case-<slug>.html; built by build_case.py) =================
         After madebyshape.co.uk/work/this-is-digital, in our vocabulary: the service hero's banner with the notch (here
         in the top-right corner, holding the clinic and the H1), the service sections, the home stat cards and the case
         cards. */
      .csh-w {
        --csh-t: clamp(96px, calc(7.2 * var(--uvw)), 132px); /* where the banner starts: the H1's first line sits above it, the rest in the notch */
        position: relative;
        padding-top: var(--csh-t);
      }
      /* the clinic and the H1 sit in a notch the script cuts into the banner's top-right corner (its curves = the
         banner's radius, like the service banner's "Tell me more" notch); the notch follows the text's real size */
      .csh-tab {
        position: absolute;
        top: 0;
        right: 0;
        z-index: 2;
        max-width: 58%;
        padding: 0 0 4px clamp(20px, calc(1.6 * var(--uvw)), 32px);
      }
      .csh-tab .eyb {
        margin-bottom: 18px;
      }
      /* the banner keeps the service hero's height (.svb), so every hero image card is the same size (user) */
      /* the project (row 2 of the hero, the service hero's statement row rhythm) */
      .cso {
        display: grid;
        grid-template-columns: minmax(0, 7fr) minmax(0, 5fr);
        gap: 40px clamp(40px, calc(6 * var(--uvw)), 120px);
        align-items: start;
        padding-top: var(--sec-y);
      }
      .cso .eyb {
        margin-bottom: 20px;
      }
      .cso-r {
        padding-top: calc(var(--fs-small) * 1.4 + 20px); /* level with the H2, under the label */
      }
      .cso-r p {
        font-size: var(--fs-lead);
        line-height: 1.45;
        color: var(--grey);
      }
      .cso-m {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 24px;
        margin: 36px 0 0;
        padding-top: 24px;
        border-top: 1px solid rgba(13, 19, 18, 0.1);
      }
      .cso-m dt {
        font-size: var(--fs-small);
        color: var(--grey);
      }
      .cso-m dd {
        margin: 6px 0 0;
        font-size: var(--fs-h5);
        font-weight: 600;
        letter-spacing: -0.02em;
        line-height: 1.25;
      }
      /* What next: two case cards (the case-studies page's card and its notch) */
      .csn-g {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 56px clamp(22px, calc(2.4 * var(--uvw)), 40px);
        align-items: start;
        margin-top: var(--sec-head);
      }
      /* the client video (the service page's card, user 2026-11-23): only the video, no quote, one "Play video"
         button in the bottom-right notch. The card rests at the service
         card's height; play opens it to 16:9 (never taller than the screen), close folds it back. */
      .csv {
        padding-top: var(--sec-y);
      }
      /* over the video, the service card's black label lines: the person's name, then their words (smaller) (user) */
      .csv .vt-q {
        font-size: var(--fs-h3);
      }
      .vt-d {
        max-width: 34rem;
        margin: 10px 0 0;
        font-size: var(--fs-h5);
        font-weight: 500;
        letter-spacing: -0.02em;
        line-height: 1.5;
      }
      .vt-d span {
        padding: 0.12em 0.4em;
        border-radius: 10px;
        background: var(--ink);
        color: #fff;
        -webkit-box-decoration-break: clone;
        box-decoration-break: clone;
      }
      /* the treatments we booked (inspo: a staggered photo row; our type, radius and motion). The head sits top-left
         over the first two columns; four photos of different heights: 1 and 2 sit on the baseline, 3 rises beside the
         head, 4 hangs from the top. A short caption under each. They enter one by one from the left. */
      .cst {
        padding: var(--sec-y) 0;
      }
      .cst-g {
        display: grid;
        grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr) minmax(0, 1.7fr) minmax(0, 1.6fr);
        grid-template-rows: auto auto;
        gap: clamp(24px, calc(2.4 * var(--uvw)), 44px) clamp(12px, calc(1.2 * var(--uvw)), 22px);
        max-width: var(--max);
        margin-inline: auto;
      }
      .cst-hd {
        grid-column: 1 / 3;
        grid-row: 1;
        align-self: start;
      }
      .cst-hd .eyb {
        margin-bottom: 20px;
      }
      .cst-hd p:not(.eyb) {
        max-width: 30rem;
        margin-top: 20px;
        font-size: var(--fs-lead);
        line-height: 1.45;
        color: var(--grey);
      }
      .cst-hd .cta {
        margin-top: 28px;
      }
      .cst-i {
        margin: 0;
      }
      .cst-m {
        overflow: hidden;
        border-radius: var(--r-card);
        background: var(--soft);
      }
      .cst-m img {
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .cst-i figcaption {
        margin-top: 12px;
        font-size: var(--fs-small);
        color: var(--grey);
      }
      .cst-i:nth-of-type(1) {
        grid-column: 1;
        grid-row: 2;
        align-self: end;
      }
      .cst-i:nth-of-type(1) .cst-m {
        aspect-ratio: 9 / 16;
      }
      .cst-i:nth-of-type(2) {
        grid-column: 2;
        grid-row: 2;
        align-self: end;
      }
      .cst-i:nth-of-type(2) .cst-m {
        aspect-ratio: 5 / 6;
      }
      .cst-i:nth-of-type(3) {
        grid-column: 3;
        grid-row: 1 / 3;
        align-self: end;
      }
      .cst-i:nth-of-type(3) .cst-m {
        aspect-ratio: 9 / 10;
      }
      .cst-i:nth-of-type(4) {
        grid-column: 4;
        grid-row: 1 / 3;
        align-self: start;
      }
      .cst-i:nth-of-type(4) .cst-m {
        aspect-ratio: 1 / 1;
      }
      @media (max-width: 1199px) {
        /* tablets and phones: the head on its own row, the photos in one row below, all one shape, no offsets */
        .cst-g {
          grid-template-columns: repeat(4, minmax(0, 1fr));
        }
        .cst-hd {
          grid-column: 1 / -1;
        }
        .cst-g .cst-i {
          grid-column: auto;
          grid-row: auto;
          align-self: start;
        }
        .cst-g .cst-i .cst-m {
          aspect-ratio: 4 / 5;
        }
        .cso {
          grid-template-columns: 1fr;
        }
        .cso-r {
          padding-top: 0;
          max-width: 640px;
        }
      }
      /* phones: no notch; the clinic and the H1, then the banner */
      @media (max-width: 899px) {
        .csh-w {
          display: flex;
          flex-direction: column;
          padding-top: 0;
        }
        .csh-tab {
          position: static;
          max-width: none;
          padding: 0;
          margin-bottom: 24px;
        }
        .cso-m {
          grid-template-columns: 1fr 1fr;
        }
        .csn-g {
          grid-template-columns: 1fr;
        }
        .csv {
          padding-top: 72px;
        }
        .csv .vt-q {
          font-size: 22px;
        }
        .vt-d {
          font-size: var(--fs-small);
        }
        /* phones: the head, then the photos two by two, all one shape */
        .cst-g {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }
      }
"""
style_out = bs.style.replace('    </style>', bs.PAGE_CSS + bc.PAGE_CSS + CASE_CSS + '    </style>')

# ---------------- script: the service page's, with the hero notch moved to the top-right and the case cards' notch ----
JS = bs.JS
JS = JS.replace('        gsap.set(".hp", { opacity: 0, y: 50 });\n        ScrollTrigger.batch(".hp", { start: "top 94%", once: true, onEnter: (b) => gsap.to(b, { opacity: 1, y: 0, duration: 1.1, ease: "expo.out", stagger: 0.08, clearProps: "opacity,transform" }) });\n\n        // client video: the card rises, the still settles, the quote and buttons follow\n        gsap.from(".vt-box", { y: 60, opacity: 0, duration: 1.3, ease: "expo.out", scrollTrigger: st(".vt", "top 85%") });\n        gsap.from(".vt-media img", { scale: 1.25, duration: 1.8, ease: "expo.out", scrollTrigger: st(".vt", "top 85%") });\n        gsap.from([".vt-say", ".vt-play", ".vt-tab"], { y: 20, opacity: 0, duration: 1, ease: "power3.out", stagger: 0.1, delay: 0.4, scrollTrigger: st(".vt", "top 85%"), clearProps: "opacity,transform" });\n', '')  # no video card on the case pages
def rep(a, b):
    global JS
    assert JS.count(a) == 1, a[:70]
    JS = JS.replace(a, b)

VID_JS = '        /* ---------- client video: the bottom-right notch for "Play video", and play opens the card, close folds it back ---------- */\n        {\n          const box = $("#vtBox"),\n            tab = $(".vt-tab"),\n            sec = box.closest(".vt");\n          const cut = () => {\n            if (sec.classList.contains("is-on") || getComputedStyle(tab).position !== "absolute") return void (box.style.clipPath = "");\n            const W = box.offsetWidth,\n              H = box.offsetHeight,\n              R = parseFloat(getComputedStyle(box).borderTopLeftRadius) || 28,\n              r = R,\n              g = Math.round(12 / (parseFloat(getComputedStyle(document.documentElement).zoom) || 1)),\n              tw = tab.offsetWidth + g,\n              th = tab.offsetHeight + g,\n              p = Math.min(tab.offsetHeight / 2 + g, th - r); // concentric with the pill: the gap stays g all the way round\n            box.style.clipPath = `path("M${R},0 H${W - R} A${R},${R} 0 0 1 ${W},${R} V${H - th - r} A${r},${r} 0 0 1 ${W - r},${H - th} H${W - tw + p} A${p},${p} 0 0 0 ${W - tw},${H - th + p} V${H - r} A${r},${r} 0 0 1 ${W - tw - r},${H} H${R} A${R},${R} 0 0 1 0,${H - R} V${R} A${R},${R} 0 0 1 ${R},0 Z")`;\n          };\n          cut();\n          new ResizeObserver(cut).observe(box);\n          new ResizeObserver(cut).observe(tab);\n          const go = $(".vt-go"),\n            media = $(".vt-media", box),\n            still = $("img", media),\n            x = $(".vt-x", box);\n          let frame = null;\n          const play = () => {\n            if (frame) return;\n            sec.classList.add("is-on");\n            cut();\n            x.tabIndex = 0;\n            // open to 16:9, but never taller than the screen (the root zoom turns screen px into CSS px)\n            const z = parseFloat(getComputedStyle(root).zoom) || 1;\n            const to = Math.max(box.offsetHeight, Math.min((box.offsetWidth * 9) / 16, (innerHeight * 0.86) / z));\n            if (motion) gsap.to(box, { height: to, duration: 0.9, ease: "expo.inOut" });\n            else box.style.height = to + "px";\n            frame = document.createElement("iframe");\n            frame.src = box.dataset.embed;\n            frame.allow = "autoplay; fullscreen; encrypted-media; picture-in-picture";\n            frame.allowFullscreen = true;\n            frame.referrerPolicy = "strict-origin-when-cross-origin";\n            frame.title = "Client video";\n            media.appendChild(frame);\n            still.style.opacity = "0";\n            x.focus({ preventScroll: true });\n          };\n          const stop = () => {\n            if (!frame) return;\n            frame.remove();\n            frame = null;\n            still.style.opacity = "";\n            sec.classList.remove("is-on");\n            x.tabIndex = -1;\n            // fold back to the height set in the CSS\n            const cur = box.style.height;\n            box.style.height = "";\n            const hh = box.offsetHeight;\n            box.style.height = cur;\n            if (motion) gsap.to(box, { height: hh, duration: 0.9, ease: "expo.inOut", clearProps: "height", onComplete: cut });\n            else box.style.height = "";\n            cut();\n            go.focus({ preventScroll: true });\n          };\n          $(".vt-play").addEventListener("click", play);\n          go.addEventListener("click", play);\n          x.addEventListener("click", stop);\n          addEventListener("keydown", (e) => e.key === "Escape" && stop());\n        }\n\n'
i = JS.index('        /* ---------- service banner: cut the notch for the button ---------- */')
j = JS.index('        /* ---------- client video:')
JS = JS[:i] + '''        /* ---------- case hero: cut the banner's top-right corner around the clinic and the H1 ----------
           The text block starts above the banner, so the notch is as deep as the part of the block that reaches into
           the banner. Curves = the banner's radius. Phones: no notch. */
        {
          const box = $("#svb"),
            tab = $(".csh-tab");
          const cut = () => {
            if (getComputedStyle(tab).position !== "absolute") return void (box.style.clipPath = "");
            const W = box.offsetWidth,
              H = box.offsetHeight,
              R = parseFloat(getComputedStyle(box).borderTopLeftRadius) || 28,
              r = R,
              g = 10,
              tw = tab.offsetWidth + g,
              th = Math.max(2 * r, tab.offsetHeight + g - box.offsetTop);
            box.style.clipPath = `path("M${R},0 H${W - tw - r} A${r},${r} 0 0 1 ${W - tw},${r} V${th - r} A${r},${r} 0 0 0 ${W - tw + r},${th} H${W - R} A${R},${R} 0 0 1 ${W},${th + R} V${H - R} A${R},${R} 0 0 1 ${W - R},${H} H${R} A${R},${R} 0 0 1 0,${H - R} V${R} A${R},${R} 0 0 1 ${R},0 Z")`;
          };
          cut();
          new ResizeObserver(cut).observe(box);
          new ResizeObserver(cut).observe(tab);
          document.fonts && document.fonts.ready.then(cut);
        }

''' + bc.JS[bc.JS.index('        /* ---------- the notches:'):bc.JS.index('        /* ---------- the video card opens')] + VID_JS + JS[JS.index('        /* ---------- reviews: the cards keep their share'):]

# hero: the service banner's order: the photo rises and settles, then the notch's content (clinic + H1, the home
# heading mask rise) and the glass numbers come in
rep('''          .from(".svh-top .eyb", { y: 14, opacity: 0, duration: 0.9, ease: "power3.out" }, 0.1)
          .from("#svc-title .ln-m > span", { yPercent: 110, duration: 1.2, ease: "expo.out", stagger: 0.09 }, 0.15)
          .from(".svh-txt p", { y: 18, opacity: 0, duration: 1, ease: "power3.out", stagger: 0.1 }, 0.4)
          .from(".svb", { y: 60, opacity: 0, duration: 1.3, ease: "expo.out" }, 0.45)
          .from(".svb-img img", { scale: 1.25, duration: 1.8, ease: "expo.out" }, 0.45)
          .from([".svb-tab", ".svb-stat"], { y: 16, opacity: 0, duration: 0.9, ease: "power3.out", stagger: 0.1 }, 1);''',
'''          .from(".svb", { y: 60, opacity: 0, duration: 1.3, ease: "expo.out" }, 0.25)
          .from(".svb-img img", { scale: 1.25, duration: 1.8, ease: "expo.out" }, 0.25)
          .from(".csh-tab .eyb", { y: 16, opacity: 0, duration: 0.9, ease: "power3.out" }, 0.8)
          .from("#case-title .ln-m > span", { yPercent: 110, duration: 1.2, ease: "expo.out", stagger: 0.09 }, 0.85)
          .from(".svb-stat", { y: 16, opacity: 0, duration: 0.9, ease: "power3.out" }, 1);''')
rep('''        gsap.from([".svs-l > *", ".svs > div:last-child > *"], { y: 30, opacity: 0, duration: 1.1, ease: "expo.out", stagger: 0.08, scrollTrigger: st(".svs", "top 86%") });''',
    '''        gsap.from([".cso .eyb", ".cso-r > *"], { y: 30, opacity: 0, duration: 1.1, ease: "expo.out", stagger: 0.08, scrollTrigger: st(".cso", "top 86%") });
        gsap.from(".vt-box", { y: 60, opacity: 0, duration: 1.3, ease: "expo.out", scrollTrigger: st(".vt", "top 85%") });
        gsap.from(".vt-media img", { scale: 1.25, duration: 1.8, ease: "expo.out", scrollTrigger: st(".vt", "top 85%") });
        gsap.from([".vt-play", ".vt-tab"], { y: 20, opacity: 0, duration: 1, ease: "power3.out", stagger: 0.1, delay: 0.4, scrollTrigger: st(".vt", "top 85%"), clearProps: "opacity,transform" });''')
rep('''        gsap.from([".help-hd .eyb", ".help-hd .cta"], { y: 16, opacity: 0, duration: 0.9, ease: "power3.out", stagger: 0.1, scrollTrigger: st(".help-hd", "top 88%") });''',
    '''        $$(".help-hd").forEach((hd) => gsap.from($$(".eyb, .cta", hd), { y: 16, opacity: 0, duration: 0.9, ease: "power3.out", stagger: 0.1, scrollTrigger: st(hd, "top 88%") }));
        // case cards: the photo rises and settles once the card is well in view, then the notch's button fades in
        gsap.set(".wk", { opacity: 0, y: 60 });
        gsap.set(".wk-cta", { opacity: 0, y: 16 });
        ScrollTrigger.batch(".wk", {
          start: "top 72%",
          once: true,
          onEnter: (b) => {
            gsap.to(b, { opacity: 1, y: 0, duration: 1.3, ease: "expo.out", stagger: 0.1, clearProps: "opacity,transform" });
            gsap.from(b.flatMap((c) => $$(".wk-media > img", c)), { scale: 1.25, duration: 1.8, ease: "expo.out", stagger: 0.1 });
            gsap.to(b.flatMap((c) => $$(".wk-cta", c)), { opacity: 1, y: 0, duration: 0.9, ease: "power3.out", stagger: 0.1, delay: 0.55, clearProps: "opacity,transform" });
          },
        });''')
rep('''        gsap.set(".fq", { opacity: 0, y: 30 });
''', '')
rep('''        ScrollTrigger.batch(".fq", { start: "top 94%", once: true, onEnter: (bt) => gsap.to(bt, { opacity: 1, y: 0, duration: 0.9, ease: "power3.out", stagger: 0.06 }) });
''', '')

def cta(label, href, cls='cta mag'):
    return (f'<a class="{cls}" href="{href}"><span class="cta-t">{label}</span><span class="cta-i">'
            '<i class="ph ph-arrow-right" aria-hidden="true"></i><i class="ph ph-arrow-right" aria-hidden="true"></i></span></a>')

def ld_txt(c, url):
    slug, clinic, ret, title, img = c[:5]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": f"{clinic}: {title}", "image": f"https://dentalmediacorp.com/assets/img/{img}", "url": url,
         "author": {"@type": "Organization", "name": "Dental Media Corp", "url": "https://dentalmediacorp.com/"},
         "publisher": {"@type": "Organization", "name": "Dental Media Corp", "url": "https://dentalmediacorp.com/"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://dentalmediacorp.com/"},
            {"@type": "ListItem", "position": 2, "name": "Case Studies", "item": "https://dentalmediacorp.com/case-studies/"},
            {"@type": "ListItem", "position": 3, "name": clinic, "item": url}]}]}
    return json.dumps(ld, ensure_ascii=False, indent=2).replace('\n', '\n      ')

def render(k):
    c = bc.CASES[k]
    slug, clinic, ret, title, img, alt, w, h, tags = c
    s = STORY[slug]
    rev, spend = title.split(' in revenue from a ')
    spend = spend.replace(' ad spend', '')
    url = f"https://dentalmediacorp.com/case-studies/{slug}/"
    e = html.escape
    nxt = [bc.CASES[(k + 1) % len(bc.CASES)], bc.CASES[(k + 2) % len(bc.CASES)]]
    lg, lw, lh = s['logo']
    desc = f"How Dental Media Corp turned a {spend} ad spend into {rev} in accepted treatment for {clinic}."
    return f'''<!doctype html>
<html lang="en-CA">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{e(clinic)} Case Study: {rev} in Revenue | Dental Media Corp</title>
    <meta name="description" content="{e(desc)}" />
    <link rel="canonical" href="{url}" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <meta name="theme-color" content="#0F1716" />
    <meta property="og:type" content="article" />
    <meta property="og:site_name" content="Dental Media Corp" />
    <meta property="og:title" content="{e(clinic)}: {e(title)}" />
    <meta property="og:description" content="{e(desc)}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:locale" content="en_CA" />
    <meta name="twitter:card" content="summary_large_image" />
{bs.head_links}
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/bold/style.css" />

    <script type="application/ld+json">
      {ld_txt(c, url)}
    </script>
{style_out}
  </head>
  <body>
    <a class="skip" href="#main">Skip to content</a>
{bs.symbols}

    <!-- ============ HEADER (Elementor: Theme Builder > Header, shared with the home page) ============ -->
{bc.header}

    <!-- ============ MOBILE MENU ============ -->
{bc.mnav}
    <main id="main">
      <!-- ============ 1. CASE HERO (inspo: madebyshape.co.uk/work/this-is-digital, our components) ============
           Elementor: Single "Case Study" template. ACF: clinic, headline (2 lines), photo, revenue, return.
           The clinic and the H1 in a notch the script cuts into the banner's top-right corner; the home glass numbers on
           the photo. Row 2: H2 | intro + Client / Service / Ad spend. -->
      <section class="svh" aria-labelledby="case-title">
        <div class="wrap">
          <div class="svh-in">
            <div class="csh-w">
              <div class="csh-tab">
                <p class="eyb">{e(clinic)}</p>
                <h1 class="t-h1" id="case-title">
                  <span class="ln-m"><span>{rev} in revenue</span></span>
                  <span class="ln-m"><span>from a {HL.format(spend + ' ad spend.')}</span></span>
                </h1>
              </div>
              <div class="svb csb" id="svb">
                <div class="svb-img"><img src="assets/img/{img}" alt="{e(alt)}" width="{w}" height="{h}" style="--pos: {POS.get(slug, '50% 50%')}; --pos-m: 50% 50%" fetchpriority="high" decoding="async" /></div>
                <div class="h-stat svb-stat">
                  <div class="h-num"><b><em>{rev}</em></b><small>In accepted treatment</small></div>
                  <div class="h-num"><b><em>{ret}</em></b><small>Return on ad spend</small></div>
                </div>
              </div>
            </div>
            <div class="cso">
              <div>
                <p class="eyb">The project</p>
                <h2 class="t-h2">
                  <span class="ln-m"><span>{s['o1']}</span></span>
                  <span class="ln-m"><span>{s['o2']}</span></span>
                </h2>
              </div>
              <div class="cso-r">
                <p>{e(s['intro'])}</p>
                <dl class="cso-m">
                  <div><dt>Client</dt><dd>{e(clinic)}</dd></div>
                  <div><dt>Service</dt><dd>Dental Marketing</dd></div>
                  <div><dt>Ad spend</dt><dd>{spend}</dd></div>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============ 2. CLIENT VIDEO (the service page's card: only the video and "Play video", user)
           Elementor: Container + HTML widget. ACF: video embed URL (data-embed), cover still.
           16:9 from the start; a click plays the video inside the card, the x (top-left) or Escape closes it. -->
      <section class="vt csv" aria-label="Client video">
        <div class="wrap">
          <div class="vt-in">
            <div class="vt-w">
{video_html(slug)}              <div class="vt-tab">
                <button class="cta vt-go" type="button"><span class="cta-t">Play video</span><span class="cta-i"><i class="ph-fill ph-play" aria-hidden="true"></i><i class="ph-fill ph-play" aria-hidden="true"></i></span></button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div class="sbreak" aria-hidden="true"></div>

      <!-- ============ 4. REVIEWS (the home hero's moving cards) ============ -->
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
{bs.reviews}        </div>
      </section>

      <div class="sbreak" aria-hidden="true"></div>

      <!-- ============ 5. WHAT NEXT: two more case cards (the case-studies card) + Browse all case studies ============ -->
      <section class="help csn" aria-labelledby="csn-title">
        <div class="wrap">
          <div class="help-in">
            <div class="help-hd">
              <div>
                <p class="eyb">More results</p>
                <h2 class="t-h2" id="csn-title">
                  <span class="ln-m"><span>What next?</span></span>
                  <span class="ln-m"><span>More clinics, <span class="hl">more patients.</span></span></span>
                </h2>
              </div>
              {cta('Browse all case studies', 'case-studies.html')}
            </div>
            <div class="csn-g">
{bc.case_html(nxt[0], 1)}
{bc.case_html(nxt[1], 2)}
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- video lightbox: the review cards' play buttons fill it with a YouTube embed -->
{bs.vbox}
    <div class="sbreak" aria-hidden="true"></div>
    <!-- ============ FOOTER (shared with the home page) ============ -->
{bc.footer}

    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>{JS}
  </body>
</html>
'''

if __name__ == '__main__':
    for k, c in enumerate(bc.CASES):
        page = render(k)
        f = page_file(c[0])
        page = preloader.inject(page)
        open(f, 'wb').write(page.replace('\n', '\r\n').encode('utf-8'))
        print('ok', f, len(page.splitlines()))
