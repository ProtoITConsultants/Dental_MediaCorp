---
name: dmc-design
description: The Dental Media Corp landing page design system (index.html), covering tokens, type, colour rules, components, motion vocabulary, hover rules, responsive behaviour and the verify loop. Load it before ANY design, layout, animation, copy-placement or new-section change to this site, and update it whenever a design decision changes.
---

# Dental Media Corp: design system and working rules

The client is strict and detail-driven. They want **minimal, calm, expensive-feeling** design in which every dimension and every animation is smooth and intentional. Before building, study what the page already does and **extend that vocabulary. Never introduce a new one.** If a request seems to need a new pattern, first look for the closest existing one below and adapt it.

The parts the client explicitly loves, which are the benchmark for anything new:
- **Navbar:** frosted glass after scroll, centred links with a hairline underline that wipes in, and a pink pill CTA.
- **"Your complete dental marketing team":** white stat cards and a 3-piece mint puzzle with a live-drawn teal growth line.
- **"Real clinics, real results":** white cards. On hover the photo slides up, the logo shows, and the results fade in.
- **"More than lead generation. The DMC Method":** the pinned mark on the left, numbered steps on the right, a line that fills as you scroll, and the active number turning pink.
- **"Book a free strategy call":** a white two-pane calendar card with mint day circles, pill time slots, and minimal type.
- **Hero reviews carousel:** glass cards drifting slowly, drag to scrub, video still with a white play circle opening a lightbox.

---

## 1. Files and conventions

- Everything lives in **one file: `index.html`**. CSS sits in the `<style>` in `<head>` (about lines 190 to 3500), markup in `<main>`, and the script at the bottom after GSAP, ScrollTrigger and Lenis (CDN).
- **CRLF line endings.** If you rewrite the file with a script, write it back with `\r\n`.
- CSS is grouped by `/* ---------- N. section ---------- */` blocks. Keep new CSS inside the block of the section it belongs to, and put its responsive overrides in the shared media blocks near the end of the style tag (`max-width: 1199px`, `max-width: 899px`, `hover: none`).
- Comments explain **why** in plain words (e.g. "colour only: a transform transition here froze the GSAP scale-in"). Keep that voice.
- Every section carries an `<!-- Elementor: ... -->` comment saying how it maps to Elementor (Container / Loop Grid / Loop Carousel / HTML widget, and the ACF fields). Add one for every new section or component.
- Icons: **Phosphor** (`ph ph-*` regular, `ph-fill ph-*` fill). No other icon set.
- Assets: `assets/img/...`, webp (quality around 88, `method=6`).
- **Image quality is a client requirement.** A photo's source must be at least **1.6× its largest displayed CSS width** (2× is ideal) so it stays sharp on retina screens (e.g. a photo shown at 680px needs a source of at least 1100px). Never use video stills or anything soft at the source, and never upscale: crop at native resolution instead. Before swapping images, check a 2× (`deviceScaleFactor: 2`) screenshot of the element. Set `width` and `height` to the real file size.
- Run it with Live Server on port 5501 (`.vscode/settings.json`), or open the file directly.

## 2. Tokens (`:root`): always use these, never one-off values

**Colour**
| token | value | use |
|---|---|---|
| `--bg` | #f7f7f7 | page background (every section sits on it; no coloured section bands) |
| `--ink` | #0d1312 | text, dark pills, dark round buttons |
| `--body` | #56625f | descriptions, body copy |
| `--grey` | #8b9693 | hero subline, case subline, counters |
| `--line` | #e3e8e5 | card borders (FAQ) |
| `--soft` | #ecefec | image placeholder fill |
| `--teal` | #1b7f73 | brand: accent words, numbers, lines, active hairlines |
| `--teal-2` / `--teal-3` | #2a9488 / #49b8a6 | focus ring, teal on dark |
| `--mint` / `--mint-2` | #ddf2ec / #bfe6dc | soft fills: FAQ icon, calendar days, puzzle, glows |
| `--deep` | #123b36 | hover state of dark pills, deep teal text |
| `--acc` | #ff9fc4 (pink) | **statement only**: arrow circles, the nav CTA, `.sh-rule`, the highlighted stat, the active FAQ icon |
| `--acc-hover` | #ffbfd7 | hover of pink fills |
| `--acc-mid` | #f06a9f | the **active** number (DMC Method, services), stars, quote icon |
| `--acc-ink` / `--acc-deep` | #b33a6b / #5c1434 | pink text on light, text on the pink card |
| `--acc-on` | ink | text and arrows sitting on pink |

**Colour rules**
- The base is white cards on #f7f7f7. Teal carries the structure; pink is a **small** accent, at most a few pink things in view at once.
- Never flood a row or card with teal or pink on hover, and never flip text to white on a light section. (That was the old services hover and it was removed for exactly this reason.)
- Glows (`.sbreak`, the hero, `.mtooth::before`) are soft radial mint plus pink and heavily blurred. Do not add hard gradients.

**Type**: Satoshi (400/500/700/900) for everything, plus Instrument Serif *italic* for the accent words (`.hl`, teal, 1.1em).
| token | size | use |
|---|---|---|
| `--fs-h1` | 44 to 78px (hero overrides to 38 to 68) | hero headline only |
| `--fs-h2` | 34 to 58px | every section heading |
| `--fs-list` | 30 to 52px | DMC Method step titles |
| `--fs-h3` | 26 to 34px | services list names, big card titles, hero figures |
| `--fs-h4` | 24px | card titles (case study, booking title) |
| `--fs-h5` | 20px | names, FAQ questions, small titles, photo captions |
| `--fs-lead` | 18 to 21px | intros under headings, stat labels, step text |
| `--fs-body` | ≥17px | descriptions, buttons, quotes |
| `--fs-small` | ≥15px | labels, nav dropdown, meta, numbers in lists |
| `--fs-xs` | ≥14px | tags, legal, captions |
| `--fs-stat` | 48 to 76px | big numbers |
- Headings: weight 700, letter-spacing -0.035em, line-height 1.09. Titles: weight 600, -0.035em (big) or -0.02em (small).
- Body line-height is 1.5 to 1.6. Numbers use `font-variant-numeric: tabular-nums`.
- Small sizes are written `max(Npx, calc(Mpx / var(--z)))` so they never drop below a readable size when the laptop zoom (below) scales the page.

**Spacing**: `--sec-y` 112px (72px on phones) above and below every section; `--sec-head` 64px (40px) from heading to content; `--pad-card` 24px (20px); `--pad-panel` 36px (24px).
**Frame**: `--side` is the gutter (20 to 80px); `--max` is the content width. Content blocks use `max-width: var(--max); margin-inline: auto` inside `.wrap`.
**Radius**: `--r-card` 28px (38px under `corner-shape: squircle`); `--r-inner` = card − 6px, for anything set 6px inside a card (**concentric corners**); `--r-pill` for every button and chip. Add new rounded surfaces to the `@supports (corner-shape: squircle)` list.
**Buttons**: `--btn` 48px (44px on phones) round icon buttons; `--btn-lg` 62px for the big carousel arrows.
**Ease**: `--ease: cubic-bezier(0.16, 1, 0.3, 1)` is the only CSS easing (expo-out). GSAP uses `expo.out` for entrances, `power3.out` for small lifts, and `expo.inOut` for wipes and rules.

## 2b. Copy voice (client brief, 2026-11-18)

The client loves the design; the copy must **sell the experience of being a DMC client, not the machinery behind DMC**. The reaction we want from a dentist:

> "Wait, you create the ads, film the videos, contact the leads, qualify the patients, and book them into my schedule? And my team just focuses on the patients who come in? That's exactly what I need."

That end-to-end handover is DMC's biggest competitive advantage, and **every section should reinforce it**.

- **Write "we do it for you":** we create, film, call, qualify, book. **Your team** just sees the patients. Speak to the dentist ("your schedule", "your team", "your front desk").
- **Never show process mechanics:** no speed-to-lead times (2 min), deposit amounts ($50), credit-score thresholds (660+), show-up percentages tied to deposits (80%+), "setters", "financial screening". Removed from the hero, stats, services, DMC Method, FAQ and the JSON-LD on 2026-11-18. Don't bring them back.
- **Outcome proof is fine:** consultations attended (5,000+), accepted treatment ($10M+), case-study revenue and ROAS, testimonials. These are the dentist's results, not our mechanics.
- **Keep the visible FAQ and the FAQPage JSON-LD in `<head>` identical** (questions and answers). Search engines read the JSON-LD.
- Current anchors: hero "We find your patients, / call them and *book them.* / Your team just treats / the ones who walk in." Subline: "We create the ads, film the videos, call every lead and book qualified patients into your schedule." Stats cards read as one sentence: Ads, Videos, Leads, Schedule → (pink) Patients. The DMC Method is the client's journey: we create your campaigns → we contact every lead → we book them into your schedule → your team sees the patients.

## 3. Component vocabulary (reuse these)

- **Section head `.sh`**: centred h2 in two masked lines, `<span class="ln-m"><span>Sans line</span></span>` then `.sh-l2` holding the pink `.sh-rule` bar and the italic `.hl` line. Every section heading follows this pattern.
- **Primary CTA `.cta`**: a 62px ink pill containing a pink 48px circle with **two arrows**. On hover the pill goes `--deep` and the first arrow slides out while the second slides in. Variants are `.teal` and `.light`. Add `.mag` for the magnetic pull (fine pointers only).
- **Arrow circle**: the same two-arrow swap (`i + i` positioned off-canvas, translate in on the active state). In lists it rests as a **hairline ring** and fills pink only when active.
- **White card**: `#fff`, `--r-card`, a 1px `rgba(13,19,18,.08)` border or a very soft long shadow (`0 30px 60px -44px rgba(13,19,18,.4)`). A photo inside it sits **6px in** with `--r-inner` (case studies, services photo card).
- **Glass**: `rgba(247,247,247,.62)` + `backdrop-filter: blur(18px) saturate(160%)` + a 1px white border. Use it only over imagery or glows (nav, hero badges, review cards). Provide a `prefers-reduced-transparency` fallback.
- **Hairline list**: rows separated by `1px rgba(13,19,18,.1)` borders, a small teal tabular number, a title, and the text under it (DMC Method, services, FAQ rhythm).
- **Mint chip / icon**: a mint circle with a teal icon (FAQ). It turns pink with ink when active.
- **Placeholder `.phx`**: the image slot until real photos arrive.

## 4. Motion vocabulary (exact values; match them)

**Entrances (GSAP + ScrollTrigger, `once: true`)**
- Headings: `.ln-m > span` from `yPercent: 110`, 1.2s `expo.out`, stagger 0.09, start `top 86%`.
- `.sh-rule`: `scaleX` from 0, 1.4s `expo.inOut`.
- Rows and cards: from `y: 50 to 60, opacity: 0`, 1.1s `expo.out`, `ScrollTrigger.batch` with stagger 0.1. Use `clearProps` when CSS transitions also act on the element.
- Carousels: cards from `x: 120`, 1.3s `expo.out`, stagger 0.08; photos settle from `scale: 1.25 to 1.35`, 1.8s.
- Counters: `data-to` / `data-suf` count up over 1.8s `power3.out`.
- The puzzle: pieces fly in rotated, then the line draws with a pen dot (`power1.inOut`, 1.3s) and the arrow appears. The whole thing is short (about 1.7s) so nobody waits.
- Card line drawings (`.rb-art`): every shape gets `pathLength=1`; strokes draw from `strokeDashoffset: 1` over 1.2s `power2.inOut` (stagger 0.04, from 0.35s), then fills fade in (`fillOpacity`, 0.6s, from 0.95s), triggered at `top 88%` of the card. JS-only, so with reduced motion they are simply there.

**Scroll-linked**: DMC line `scaleY` scrubbed; DMC mark rotates −7° to 7°; hero mark parallax `yPercent 14`; nav `.is-stuck` after 30px (height 84 to 68, glass fades in).

**Hover / active (CSS, `--ease`)**
- Text links: a 1px underline `scaleX(0 to 1)`. The origin swaps right to left so it wipes in from the left and out to the right (0.45s).
- White cards (stats): the border goes teal 0.45 (0.4s).
- Services carousel: the slide is 1s `--ease` (card width plus track transform). Photos stay perfectly still: the card reveals them; nothing zooms or blurs. The copy fades in after 0.45s. (Earlier list versions used a letter roll and a cursor pill; see the section map.)
- Cards: the image area changes height or position (0.7s), and secondary content fades in **after** a 0.2s delay (case studies).
- Photo swap: crossfade opacity 0.7s, and the incoming photo settles from `scale(1.06)` over 1.4s. Captions crossfade with an 8px rise.
- Buttons: colour 0.3 to 0.35s; icon translate 0.45s.

**Ambient**: review carousel drift (0.032px/ms, 4× slower on hover, drag to scrub, infinite clones); hero mark float (±14px, 4.2s sine) plus pointer follow; magnetic buttons.

**Motion rules**
- Smooth and slow-out (expo). Nothing bounces, spins or snaps, and nothing loops except the slow ambient drift and float.
- **Hover must never move layout** (no height changes that push other rows) and must never dim other items to near-invisible. Every item stays readable.
- In a list, keep **one active item at all times** and let it persist when the pointer leaves, so the state never flickers back.
- Never put a CSS `transform` transition on an element that GSAP also tweens: GSAP's inline transforms fight the transition. Wrap the element and animate the wrapper instead (e.g. `.sv-zoom` is tweened while the `img` transitions).
- `prefers-reduced-motion`: GSAP choreography, the preloader and Lenis are all skipped, and CSS durations drop to 0.01s. The page must look complete without JS animation.

## 5. Section map (top to bottom)

1. **Hero** `.hero`: a 4-line h1 with one `.hl` phrase; the side subline and CTA; the 3D mark in the background, masked at the bottom; glass badges (Google / Meta / HIPAA) plus glass stats (5,000+ / $10M+ with a pink highlighter); reviews carousel `.q` inside the hero (`#testimonials`). A preloader wipes up with a pink edge line.
   - **Review cards keep a fixed share of the screen on every desktop (≥1200px) and at any browser zoom** (client requirement, after theimplantengine.com's hero cards; behaviour only, our own design):
     - Design size is 540 × 270 at 1920 (28.13% × 14.06% of the screen width).
     - The script sets `--qs = innerWidth / 1920 / rootZoom` on `:root` (re-run on resize, which a browser zoom also fires), and `.q { zoom: var(--qs) }` scales the whole card, text included. The track gap is `16px × --qs`. **Measured on the screen, not the page box:** the user wants these cards, and only these, to keep their share of the *screen* (confirmed twice; do not change).
     - At ≥1200px the cards have a fixed `height: 270px` and the 1920 text sizes (`--fs-body` 17, `--fs-small` 15, `--fs-xs` 14, `--fs-h5` 20). The site's laptop text bump would otherwise make them taller on laptops.
     - The loop length is measured with `offsetLeft` of the first copy, and drag divides the pointer delta by the root zoom (1:1 with the pointer).
     - Below 1200px `--qs` is 1 and the phone/tablet layout is unchanged.
   - **No edge fade on the reviews row** (it read as blur on the first and last card). At ≥1921px the row runs edge to edge of the screen: `.hero { overflow-x: visible }`, and `.q-row` gets `margin-inline: −var(--bleed)` and `padding-left: var(--bleed) + var(--side)`, so the first card still lines up with the content.
   - The hero, nav and services caps are `max-width: calc(1920px / var(--z))` (1920 *screen* px). A plain 1920px was capped early under the laptop zoom, leaving gaps at the screen edges.
2. **Team / numbers** `.team #about`: a 4-col grid `.rs` holding cards `.rb` (big word bottom-right, label top-left, one pink gradient card `.rb-5`) and puzzle pieces `.pz-1..3`. Phones get a 2-col named grid. Since 2026-11-18 the cards hold words, not stats (Ads / Videos / Leads / Schedule / pink Patients; see Copy voice). `.rb` is a size container and the word is `min(var(--fs-stat), 16cqw)` (`min(44px, 16cqw)` on phones), so the longest word fits a narrow card. No count-up (`data-to`) on these cards any more. **Each card has a bold tone-on-tone glyph `.rb-art`** (user-approved 2026-11-19, after a Dribbble set of tone-on-tone category cards): inline SVG, viewBox 160×160, one simple icon per card in thick rounded strokes (`stroke-width: 12`) with a soft fill (`.f`) and dots (`.d`). The icons are Ads = megaphone with sound waves, Videos = a frame with a play button, Leads = a chat bubble with three dots, Schedule = a calendar with a tick, and Patients = two people. Colour comes from `--rb-ic` / `--rb-fill`: pale teal 0.13 / 0.045 on the white cards, and pink 0.4 / white 0.24 on the pink card. Placement: upright (no tilt, no blur), `width: 62%`, `top: −9%`, `right: −11%`, cropped by the card's edge; the big word owns the bottom-right. On hover the glyph nudges into the card (`translate(−6px, 6px) scale(1.04)`, 0.9s) and its colour deepens (0.2 teal, 0.55 pink, 0.6s). Below 1200px it is 58% wide. It draws in on scroll (see the motion vocabulary). Rejected along the way: thin hairline drawings centred like stickers; the same drawings big, tilted and feathered in alternating corners; and those drawings placed upright at the right edge.
3. **Services** `.svc #services`: **CURRENT = the services carousel `.sx`**, after the user's reference "Carousel experimentation" by Sacha Jerrems (Dribbble 11431212), adapted to the brand. It sits outside `.wrap` (full width, max 1920).
   - **Sizing:** everything derives from `--sx-h` (clamp 460 to 600px; 460px on phones). Active card `--sx-big` = 1.5×h, strips `--sx-small` = 0.55×h, gap 24px. On phones the active card fills the width less a 48px peek, and strips are 120px.
   - **Slide:** the track moves `translate3d(calc(--sx-x0 − --j × (small + gap) + --dx))`, because every card left of the active one is a strip. Card `width` and track `transform` both transition over 1s `--ease`. **Photos are static (user request):** each `img` is fixed at `--sx-big` × `--sx-h`, centred (`left: 50%; translateX(-50%)`), so the card is a window that reveals more of a still photo as it opens. No zoom, no blur, and no `width: 100%` + `object-fit` (that re-crops the photo as the card resizes, which reads as a zoom).
   - **Copy:** the name keeps the strip's width in both states, so it never re-wraps. The description and Explore link sit in a second column that the strip clips; they fade in after 0.45s.
   - **Overlay (legibility, user request 2026-11-19):** `.sx-card::after` = an ink gradient from the foot (0.9 → 0.72 at 26% → 0.36 at 52% → 0 at 76%) over a 0.16 ink tint on the whole photo. The name and line have a soft ink halo (`text-shadow` 0 2px 22px / 0 1px 16px), and the line is white 0.94. Tested on the brightest photo (Search Console).
   - **Chip:** dark glass with a pink number and the stage (Attract / Convert / Measure).
   - **Script "services carousel"**, via `go(i)`:
     - Sets `--j` and `.on`, re-tints the glow (`@property --sx-tint`, mint and pink alternating), and updates the counter, the progress bar `scaleX((j+1)/7)` and the arrows' disabled state.
     - **Cursor: the site's normal cursor** (user request: "stay simple as on the other sections"). The cards get `cursor: pointer`. No custom cursor: the ring was built, made section-wide, then removed.
   - **Inputs:** arrows, ←/→ keys, drag/swipe (60px threshold, the track follows at 0.55×), a click on a strip (it slides; only the active card follows its link), keyboard focus (only `:focus-visible`, since pointer focus would open the card before the click and the click would then navigate), and nav links (the `sx:go` event from `goTo`).
   - **Photos:** placeholders from `assets/img/v5` (1200px, about 1.33× the 900px card, below the 1.6× rule; replace with ≥1440px originals).
   - Card ids `#svc-*` and `#treatments` are kept.
   Previous version, a **letter-roll hover list with a cursor pill** (replaced the marquee below; the marquee details are kept only as history). Same hairline rows. Script "services: letter roll + cursor pill" splits each name into word windows `.sm-w` (inline-block, overflow hidden, so lines still wrap between words) and letters `.sm-c` (`--i` index). The link gets `aria-label` with the full name. Each letter carries a teal copy of itself via `text-shadow: 0 1.2em 0 var(--teal)`. On hover, focus or touch `.on`, the letters roll up by `translateY(-1.2em)` (0.75s `--ease`, 18ms apart). Fine pointers get `.sv-pill`, a fixed pink "Explore" pill with an ink arrow circle (the CTA inverted). It follows the pointer with `gsap.quickTo` (0.55s, divided by the laptop zoom), scales in with `expo.out` over a row, and the native cursor is hidden over rows. Active row: teal foot line, `--acc-mid` number, description to ink, arrow ring to ink with the swap. Hairlines still draw in on entrance; touch still activates the row crossing 58%.
   Previous version, a **marquee hover list**: No photos and no cards (the client's decision: cards sit above and below). `.sv-list` of hairline rows `.sm`: number | name (`--fs-list`) | one line (max 360px) | arrow ring; on phones the line drops under the name. The whole row is a link (stretched `.sm-link::after`; keep `h3` and `a` unpositioned). On hover (fine pointer) the name `.sm-t` slides up (`translateY(-105%)`, 0.7s) and the marquee `.sm-mq` slides in. The marquee is built by script: 8 copies of the name in the teal Instrument Serif italic, with pink dots, in two equal halves looping by −50% at about 70px/s. Margins, not `gap`, keep the loop seamless. At the same time the teal foot line draws in, the number turns `--acc-mid`, and the arrow ring fills pink with the swap. Even rows drift the opposite way (`animation-direction: reverse`). The arrow ring leans toward the pointer (clamped ±14px). Entrance: each row's top hairline (`.sm::before`) draws in from the left (`.in` class, 0.09s apart; the `sm-draw` root class is only set when motion runs), then number, name, line and arrow rise (y 28, 1s `expo.out`, stagger 0.05). Keyboard focus gives the line and number without the marquee. On touch, the row crossing 58% of the screen gets `.on`, the full hover state including the marquee, which runs along the first line of a wrapped name. Row ids `#svc-*` (and `#treatments` in row 1) are nav targets; do not rename them.
4. **Case studies** `.cases #results`: a horizontal snap row of `.cs` cards with prev/next arrows (`.arw`), drag, and a disclaimer note.
5. **DMC Method** `.meth #dmc`: `.mgrid` with 5fr and 7fr. The left mark is sticky (no `overflow: hidden` on ancestors!); the right holds `.mstep` items with `.mline` progress.
6. **Booking** `.book #contact`: the `.bk` widget, an info pane plus a calendar showing live LeadConnector slots, then a form step and a confirmation.
7. **FAQ** `.faq #faq`: an accordion with one open at a time and GSAP height animation.
8. **Footer** `.foot`: brand, link columns, a big contact line, legal.

Between sections: `<div class="sbreak" aria-hidden="true"></div>`, a blurred glow strip that alternates mint and pink.

## 6. Responsive

- Tuned at **1920px**. Laptops get the same picture scaled down: `zoom: 0.8` from 1200 to 1699px and `0.9` from 1700 to 1919px, with `--z` set to match. Always size with `var(--uvw)`, `var(--uvh)` and the related units (zoom-corrected `vw` and `vh`), never raw `vw` or `vh`.
- **The page box: centre the content, not the visuals** (user request). `<main>` is the centred parent of every section: `max-width: calc(1920px / var(--z))` (1920 *screen* px at any laptop zoom), `margin-inline: auto`, **no clipping**. On a wide screen or a zoomed-out browser the content stays together in the middle. The **visuals run full screen width**: the header's glass bar (its `.nav` content stays capped and centred), the section-break glows (`main > .sbreak` gets `margin-inline: −var(--bleed)`; the strip before the footer is already in the full-width body, so it must not), the services carousel `.sx` (`margin-inline: −var(--bleed)`, `--sx-x0 = bleed + side + 64px`, so the open card lines up with the content and strips run to the screen edge), and the hero reviews row (above). `--bleed` on `:root` = `(100·uvw − min(100·uvw, 1920px/z)) / 2`: how far the screen edge lies past the box (0 up to 1920 screen px). `body { overflow-x: clip }` plus correct bleeds keep sideways scroll at zero. Check `scrollWidth` at 2400 and 3840.
- At **1921px and up** the hero headline keeps growing up to its cap; content still sits inside the page box.
- At **≤1199px** the burger menu replaces the links.
- At **≤899px** (phones) the spacing tokens shrink, sections stack to one column, sticky pieces turn static, and secondary visuals hide.
- **Touch** (`hover: none` / `pointer: coarse`): never rely on hover. Show the hover-only content by default (case results, services photos and Explore buttons).
- No horizontal page scroll at any width (`body { overflow-x: clip }`; check `scrollWidth`).

## 7. Accessibility baseline

- Use the skip link, `aria-labelledby` on sections, `aria-hidden` on decorative visuals and duplicated content, and the teal `:focus-visible` ring (use `:has(:focus-visible)` for stretched-link rows).
- Keyboard focus must trigger the same active state as hover.
- Use real `alt` text for content photos and `alt=""` for decorative or duplicate ones. Give buttons `aria-label`s.

## 8. Workflow for any new request

1. Read this file, then the relevant CSS block and markup in `index.html`.
2. Name the existing pattern(s) the change will reuse (section 3) and the motion values it will use (section 4).
3. Build with tokens only, including the Elementor comment, responsive overrides, touch behaviour, reduced motion, and the squircle list.
4. **Verify visually.** Playwright-core drives the installed Chrome (`C:/Program Files/Google/Chrome/Application/chrome.exe`). Install `playwright-core` into the session scratchpad, not the repo. In the test only, stub out Lenis (`addInitScript(() => Object.defineProperty(window, "Lenis", { get(){}, set(){} }))`) so `scrollTo` works, wheel through the page once so every `once` reveal fires, then screenshot at **1920×1080, 1440×900 (laptop zoom) and 390×844 touch**, plus a hover state. Check for page errors and horizontal overflow.
5. Show the result, then **update this file**: tokens, patterns, the section map and the decision log below.

## 9. Decision log (keep appending)

- **2026-11-17: Services redesigned.** The old row hover (a teal fill wiping up, white text, other rows dimmed to 30%) and the full-width mint band clashed with the minimal system, so both were removed. The section is now a hairline list plus a sticky photo card. Active state: a teal foot line, a pink number, a 10px text nudge, and a pink arrow ring; the photo crossfades. Service names moved from `--fs-list` to `--fs-h3` because seven rows sit in a 7fr column.
- 2026-11-17: Services photos were swapped for sharp stock (`assets/img/services/hd/`) after "use good image quality". **Superseded the same day.**
- 2026-11-17: Tried expanding photo panels for services (seven slim panels, the active one opening with a photo and an auto-advancing timer line). **Rejected:** it didn't make sense to the client, and they don't want images in this section.
- 2026-11-17: Services as a no-image card grid (white cards with icon chips, a pointer-following mint light, and a pink "Not sure where to start?" card). **Rejected:** too many cards, since the stats section above and the case studies below are already cards.
- **2026-11-17: Services = the marquee hover list (current).** It keeps the original hairline list and replaces the teal row flood with the italic name marquee. The `hd/` photos were deleted; the old `services/svc-*.webp` and `dmc-*.webp` files remain, unused.
- 2026-11-17: Marquee list refined: hairlines draw in on entrance, alternating marquee direction, a magnetic arrow ring, and a scroll-driven active row on touch screens (phones previously had no interaction).
- 2026-11-17: The user wasn't satisfied with the marquee and asked for a luxury, award-site animation on the original list. **Now: letter roll plus cursor pill (current).** The marquee, its alternating direction and the magnetic arrow were removed.
- **2026-11-17: Services = the services carousel (current).** The user asked for the Dribbble "Carousel experimentation" animation with images, overriding the earlier "no images in services". It keeps the reference's mechanics: wide active card, strips, width-changing slide, directional motion blur, stretching ring cursor. The reference's full-page colour swap became the brand glow re-tint. Note: the case studies just below are also a horizontal card row; the user chose this knowingly. If they feel repetitive, differentiate the case studies, not this section.
- 2026-11-17: Carousel simplified at the user's request, to match the reference: photos are static and the card reveals them as it opens (fixed size, centred). The image zoom (1.12 → 1) and the motion blur were removed. Kept: the slide, the width change, the copy fade and the ring cursor. Lesson: when copying a reference, don't add effects it doesn't have.
- 2026-11-17: The ring cursor was made section-wide, then **removed at the user's request**: keep the normal cursor, like every other section. Lesson: no custom cursors on this site unless the user asks for one.
- 2026-11-17: Hero review cards locked to a fixed share of the screen on all desktops and browser zoom levels (before: 432×225 on laptops, 540×270 at 1920, other sizes in between). The edge fade at ≥1921px was removed; the row runs edge to edge. The 1920 caps became zoom-aware. Testing tip: a browser zoom equals a different CSS viewport width, so test widths 1200 to 2880 and compare `width / innerWidth`.
- 2026-11-17: **Page box.** First built as one box that clipped everything; the user rejected the boxed-in visuals and the review cards changing. **Final:** centre the content only. The visuals (glows, header bar, services carousel, hero reviews) break out to the full screen width via `--bleed`. The hero review cards follow the screen again (`innerWidth / 1920 / z`). Bug to remember: a negative-margin breakout on an element that is not inside the box (the last `.sbreak`, in `<body>`) doubles its width and adds a sideways scroll.
- **2026-11-18: Copy pass to the client brief** (see 2b Copy voice). Changed: the meta and OG description, the hero headline and subline, the five team cards (stats became the we-do-it sentence), the seven service lines, the four DMC Method steps (the DMC Network step was replaced by "Your team sees the patients"; consider giving the Network its own FAQ if the client wants it kept), the booking blurb, and FAQs 01, 02 and 04 plus their JSON-LD. Layout and design untouched.
- 2026-11-19: Line drawings added behind the five team cards (user request: "add svgs in the background according to ads, video, leads, schedule and patients"), in the puzzle's teal-and-mint hairline style, drawing in with the growth line. Desktop only.
- 2026-11-19: Services carousel overlay strengthened so the white text stands out on bright photos (deeper foot gradient, light whole-card tint, soft text halo).
- 2026-11-19: Card drawings changed from centred "stickers" to big tilted corner artwork (alternating top-right / bottom-left, cropped by the card, feathered and slightly soft, straightening on hover). Now shown at every size, quieter below 1200px.
- 2026-11-19: **Card icons final = bold tone-on-tone glyphs** in the top-right corner (after the user's tone-on-tone category-card reference; user-confirmed with a screenshot). The earlier thin drawings (sticker, tilted-corner and right-edge placements) were all replaced.
- Tooling lesson: in splice scripts, `re.subn(pattern, lambda m: rep, …)` inserts `rep` literally, so never put `\1` / `\2` in `rep` (that broke the page once). Use the match object, or rebuild the text yourself. Always re-run the page and check for script errors after a splice.
- **Lessons from the services rounds:**
  - Before designing a section, look at its neighbours and don't repeat their pattern. Cards: stats and case studies. Sticky steps: DMC Method. Accordion: FAQ. Horizontal row: case studies and reviews.
  - ~~No images in services.~~ Superseded: the user asked for images with the carousel. Always follow the newest explicit request.
  - "Creative" for this client means one memorable but quiet interaction on top of the approved vocabulary, not new mechanics (auto-advance, vertical text, expanding layouts).
  - When the user asks for a new direction, offer 2 or 3 named patterns (searchable names) before building.
- Earlier: Satoshi + Instrument Serif; Apple-style squircle corners; spacing and type tokens; the live-drawn growth chart; DMC Method timing; laptop zoom scaling; the pink accent on the nav CTA; glass hero badges.
