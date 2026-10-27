/* =========================================================
   Dental Media Corp: shared behaviour (every page)
   Smooth scroll, header, mobile menu, magnetic buttons and the page
   transition that grows a service page out of the clicked image.
   Load after GSAP + ScrollTrigger + Lenis (each optional) and before
   the page script (home.js / service.js), which reads window.DMC.
   ========================================================= */
(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const hasG = !!(window.gsap && window.ScrollTrigger);
  if (hasG) gsap.registerPlugin(ScrollTrigger);
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const pad = (n) => String(n).padStart(2, "0");
  // shared with the page scripts
  const DMC = (window.DMC = {
    $,
    $$,
    pad,
    reduce,
    fine,
    hasG,
    lenis: null,
    arrived: false, // true when this page was opened by the page transition
    onAnchor: [], // hooks run before an in-page #link scrolls
  });

  /* ---------- smooth scroll ---------- */
  let lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ lerp: 0.09 });
    if (hasG) {
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add((t) => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      const raf = (t) => {
        lenis.raf(t);
        requestAnimationFrame(raf);
      };
      requestAnimationFrame(raf);
    }
  }
  DMC.lenis = lenis;

  // a click inside a desktop dropdown closes it until the pointer leaves
  const shutDd = (a) => {
    const dd = a.closest(".dd");
    if (!dd) return;
    dd.classList.add("shut");
    dd.addEventListener("mouseleave", () => dd.classList.remove("shut"), {
      once: true,
    });
  };
  $$('a[href^="#"]').forEach((a) =>
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (id === "#") return;
      const t = $(id);
      if (!t) return;
      e.preventDefault();
      const go = () => {
        DMC.onAnchor.forEach((f) => f(a));
        if (lenis) lenis.scrollTo(t, { duration: 1.4, offset: -90 });
        else t.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
      };
      shutDd(a);
      if (document.activeElement) document.activeElement.blur();
      if (mOpen) closeMnav(go);
      else go();
    }),
  );

  /* ---------- nav: hover pill, shadow on scroll ---------- */
  const top = $("#top"),
    menu = $("#menu"),
    ind = $(".ind", menu),
    burger = $(".burger");
  $$(":scope > a, :scope > .dd > .dd-t", menu).forEach((a) =>
    a.addEventListener("mouseenter", () => {
      const r = a.getBoundingClientRect(),
        m = menu.getBoundingClientRect();
      ind.style.width = r.width + "px";
      ind.style.transform = "translateX(" + (r.left - m.left) + "px)";
      ind.style.opacity = 1;
    }),
  );
  menu.addEventListener("mouseleave", () => {
    ind.style.opacity = 0;
  });
  if (hasG)
    ScrollTrigger.create({
      start: 0,
      end: "max",
      onUpdate: (s) => {
        top.classList.toggle("scrolled", s.scroll() > 40);
      },
    });

  /* ---------- mobile menu: full screen, grows out of the hamburger ---------- */
  const mnav = $("#mnav"),
    mWords = $$(".mn-t > span", mnav),
    mNums = $$(".mn-num", mnav),
    mTgs = $$(".mn-tg", mnav),
    mFoot = $$(".mnav-foot > *", mnav);
  let mOpen = false,
    mBusy = false;
  const mCircle = () => {
    const r = burger.getBoundingClientRect(),
      x = r.left + r.width / 2,
      y = r.top + r.height / 2;
    return {
      x,
      y,
      R:
        Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y)) +
        20,
    };
  };
  function openMnav() {
    if (mOpen || mBusy) return;
    mOpen = true;
    burger.classList.add("x");
    burger.setAttribute("aria-expanded", "true");
    burger.setAttribute("aria-label", "Close menu");
    top.classList.add("menu-open");
    mnav.removeAttribute("inert");
    mnav.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("mn-lock");
    if (lenis) lenis.stop();
    $(".mnav-in", mnav).scrollTop = 0;
    if (!hasG || reduce) {
      mnav.style.visibility = "visible";
      mnav.style.clipPath = "none";
      return;
    }
    const { x, y, R } = mCircle();
    mBusy = true;
    gsap
      .timeline({
        onComplete: () => {
          mBusy = false;
        },
      })
      .set(mnav, { visibility: "visible" })
      .fromTo(
        mnav,
        { clipPath: "circle(0px at " + x + "px " + y + "px)" },
        {
          clipPath: "circle(" + R + "px at " + x + "px " + y + "px)",
          duration: 1,
          ease: "expo.inOut",
        },
      )
      .fromTo(
        ".mnav-bg",
        { scale: 1.25, opacity: 0 },
        { scale: 1, opacity: 1, duration: 1.2, ease: "expo.out" },
        0.15,
      )
      .fromTo(
        mWords,
        { yPercent: 115, rotate: 4 },
        {
          yPercent: 0,
          rotate: 0,
          duration: 1,
          ease: "expo.out",
          stagger: 0.055,
        },
        0.42,
      )
      .fromTo(
        mNums,
        { opacity: 0, x: -12 },
        {
          opacity: 1,
          x: 0,
          duration: 0.6,
          ease: "power3.out",
          stagger: 0.055,
        },
        0.5,
      )
      .fromTo(
        mTgs,
        { scale: 0, rotate: -90 },
        {
          scale: 1,
          rotate: 0,
          duration: 0.7,
          ease: "back.out(2)",
          stagger: 0.08,
        },
        0.7,
      )
      .fromTo(
        $$(".mnav-list > li", mnav),
        { borderBottomColor: "rgba(255,255,255,0)" },
        {
          borderBottomColor: "rgba(255,255,255,.09)",
          duration: 0.6,
          stagger: 0.05,
        },
        0.55,
      )
      .fromTo(
        mFoot,
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.8,
          ease: "power3.out",
          stagger: 0.08,
        },
        0.75,
      );
  }
  function closeMnav(after, instant) {
    if (!mOpen) {
      if (after) after();
      return;
    }
    mOpen = false;
    burger.classList.remove("x");
    burger.setAttribute("aria-expanded", "false");
    burger.setAttribute("aria-label", "Open menu");
    const done = () => {
      mnav.style.visibility = "hidden";
      mnav.setAttribute("inert", "");
      mnav.setAttribute("aria-hidden", "true");
      $$(".mn-has", mnav).forEach((h) => {
        h.classList.remove("open");
        $(".mn-sub", h).style.height = "0px";
        $(".mn-tg", h).setAttribute("aria-expanded", "false");
      });
      document.documentElement.classList.remove("mn-lock");
      if (lenis) lenis.start();
      mBusy = false;
      if (after) after();
    };
    top.classList.remove("menu-open");
    if (!hasG || reduce || instant) {
      done();
      return;
    }
    const { x, y } = mCircle();
    mBusy = true;
    gsap
      .timeline({ onComplete: done })
      .to(mFoot, { y: 20, opacity: 0, duration: 0.3, ease: "power2.in" }, 0)
      .to(
        mWords,
        {
          yPercent: -115,
          duration: 0.4,
          ease: "power3.in",
          stagger: 0.03,
        },
        0,
      )
      .to(
        mnav,
        {
          clipPath: "circle(0px at " + x + "px " + y + "px)",
          duration: 0.75,
          ease: "expo.inOut",
        },
        0.2,
      );
  }
  burger.addEventListener("click", () => {
    if (mOpen) closeMnav();
    else openMnav();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && mOpen) {
      closeMnav();
      burger.focus();
    }
  });
  addEventListener("resize", () => {
    if (mOpen && innerWidth >= 1200) closeMnav();
  });
  // tap-to-expand sub-lists
  $$(".mn-has", mnav).forEach((h) => {
    const tg = $(".mn-tg", h),
      list = $(".mn-sub", h);
    tg.addEventListener("click", () => {
      const open = !h.classList.contains("open");
      h.classList.toggle("open", open);
      tg.setAttribute("aria-expanded", open);
      if (!hasG || reduce) {
        list.style.height = open ? "auto" : "0px";
        return;
      }
      gsap.to(list, {
        height: open ? "auto" : 0,
        duration: 0.6,
        ease: "expo.out",
      });
      if (open)
        gsap.fromTo(
          $$("li", list),
          { x: -16, opacity: 0 },
          {
            x: 0,
            opacity: 1,
            duration: 0.5,
            ease: "power3.out",
            stagger: 0.05,
            delay: 0.05,
          },
        );
    });
  });

  /* ---------- magnetic buttons ---------- */
  if (fine && hasG && !reduce)
    $$(".mag").forEach((el) => {
      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect();
        gsap.to(el, {
          x: (e.clientX - r.left - r.width / 2) * 0.22,
          y: (e.clientY - r.top - r.height / 2) * 0.3,
          duration: 0.5,
          ease: "power3",
        });
      });
      el.addEventListener("pointerleave", () =>
        gsap.to(el, {
          x: 0,
          y: 0,
          duration: 0.9,
          ease: "elastic.out(1,.4)",
        }),
      );
    });

  /* ---------- page transition: a service page grows out of the clicked image ----------
     Leaving: the clicked card image (or link) grows into the service page's hero
     frame, then the browser navigates. The service page starts on that same frame
     (DMC.arrived). Coming back (Back button or "All services"): this page starts
     covered by that frame and it shrinks back into the image it came from. */

  // each service page's hero photo and framing, so the last frame matches it
  const IMG = new URL("../img/", document.currentScript.src);
  const SERVICES = {
    "video-content-production": ["showreel.jpg", "50% 6%"],
    "social-media-management": ["phone.webp", "50% 42%"],
    "website-seo": ["case3.webp", "50% 50%"],
    "paid-media-acquisition": ["case1.webp", "50% 50%"],
    "reporting-analytics": ["case2.webp", "50% 30%"],
  };
  const PT = "dmc-pt:";
  const store = {
    get: (k) => {
      try {
        return JSON.parse(sessionStorage.getItem(PT + k));
      } catch (e) {
        return null;
      }
    },
    set: (k, v) => {
      try {
        sessionStorage.setItem(PT + k, JSON.stringify(v));
      } catch (e) {}
    },
    del: (k) => {
      try {
        sessionStorage.removeItem(PT + k);
      } catch (e) {}
    },
  };
  // a page's address without hash or trailing index.html
  const url = (h) => {
    const u = new URL(h, location.href);
    return u.origin + u.pathname.replace(/index\.html$/, "") + u.search;
  };
  const here = url(location.href);
  const navType = (performance.getEntriesByType("navigation")[0] || {}).type;
  const svcOf = (a) => {
    const m = new URL(a.href, location.href).pathname.match(
      /\/services\/([a-z-]+)\/(?:index\.html)?$/,
    );
    return m && SERVICES[m[1]] ? m[1] : null;
  };

  const pt = document.createElement("div");
  pt.className = "pt";
  pt.setAttribute("aria-hidden", "true");
  pt.innerHTML = '<img alt="" decoding="async" />';
  document.body.append(pt);
  const ptImg = $("img", pt);
  const vw = () => document.documentElement.clientWidth,
    vh = () => document.documentElement.clientHeight;
  const FULL = "inset(5px 5px 5px 5px round 28px)"; // the service hero card
  const inset = (r) =>
    "inset(" +
    [r.top, vw() - r.right, vh() - r.bottom, r.left]
      .map((v) => Math.max(0, Math.round(v)) + "px")
      .join(" ") +
    " round 20px)";
  const ptShow = (src, pos) => {
    ptImg.src = src;
    ptImg.style.objectPosition = innerWidth <= 640 ? "50% 35%" : pos;
    ptImg.style.transform = "";
    pt.style.opacity = 1;
    pt.style.visibility = "visible";
  };
  const ptHide = () => {
    pt.classList.remove("on");
    pt.style.visibility = "hidden";
    pt.style.clipPath = "";
  };
  // the image a link grows out of: its card's photo, else the link itself
  const origin = (a) => {
    const c = a.closest(".step, .sp-nx");
    return (c && $(".step-media, .sp-nx-media", c)) || a;
  };
  // on-screen rect of an element, or null if it's hidden, off screen or covered
  const onScreen = (el) => {
    if (
      !el ||
      (el.checkVisibility && !el.checkVisibility({ visibilityProperty: true }))
    )
      return null;
    const r = el.getBoundingClientRect(),
      x = r.left + r.width / 2,
      y = r.top + r.height / 2;
    if (!r.width || x < 0 || y < 0 || x > vw() || y > vh()) return null;
    const hit = document.elementFromPoint(x, y);
    return hit && (el.closest(".step, .sp-nx") || el).contains(hit) ? r : null;
  };
  let ptOut = null; // the last transition out of this page (kept for back/forward cache)

  function ptGo(a, slug) {
    const [file, pos] = SERVICES[slug],
      links = $$("a[href]");
    ptOut = {
      to: url(a.href),
      i: links.indexOf(a),
      y: Math.round(scrollY),
      src: new URL(file, IMG).href,
      pos,
    };
    store.set(here, ptOut);
    store.set("to", ptOut.to);
    if (!hasG || reduce) {
      location.href = a.href;
      return;
    }
    const r = onScreen(origin(a)),
      x = vw() / 2,
      y = vh() / 2,
      R = Math.hypot(x, y);
    const from = r ? inset(r) : "circle(0px at " + x + "px " + y + "px)",
      to = r ? FULL : "circle(" + R + "px at " + x + "px " + y + "px)";
    if (lenis) lenis.stop();
    pt.classList.add("on");
    pt.style.clipPath = from;
    ptShow(ptOut.src, pos);
    // wait (briefly) for the photo so the frame never grows empty
    Promise.race([
      ptImg.decode().catch(() => {}),
      new Promise((res) => setTimeout(res, 400)),
    ]).then(() =>
      gsap
        .timeline({ onComplete: () => (location.href = a.href) })
        .fromTo(
          pt,
          { clipPath: from },
          { clipPath: to, duration: 0.9, ease: "expo.inOut" },
        )
        .fromTo(
          ptImg,
          { scale: 1.25 },
          { scale: 1, duration: 1.1, ease: "expo.out" },
          0,
        ),
    );
  }

  function ptReturn(st) {
    const links = $$("a[href]");
    let r = null;
    for (const l of [links[st.i], ...links])
      if (l && url(l.href) === st.to && (r = onScreen(origin(l)))) break;
    pt.classList.remove("on");
    pt.style.clipPath = FULL;
    ptShow(st.src, st.pos);
    if (!hasG || reduce) {
      ptHide();
      return;
    }
    const tl = gsap.timeline({ onComplete: ptHide });
    if (r)
      tl.fromTo(
        pt,
        { clipPath: FULL },
        { clipPath: inset(r), duration: 0.8, ease: "expo.inOut" },
      ).fromTo(
        ptImg,
        { scale: 1 },
        { scale: 1.25, duration: 0.8, ease: "expo.inOut" },
        0,
      );
    else tl.to(pt, { opacity: 0, duration: 0.5, ease: "power2.out" });
  }

  $$("a[href]").forEach((a) => {
    const slug = svcOf(a);
    if (!slug || url(a.href) === here) return;
    a.addEventListener("click", (e) => {
      if (e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      shutDd(a);
      ptGo(a, slug);
    });
  });

  // "All services": if we came from that page, go back so it can shrink into its card
  $$("[data-pt-back]").forEach((a) =>
    a.addEventListener("click", (e) => {
      if (!document.referrer || url(document.referrer) !== url(a.href)) return;
      e.preventDefault();
      const img = $(".sp-hero .h-media img");
      if (!hasG || reduce || !img) {
        history.back();
        return;
      }
      if (lenis) lenis.stop();
      pt.classList.add("on");
      pt.style.clipPath = FULL;
      ptShow(img.currentSrc || img.src, img.style.objectPosition);
      gsap.fromTo(
        pt,
        { opacity: 0 },
        {
          opacity: 1,
          duration: 0.35,
          ease: "power2.out",
          onComplete: () => history.back(),
        },
      );
    }),
  );

  // arrived here through the transition: the page script skips its photo zoom
  if (store.get("to") === here) {
    DMC.arrived = true;
    store.del("to");
  }

  // back here without the back/forward cache: start covered, shrink once laid out
  const back = navType === "back_forward" ? store.get(here) : null;
  if (back && hasG && !reduce) {
    pt.style.clipPath = FULL;
    ptShow(back.src, back.pos);
  }
  addEventListener("pageshow", (e) => {
    if (e.persisted) {
      // restored from the back/forward cache exactly as we left it
      store.del(here);
      if (mOpen) closeMnav(null, true);
      if (lenis) lenis.start();
      if (ptOut && pt.style.visibility === "visible") ptReturn(ptOut);
      else ptHide();
      ptOut = null;
      return;
    }
    if (!back) return;
    store.del(here);
    if (lenis) lenis.scrollTo(back.y, { immediate: true, force: true });
    else scrollTo(0, back.y);
    if (hasG) ScrollTrigger.update();
    requestAnimationFrame(() => ptReturn(back));
  });
})();
