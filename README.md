# Dental Media Corp website

Static, build-free marketing site for Dental Media Corp: a home page plus one
page per service. Plain HTML, CSS and JavaScript. Deploy the folder as-is to any
static host (Vercel, Netlify, Cloudflare Pages, S3, Apache, Nginx).

## Structure

```
.
├── index.html                      Home page
├── services/                       One folder per service → clean URLs (/services/<slug>/)
│   ├── video-content-production/index.html
│   ├── social-media-management/index.html
│   ├── website-seo/index.html
│   ├── paid-media-acquisition/index.html
│   └── reporting-analytics/index.html
├── assets/
│   ├── css/
│   │   ├── base.css                Shared: tokens, buttons, header, mobile menu, hero card,
│   │   │                           section primitives, shared cards, footer, page transition
│   │   ├── home.css                Home page sections only
│   │   └── service.css             Service page sections only
│   ├── js/
│   │   ├── site.js                 Shared: smooth scroll, header, mobile menu, magnetic
│   │   │                           buttons, page transition. Exposes window.DMC
│   │   ├── home.js                 Home only: carousel, booking calendar, FAQ, scroll choreography
│   │   └── service.js              Service pages only: hero intro, scroll reveals
│   └── img/
│       ├── brand/dmc-mark.png      Logo mark (also the favicon)
│       ├── *.webp / *.jpg          Photography (see assets/img/CREDITS.md)
│       └── CREDITS.md
├── robots.txt
└── sitemap.xml
```

Every page loads `base.css` and `site.js`, followed by its own page CSS and JS.
GSAP 3.12.5, ScrollTrigger and Lenis 1.1.13 come from CDNs and are optional: without
them (or with `prefers-reduced-motion`), the site works without animation.

## Run locally

Links use folder URLs (`services/website-seo/`), so serve the folder over HTTP
instead of opening the files directly:

```sh
python -m http.server 8080      # or: npx serve .
```

Then open http://localhost:8080/.

## Page transition (service cards)

Clicking a service card, or any link to a service page, grows the card's
photo to fill the screen. The browser then navigates, and the service page
starts on that same frame. Back (browser Back or "All services") shrinks it
back into the card it came from. Everything lives in the page-transition
section of `assets/js/site.js`:

- `SERVICES` maps each service slug to its hero photo and framing
  (`object-position`). Keep it in sync with the hero `<img>` on that page,
  so the transition's last frame matches the page's first frame.
- The transition uses `sessionStorage` (`dmc-pt:*`), so it also works when the
  browser doesn't keep the page in its back/forward cache.

## Adding a service page

1. Copy a folder in `services/` to `services/<new-slug>/` and edit its content,
   `<title>`, meta description, canonical/OG URLs and the JSON-LD block.
2. Add the slug's hero photo and framing to `SERVICES` in `assets/js/site.js`.
3. Add the page to the Services menus (desktop dropdown, mobile menu and footer)
   on **every** page, add a card to the home `#services` stack, and update the
   "Next service" card on the previous page.
4. Add the URL to `sitemap.xml`.

The header, mobile menu and footer are repeated in each HTML file (no build step).
When you change them, change them on all six pages.

## Elementor mapping

The markup is written to port to WordPress/Elementor:

- Each `<section>` = one top-level Container; `.wrap` = boxed inner Container.
- `:root` colours = Site Settings › Global Colors; Plus Jakarta Sans = Global Fonts.
- Header and footer = Theme Builder › Header / Footer.
- Each service page = a page at `/services/<slug>/` (same URLs as `sitemap.xml`).
- `base.css` + the page CSS = Custom CSS; GSAP, Lenis and the JS files = Elementor Pro › Custom Code.
