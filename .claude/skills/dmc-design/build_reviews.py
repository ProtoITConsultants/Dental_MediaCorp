# -*- coding: utf-8 -*-
# Builds reviews.html (inspo: theimplantengine.com/reviews, the layout only; every size, card and motion is ours):
#   1. hero: the blog / case-studies head, centred (label, H1, intro)
#   2. the numbers bar: the home hero's glass badge box (.h-badges), filled with our real figures
#   3. video testimonials: the home hero's review cards, in the service pages' moving row ("What dentists say")
#   then the footer. Nothing else (user).
# Reuses the service template's parts (build_service.py): style, header, footer, review cards, lightbox and script.
# Run from the repo root:  python .claude/skills/dmc-design/build_reviews.py
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import preloader
import build_service as bs

header = bs.header.replace('<a class="dd-t is-cur" href="index.html#services"', '<a class="dd-t" href="index.html#services"')
header = header.replace('<a href="reviews.html">Reviews</a>', '<a class="is-cur" href="reviews.html">Reviews</a>')

# only figures the site already states (home hero, review cards, case studies)
STATS = [
    ('<i class="ph-fill ph-star rv-ic" aria-hidden="true"></i>', '5.0 <span class="rv-stars" aria-hidden="true">★★★★★</span>', 'Average rating'),
    ('<i class="ph-fill ph-users-three rv-ic" aria-hidden="true"></i>', '5,000+', 'Consultations attended'),
    ('<i class="ph-fill ph-currency-circle-dollar rv-ic" aria-hidden="true"></i>', '$10M+', 'Accepted treatment'),
    ('<i class="ph-fill ph-chart-line-up rv-ic" aria-hidden="true"></i>', 'Up to 19.4×', 'Return on ad spend'),
]
stats = '\n'.join(f'            <li>{ic}<span><b>{num}</b> {lbl}</span></li>' for ic, num, lbl in STATS)

CSS = """
      /* ================= reviews (reviews.html; built by build_reviews.py) =================
         The blog head centred, the home hero's glass badge box as a numbers bar, then the service pages' review row. */
      .menu a.is-cur {
        color: var(--teal);
      }
      .rvh {
        position: relative;
        padding: clamp(118px, calc(16 * var(--uvh)), 150px) 0 0;
        background:
          radial-gradient(32% 40% at 80% 12%, rgba(255, 191, 215, 0.34), transparent 70%),
          radial-gradient(36% 44% at 16% 30%, rgba(191, 230, 220, 0.5), transparent 70%);
      }
      .rvh-in {
        max-width: 860px;
        margin-inline: auto;
        text-align: center;
      }
      .rvh .eyb {
        justify-content: center;
        margin-bottom: 22px;
      }
      .rvh .t-h1 {
        --fs-h1: clamp(38px, calc(4.2 * var(--uvw)), 68px);
      }
      .rvh-txt {
        max-width: 600px;
        margin: 24px auto 0;
        font-size: var(--fs-lead);
        line-height: 1.45;
        color: var(--grey);
      }
      /* the numbers bar: the hero's glass badge box, wider, a figure over its label */
      .rvh .h-badges {
        max-width: 1040px;
        margin: clamp(40px, calc(5 * var(--uvh)), 64px) auto 0;
        padding: 20px 6px;
      }
      .rvh .h-badges b {
        font-size: var(--fs-h4);
        font-weight: 600;
        letter-spacing: -0.03em;
        color: var(--ink);
      }
      .rvh .h-badges li:first-child b {
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .rv-ic {
        font-size: 30px;
        color: var(--teal);
      }
      .rv-stars {
        margin-left: 4px;
        font-size: 0.6em;
        letter-spacing: 1px;
        color: var(--acc-mid);
        vertical-align: 0.2em;
      }
      .rvw.rv-page {
        padding-top: var(--sec-y);
      }
      @media (max-width: 899px) {
        .rvh .h-badges {
          flex-wrap: wrap;
          row-gap: 16px;
        }
        .rvh .h-badges li {
          flex: 1 1 45%;
          justify-content: flex-start;
          padding: 0 14px;
        }
        .rvh .h-badges li + li {
          border-left: 0;
        }
      }
"""
style_out = bs.style.replace('    </style>', bs.PAGE_CSS + CSS + '    </style>')

# the service script, with its service-only blocks (banner notch, client video) skipped: this page has neither
JS = bs.JS
for head, el in [('        /* ---------- service banner: cut the notch for the button ---------- */\n        {', '#svb'),
                 ('        /* ---------- client video: the bottom-right notch for the buttons, and play in the card ---------- */\n        {', '#vtBox')]:
    assert JS.count(head) == 1, head[:60]
    JS = JS.replace(head, head[:-1] + f'if ($("{el}")) {{')

page = f'''<!doctype html>
<html lang="en-CA">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Reviews | Dental Media Corp</title>
    <meta name="description" content="What dentists say about working with Dental Media Corp: video testimonials from clinics across Canada." />
    <link rel="canonical" href="https://dentalmediacorp.com/reviews/" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <meta name="theme-color" content="#0F1716" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Dental Media Corp" />
    <meta property="og:title" content="Reviews | Dental Media Corp" />
    <meta property="og:url" content="https://dentalmediacorp.com/reviews/" />
    <meta property="og:locale" content="en_CA" />
{bs.head_links}
{style_out}
  </head>
  <body>
    <a class="skip" href="#main">Skip to content</a>
{bs.symbols}

    <!-- ============ HEADER (shared with the home page) ============ -->
{header}

    <!-- ============ MOBILE MENU ============ -->
{bs.mnav}
    <main id="main">
      <!-- ============ 1. HERO + NUMBERS (inspo: theimplantengine.com/reviews; our components)
           Elementor: Container. Label, H1, intro; then an Icon List in the home hero's glass box (ACF: icon, figure, label). -->
      <section class="rvh" aria-labelledby="rv-title">
        <div class="wrap">
          <div class="rvh-in">
            <p class="eyb">Reviews</p>
            <h1 class="t-h1" id="rv-title">
              <span class="ln-m"><span>Real reviews from</span></span>
              <span class="ln-m"><span><span class="hl">real clinics.</span></span></span>
            </h1>
            <p class="rvh-txt">Dentists across Canada on what changed once we took over their marketing: the ads, the calls and the bookings, so their team could focus on patients.</p>
          </div>
          <ul class="h-badges" aria-label="Our results in numbers">
{stats}
          </ul>
        </div>
      </section>

      <!-- ============ 2. VIDEO TESTIMONIALS (the home hero's moving cards) ============ -->
      <section class="rvw rv-page" id="testimonials" aria-labelledby="rvw-title">
        <div class="wrap">
          <div class="sh">
            <h2 class="t-h2" id="rvw-title">
              <span class="ln-m"><span>Video testimonials</span></span>
              <span class="sh-l2"><span class="sh-rule" aria-hidden="true"></span><span class="ln-m"><span class="hl">from our clinics.</span></span></span>
            </h2>
          </div>
        </div>
        <div class="rvw-row">
{bs.reviews}        </div>
      </section>
    </main>

    <!-- video lightbox: the review cards' play buttons fill it with a YouTube embed -->
{bs.vbox}
    <div class="sbreak" aria-hidden="true"></div>
    <!-- ============ FOOTER (shared with the home page) ============ -->
{bs.footer}

    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>{JS}
  </body>
</html>
'''

if __name__ == '__main__':
    out = preloader.inject(page)
    open('reviews.html', 'wb').write(out.replace('\n', '\r\n').encode('utf-8'))
    print('ok reviews.html', len(out.splitlines()))
