# -*- coding: utf-8 -*-
# The home page's preloader on every page (user, 2026-11-24): the dark panel with the 3D mark and "Dental Media Corp",
# held until EVERY image on the page has loaded (lazy ones are switched to eager while it shows; at most 8s), then the
# same exit as the home page: the name lifts away, the panel wipes up with the pink edge line, and the page's own
# entrances play as it lifts. The CSS (.pre, .pre-obj, .pre-b, .pre-edge, html.is-pre) is already in every page's
# <style> (copied from index.html). index.html carries its own copy of BODY (and runs its own GSAP exit, which also waits
# for window.__preWait()); the other builders call inject(page) just before writing.
#
# How the other pages wait: this script runs after GSAP / ScrollTrigger / Lenis load and before the page script, pauses
# GSAP's global timeline (so the page's entrances are created in their start state but don't play), blocks scrolling
# under the panel, and runs the exit with the Web Animations API (independent of GSAP), resuming GSAP 0.55s into the
# wipe, the moment the home page starts its hero build.

BODY = '''    <script>
      // preloader only runs when the motion stack is going to run it
      if (!matchMedia("(prefers-reduced-motion: reduce)").matches) document.documentElement.classList.add("is-pre");
      // it waits for every image on the page (the lazy ones load now too), at most 8s; the ones in view are also decoded
      window.__preWait = () => {
        const imgs = [...document.images];
        const one = (i) => {
          if (i.loading === "lazy") i.loading = "eager";
          if (i.complete && i.naturalWidth) return Promise.resolve();
          return new Promise((r) => {
            i.addEventListener("load", r, { once: true });
            i.addEventListener("error", r, { once: true });
            if (i.complete) r();
          });
        };
        const inView = () => imgs.filter((i) => i.getBoundingClientRect().top < innerHeight).map((i) => (i.decode ? i.decode().catch(() => {}) : 0));
        const all = Promise.all(imgs.map(one)).then(() => Promise.all(inView()));
        return Promise.race([all, new Promise((r) => setTimeout(r, 8000))]);
      };
    </script>
'''

MARKUP = '''
    <!-- ============ PRELOADER (the home page's; Elementor: a Custom Code snippet) ============ -->
    <div class="pre" id="pre" aria-hidden="true">
      <img class="pre-obj" src="assets/img/v11/mark-pre.webp" alt="" width="1920" height="1080" fetchpriority="high" />
      <span class="pre-b"><img src="assets/dmc-mark.png" alt="" width="22" height="22" />Dental Media Corp</span>
    </div>
    <span class="pre-edge" id="preEdge" aria-hidden="true"></span>
'''

LIFT = '''
    <script>
      /* ---------- preloader: hold until every image has loaded, then the home page's wipe ---------- */
      (() => {
        const root = document.documentElement,
          pre = document.getElementById("pre"),
          edge = document.getElementById("preEdge");
        if (!pre) return;
        if (!root.classList.contains("is-pre")) return void (pre.remove(), edge && edge.remove());
        const G = window.gsap;
        if (G) G.globalTimeline.pause(); // the page's entrances wait for the wipe
        // nothing scrolls under the panel (registered before Lenis, so it never sees these)
        const stop = (e) => (e.preventDefault(), e.stopImmediatePropagation());
        const keys = (e) => [" ", "ArrowDown", "ArrowUp", "PageDown", "PageUp", "Home", "End"].includes(e.key) && stop(e);
        addEventListener("wheel", stop, { passive: false, capture: true });
        addEventListener("touchmove", stop, { passive: false, capture: true });
        addEventListener("keydown", keys, { capture: true });
        const inOut = "cubic-bezier(0.87, 0, 0.13, 1)"; // expo.inOut
        pre.querySelector(".pre-obj").animate([{ transform: "scale(1.15)" }, { transform: "scale(1)" }], { duration: 2600, easing: "cubic-bezier(0.25, 0.46, 0.45, 0.94)", fill: "both" });
        const t0 = performance.now();
        window.__preWait().then(() => {
          // never a flash: the panel shows for at least 0.6s
          setTimeout(() => {
            pre.querySelector(".pre-b").animate([{ transform: "none", opacity: 1 }, { transform: "translateY(-40%)", opacity: 0 }], { duration: 500, easing: "cubic-bezier(0.55, 0.06, 0.68, 0.19)", fill: "forwards" });
            setTimeout(() => {
              const z = parseFloat(getComputedStyle(root).zoom) || 1;
              pre.animate([{ clipPath: "inset(0 0 0% 0)" }, { clipPath: "inset(0 0 100% 0)" }], { duration: 1100, easing: inOut, fill: "forwards" });
              edge.style.opacity = "1";
              edge.animate([{ transform: "translateY(0)" }, { transform: `translateY(${-innerHeight / z}px)` }], { duration: 1100, easing: inOut, fill: "forwards" });
            }, 200);
            setTimeout(() => G && G.globalTimeline.resume(), 750);
            setTimeout(() => {
              root.classList.remove("is-pre");
              pre.remove();
              edge.remove();
              removeEventListener("wheel", stop, { capture: true });
              removeEventListener("touchmove", stop, { capture: true });
              removeEventListener("keydown", keys, { capture: true });
              if (window.ScrollTrigger) ScrollTrigger.refresh();
            }, 1350);
          }, Math.max(0, 600 - (performance.now() - t0)));
        });
      })();
    </script>'''

LENIS_TAG = '<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>'


def inject(page):
    """Add the preloader to a built page (once): the waiter + markup at the top of <body>, the exit before the page script."""
    if 'id="pre"' in page:
        return page
    assert page.count('  <body>\n') == 1 and page.count(LENIS_TAG) == 1
    page = page.replace('  <body>\n', '  <body>\n' + BODY + MARKUP, 1)
    return page.replace(LENIS_TAG, LENIS_TAG + LIFT, 1)
