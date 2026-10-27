/* =========================================================
   Dental Media Corp: home page behaviour (index.html)
   Treatments carousel, booking calendar, showreel, FAQ and the
   scroll choreography. Needs site.js (window.DMC) loaded first.
   ========================================================= */
(() => {
  const { $, $$, pad, reduce, fine, hasG } = window.DMC;

  /* ---------- about: split statement into words ---------- */
  const say = $("#say");
  say.innerHTML = say.textContent
    .trim()
    .split(/\s+/)
    .map((w) => '<span class="w">' + w + "</span>")
    .join(" ");

  /* ---------- treatments carousel: the active card opens and shows its image ---------- */
  const row = $("#tRow"),
    tcards = $$(".tcard", row),
    tPrev = $("#tPrev"),
    tNext = $("#tNext");
  let ta = 0,
    tSnap = null,
    tDown = false,
    tMoved = false;
  const tGap = 14;
  const tW = () => (innerWidth <= 640 ? innerWidth * 0.82 : 290);
  function tSet(i, scroll = true) {
    ta = Math.max(0, Math.min(tcards.length - 1, i));
    tcards.forEach((c, k) => {
      c.classList.toggle("on", k === ta);
      c.setAttribute("aria-current", k === ta ? "true" : "false");
    });
    tPrev.disabled = ta === 0;
    tNext.disabled = ta === tcards.length - 1;
    if (scroll)
      row.scrollTo({
        left: ta * (tW() + tGap),
        behavior: reduce ? "auto" : "smooth",
      });
  }
  tNext.addEventListener("click", () => tSet(ta + 1));
  tPrev.addEventListener("click", () => tSet(ta - 1));
  tcards.forEach((c, k) =>
    c.addEventListener("click", () => {
      if (!tMoved && k !== ta) tSet(k);
    }),
  );
  row.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") {
      e.preventDefault();
      tSet(ta + 1);
    }
    if (e.key === "ArrowLeft") {
      e.preventDefault();
      tSet(ta - 1);
    }
  });
  // after a free swipe or drag, the card nearest the start becomes the active one
  row.addEventListener(
    "scroll",
    () => {
      clearTimeout(tSnap);
      tSnap = setTimeout(() => {
        if (tDown) return;
        const i = Math.max(
          0,
          Math.min(
            tcards.length - 1,
            Math.round(row.scrollLeft / (tW() + tGap)),
          ),
        );
        if (i !== ta || Math.abs(row.scrollLeft - i * (tW() + tGap)) > 2)
          tSet(i);
      }, 140);
    },
    { passive: true },
  );
  if (fine) {
    let sx = 0,
      sl = 0;
    row.addEventListener("pointerdown", (e) => {
      tDown = true;
      tMoved = false;
      sx = e.clientX;
      sl = row.scrollLeft;
    });
    window.addEventListener("pointermove", (e) => {
      if (!tDown) return;
      const dx = e.clientX - sx;
      if (Math.abs(dx) > 4) {
        tMoved = true;
        row.classList.add("drag");
      }
      row.scrollLeft = sl - dx;
    });
    window.addEventListener("pointerup", () => {
      if (!tDown) return;
      tDown = false;
      row.classList.remove("drag");
      row.dispatchEvent(new Event("scroll"));
    });
  }
  addEventListener("resize", () => tSet(ta, false));
  tSet(0, false);

  /* ---------- calendar card: current month, today highlighted ---------- */
  {
    const g = $("#calGrid"),
      now = new Date(),
      y = now.getFullYear(),
      m = now.getMonth(),
      today = now.getDate();
    $("#calTitle").textContent = now.toLocaleDateString("en-CA", {
      month: "long",
      year: "numeric",
    });
    let h = ["S", "M", "T", "W", "T", "F", "S"]
      .map((d) => "<b>" + d + "</b>")
      .join("");
    const first = new Date(y, m, 1).getDay(),
      days = new Date(y, m + 1, 0).getDate();
    for (let i = 0; i < first; i++) h += "<span></span>";
    for (let d = 1; d <= days; d++) {
      const wd = (first + d - 1) % 7,
        cls =
          d === today
            ? "today"
            : wd > 0 && wd < 6 && d > today && d <= today + 7
              ? "wk"
              : "";
      h += "<span" + (cls ? ' class="' + cls + '"' : "") + ">" + d + "</span>";
    }
    g.innerHTML = h;
  }

  /* ---------- booking calendar: live open times from LeadConnector ---------- */
  {
    const bk = $("#bk"),
      CAL = bk.dataset.calendar,
      BOOK_URL = bk.dataset.bookEndpoint || "";
    const daysEl = $("#bkDays"),
      monthEl = $("#bkMonth"),
      msgEl = $("#bkMsg"),
      tzSel = $("#bkTz");
    const timesEl = $("#bkTimes"),
      slotsEl = $("#bkSlots"),
      dayEl = $("#bkDay");
    const prevBtn = $("#bkPrev"),
      nextBtn = $("#bkNext"),
      s1 = $("#bkS1"),
      s2 = $("#bkS2"),
      s3 = $("#bkS3");
    const localTz =
      Intl.DateTimeFormat().resolvedOptions().timeZone || "America/Edmonton";
    const ZONES = [
      [localTz, "Your time zone"],
      ["America/Edmonton", "Mountain Time (Calgary)"],
      ["America/Vancouver", "Pacific Time (Vancouver)"],
      ["America/Regina", "Central Time (Regina)"],
      ["America/Winnipeg", "Central Time (Winnipeg)"],
      ["America/Toronto", "Eastern Time (Toronto)"],
      ["America/Halifax", "Atlantic Time (Halifax)"],
      ["America/St_Johns", "Newfoundland Time"],
    ];
    const MONTHS = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];
    const p2 = (n) => String(n).padStart(2, "0");
    const isoToday = (tz) =>
      new Intl.DateTimeFormat("en-CA", {
        timeZone: tz,
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      }).format(new Date());
    const clock = (tz) =>
      new Intl.DateTimeFormat("en-US", {
        hour: "numeric",
        minute: "2-digit",
        timeZone: tz,
      })
        .format(new Date())
        .toLowerCase()
        .replace(" ", "");
    const dayName = (iso) => {
      const [y, m, d] = iso.split("-").map(Number);
      return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric",
        year: "numeric",
        timeZone: "UTC",
      });
    };
    // slot strings come back already in the requested zone, e.g. 2026-10-26T20:30:00-06:00
    const slotTime = (s) => {
      let h = +s.slice(11, 13);
      const mi = s.slice(14, 16),
        ap = h >= 12 ? "pm" : "am";
      h = h % 12 || 12;
      return h + ":" + mi + ap;
    };

    [...new Map(ZONES.map((z) => [z[0], z])).values()].forEach(([id, name]) => {
      const o = document.createElement("option");
      o.value = id;
      o.textContent = name + " (" + clock(id) + ")";
      tzSel.append(o);
    });
    let tz = localTz,
      today = isoToday(tz),
      view = { y: +today.slice(0, 4), m: +today.slice(5, 7) - 1 };
    const cache = {},
      sel = { date: null, slot: null };
    tzSel.value = tz;
    const tzLabel = () => {
      $("#bkTzLabel").textContent =
        tzSel.options[tzSel.selectedIndex].textContent.replace(/ \(.*\)$/, "") +
        " (" +
        tz.replace(/_/g, " ") +
        ")";
    };

    // offset of the chosen zone from UTC (ms) around a given instant
    const tzOff = (t) => {
      const p = Object.fromEntries(
        new Intl.DateTimeFormat("en-US", {
          timeZone: tz,
          hourCycle: "h23",
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
          .formatToParts(new Date(t))
          .map((x) => [x.type, x.value]),
      );
      return (
        Date.UTC(+p.year, p.month - 1, +p.day, +p.hour, +p.minute, +p.second) -
        Math.floor(t / 1000) * 1000
      );
    };

    async function load(y, m) {
      const key = tz + "|" + y + "|" + m;
      if (!cache[key]) {
        // the API allows at most 31 days, so ask for exactly this month in the chosen zone
        const start = Date.UTC(y, m, 1) - tzOff(Date.UTC(y, m, 1)),
          end = Date.UTC(y, m + 1, 1) - tzOff(Date.UTC(y, m + 1, 1)) - 1;
        cache[key] = fetch(
          "https://backend.leadconnectorhq.com/calendars/" +
            CAL +
            "/free-slots?startDate=" +
            start +
            "&endDate=" +
            end +
            "&timezone=" +
            encodeURIComponent(tz),
        )
          .then((r) => {
            if (!r.ok) throw new Error(r.status);
            return r.json();
          })
          .then((j) => {
            const pre = y + "-" + p2(m + 1) + "-",
              out = {};
            Object.keys(j).forEach((k) => {
              if (k.startsWith(pre) && j[k] && j[k].slots && j[k].slots.length)
                out[k] = j[k].slots;
            });
            return out;
          })
          .catch((e) => {
            delete cache[key];
            throw e;
          });
      }
      return cache[key];
    }

    async function render() {
      const { y, m } = view,
        now = isoToday(tz);
      monthEl.textContent = MONTHS[m] + " " + y;
      prevBtn.disabled =
        y < +now.slice(0, 4) ||
        (y === +now.slice(0, 4) && m <= +now.slice(5, 7) - 1);
      const first = (new Date(Date.UTC(y, m, 1)).getUTCDay() + 6) % 7,
        days = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
      daysEl.innerHTML =
        "<span></span>".repeat(first) + '<span class="sk"></span>'.repeat(days);
      msgEl.textContent = "";
      let open;
      try {
        open = await load(y, m);
      } catch (e) {
        if (view.y !== y || view.m !== m) return;
        daysEl.innerHTML =
          "<span></span>".repeat(first) +
          Array.from(
            { length: days },
            (_, i) => "<span>" + (i + 1) + "</span>",
          ).join("");
        msgEl.innerHTML =
          'We couldn’t load open times. <a href="https://api.leadconnectorhq.com/widget/bookings/dmc-calendar-intro" target="_blank" rel="noopener">Book on LeadConnector</a>';
        return;
      }
      if (view.y !== y || view.m !== m) return;
      let html = "<span></span>".repeat(first);
      for (let d = 1; d <= days; d++) {
        const iso = y + "-" + p2(m + 1) + "-" + p2(d),
          cls = iso === now ? ' class="today"' : "";
        html += open[iso]
          ? '<button type="button"' +
            cls +
            ' data-d="' +
            iso +
            '" aria-pressed="' +
            (sel.date === iso) +
            '" aria-label="' +
            dayName(iso) +
            ", " +
            open[iso].length +
            ' times available">' +
            d +
            "</button>"
          : "<span" + cls + ' aria-hidden="true">' + d + "</span>";
      }
      daysEl.innerHTML = html;
      if (!Object.keys(open).length)
        msgEl.innerHTML =
          "No open times in " +
          MONTHS[m] +
          '. <button type="button" data-jump>See next month</button>';
      if (hasG && !reduce)
        gsap.from($$("button", daysEl), {
          scale: 0.6,
          opacity: 0,
          duration: 0.5,
          ease: "back.out(2)",
          stagger: 0.025,
        });
    }

    function pickDay(iso) {
      sel.date = iso;
      sel.slot = null;
      $$("button", daysEl).forEach((b) =>
        b.setAttribute("aria-pressed", b.dataset.d === iso),
      );
      bk.classList.add("has-day");
      timesEl.hidden = false;
      dayEl.textContent = dayName(iso).replace(/, \d{4}$/, "");
      const key = tz + "|" + view.y + "|" + view.m;
      cache[key].then((open) => {
        slotsEl.innerHTML = open[iso]
          .map(
            (s) =>
              '<div class="bk-slot"><button type="button" class="t" data-s="' +
              s +
              '">' +
              slotTime(s) +
              '</button><button type="button" class="go" tabindex="-1">Next</button></div>',
          )
          .join("");
        if (hasG && !reduce)
          gsap.from(slotsEl.children, {
            x: 24,
            opacity: 0,
            duration: 0.6,
            ease: "expo.out",
            stagger: 0.05,
          });
      });
    }

    function step(n) {
      [s1, s2, s3].forEach((s, i) => {
        s.hidden = i !== n - 1;
      });
      if (hasG && !reduce)
        gsap.from([s1, s2, s3][n - 1], {
          y: 16,
          opacity: 0,
          duration: 0.6,
          ease: "power3.out",
        });
      if (hasG) ScrollTrigger.refresh();
    }

    daysEl.addEventListener("click", (e) => {
      const b = e.target.closest("button[data-d]");
      if (b) pickDay(b.dataset.d);
    });
    msgEl.addEventListener("click", (e) => {
      if (e.target.closest("[data-jump]")) nextBtn.click();
    });
    slotsEl.addEventListener("click", (e) => {
      const row = e.target.closest(".bk-slot");
      if (!row) return;
      if (e.target.closest(".go")) {
        $("#bkWhenRow").hidden = false;
        $("#bkWhen").textContent =
          slotTime(sel.slot) + ", " + dayName(sel.date);
        step(2);
        $("#f-name").focus();
        return;
      }
      sel.slot = $(".t", row).dataset.s;
      $$(".bk-slot", slotsEl).forEach((r) => {
        const on = r === row;
        r.classList.toggle("sel", on);
        $(".go", r).tabIndex = on ? 0 : -1;
      });
    });
    prevBtn.addEventListener("click", () => {
      if (--view.m < 0) {
        view.m = 11;
        view.y--;
      }
      render();
    });
    nextBtn.addEventListener("click", () => {
      if (++view.m > 11) {
        view.m = 0;
        view.y++;
      }
      render();
    });
    tzSel.addEventListener("change", () => {
      tz = tzSel.value;
      sel.date = sel.slot = null;
      bk.classList.remove("has-day");
      timesEl.hidden = true;
      tzLabel();
      render();
    });
    $("#bkBack").addEventListener("click", () => {
      $("#bkWhenRow").hidden = true;
      step(1);
    });

    s2.addEventListener("submit", async (e) => {
      e.preventDefault();
      let ok = true;
      [
        ["#f-name", (v) => v.trim().length > 1, "Please enter your name."],
        [
          "#f-email",
          (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v),
          "Please enter a valid email.",
        ],
      ].forEach(([s, test, msg]) => {
        const inp = $(s),
          fld = inp.closest(".field"),
          err = $(".err", fld),
          good = test(inp.value);
        fld.classList.toggle("bad", !good);
        err.textContent = good ? "" : msg;
        if (!good && ok) {
          inp.focus();
          ok = false;
        }
      });
      if (!ok) return;
      const data = Object.fromEntries(new FormData(s2));
      $("#bkErr").textContent = "";
      if (BOOK_URL) {
        const btn = $(".bk-submit", s2);
        btn.disabled = true;
        btn.textContent = "Scheduling...";
        try {
          const r = await fetch(BOOK_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              calendarId: CAL,
              slot: sel.slot,
              timezone: tz,
              ...data,
            }),
          });
          if (!r.ok) throw new Error(r.status);
        } catch (err) {
          btn.disabled = false;
          btn.textContent = "Schedule Call";
          $("#bkErr").textContent =
            "That time could not be booked. Please pick another time or try again.";
          return;
        }
      }
      $("#bkDone").textContent =
        "Intro Strategy Call on " +
        $("#bkWhen").textContent +
        ". A confirmation will go to " +
        data.email +
        ".";
      $("#bkPreview").hidden = !!BOOK_URL;
      step(3);
    });

    tzLabel();
    // load open times once the section is close to the viewport
    new IntersectionObserver(
      (es, o) => {
        if (es[0].isIntersecting) {
          o.disconnect();
          render();
        }
      },
      { rootMargin: "600px" },
    ).observe(bk);
  }

  /* ---------- showreel plays inside its card ---------- */
  {
    const card = $(".sv-vid"),
      play = $(".play", card);
    play.addEventListener("click", (e) => {
      e.preventDefault();
      if (card.classList.contains("playing")) return;
      const v = document.createElement("video");
      v.className = "sv-video";
      v.src = play.href;
      v.controls = true;
      v.playsInline = true;
      v.autoplay = true;
      v.preload = "auto";
      v.setAttribute("aria-label", "Dental Media Corp showreel");
      card.append(v);
      card.classList.add("playing");
      v.play().catch(() => {});
    });
  }

  /* ---------- FAQ accordion (one open) ---------- */
  const fqs = $$(".fq");
  fqs.forEach((f) =>
    $("button", f).addEventListener("click", () => {
      const open = !f.classList.contains("open");
      fqs.forEach((x) => {
        x.classList.toggle("open", x === f && open);
        $("button", x).setAttribute("aria-expanded", x === f && open);
      });
    }),
  );

  /* ---------- counters ---------- */
  function count(el, delay = 0) {
    const to = +el.dataset.to,
      dec = +(el.dataset.dec || 0),
      pre = el.dataset.pre || "",
      suf = el.dataset.suf || "",
      o = { v: 0 };
    gsap.to(o, {
      v: to,
      duration: 1.8,
      delay,
      ease: "power3.out",
      onUpdate: () => {
        el.textContent = pre + (dec ? o.v.toFixed(dec) : Math.round(o.v)) + suf;
      },
    });
  }

  /* ---------- scroll choreography (created in page order) ---------- */
  if (hasG && !reduce) {
    // hero intro
    const tl = gsap.timeline({ delay: 0.1 });
    tl.from(
      "#hCard .h-media",
      { scale: 1.25, duration: 2, ease: "expo.out" },
      0,
    )
      .from(
        ".nav",
        { y: -30, opacity: 0, duration: 1, ease: "power3.out" },
        0.4,
      )
      .from(
        "#hCard h1 .ln > span",
        { yPercent: 110, duration: 1.2, ease: "expo.out", stagger: 0.09 },
        0.75,
      )
      .from(
        "#hCard .h-fade",
        {
          y: 30,
          opacity: 0,
          duration: 1,
          ease: "power3.out",
          stagger: 0.08,
        },
        1.05,
      )
      .from(
        "#hCard .h-pop",
        {
          y: 40,
          opacity: 0,
          scale: 0.94,
          duration: 1,
          ease: "back.out(1.4)",
          stagger: 0.1,
        },
        1.15,
      );
    gsap.to("#hCard .h-media", {
      yPercent: 6,
      ease: "none",
      scrollTrigger: {
        trigger: "#hCard",
        start: "top top",
        end: "bottom top",
        scrub: true,
      },
    });

    // tag cloud: the lime tag hops between treatments
    const tags = $$(".tagcloud .t"),
      plus = $$(".tagcloud .p");
    let ti = 1;
    setInterval(() => {
      if (document.hidden) return;
      ti = (ti + 1) % tags.length;
      tags.forEach((t, i) => t.classList.toggle("on", i === ti));
      plus.forEach((p, i) =>
        p.classList.toggle("on", i === (ti + 2) % plus.length),
      );
    }, 2400);

    // about statement fills in word by word
    gsap.fromTo(
      $$(".w", say),
      { color: "#B8C0BD" },
      {
        color: "#0F1716",
        stagger: 0.05,
        ease: "none",
        scrollTrigger: {
          trigger: say,
          start: "top 78%",
          end: "bottom 45%",
          scrub: true,
        },
      },
    );

    // bento
    gsap.from(".bx", {
      y: 70,
      opacity: 0,
      duration: 1.2,
      ease: "expo.out",
      stagger: 0.08,
      scrollTrigger: { trigger: ".bento", start: "top 85%" },
    });
    ScrollTrigger.create({
      trigger: ".bento",
      start: "top 80%",
      once: true,
      onEnter: () => {
        $$(".bento [data-to]").forEach((el, i) => count(el, 0.2 + i * 0.1));
        const r = $(".b1 .num"),
          o = { a: 0, b: 0 };
        gsap.to(o, {
          a: 5,
          b: 20,
          duration: 1.8,
          delay: 0.2,
          ease: "power3.out",
          onUpdate: () => {
            r.textContent = Math.round(o.a) + "-" + Math.round(o.b) + "×";
          },
        });
      },
    });

    // headings
    $$("main .h2").forEach((h) =>
      gsap.from(h, {
        y: 50,
        opacity: 0,
        duration: 1.2,
        ease: "expo.out",
        scrollTrigger: { trigger: h, start: "top 90%" },
      }),
    );

    // treatments slide in from the right
    gsap.from(".tcard", {
      x: 120,
      opacity: 0,
      duration: 1.3,
      ease: "expo.out",
      stagger: 0.07,
      scrollTrigger: { trigger: "#tRow", start: "top 85%" },
    });

    // services: glass cards rise, channel logos pop, numbers count
    gsap.from(".tagpill, .sv-head p", {
      y: 30,
      opacity: 0,
      duration: 1,
      ease: "expo.out",
      stagger: 0.08,
      scrollTrigger: { trigger: ".sv-head", start: "top 88%" },
    });
    gsap.from(".sv-grid > *", {
      y: 70,
      opacity: 0,
      duration: 1.2,
      ease: "expo.out",
      stagger: 0.09,
      scrollTrigger: { trigger: ".sv-grid", start: "top 85%" },
    });
    gsap.from(".logos span", {
      scale: 0,
      duration: 0.8,
      ease: "back.out(2)",
      stagger: 0.07,
      delay: 0.3,
      scrollTrigger: { trigger: ".sv-grid", start: "top 85%" },
    });
    ScrollTrigger.create({
      trigger: ".sv-grid",
      start: "top 80%",
      once: true,
      onEnter: () =>
        $$(".sv-grid [data-to]").forEach((el, i) => count(el, 0.35 + i * 0.15)),
    });
    gsap.fromTo(
      ".sv-vid .phx",
      { yPercent: -5 },
      {
        yPercent: 5,
        ease: "none",
        scrollTrigger: {
          trigger: ".sv-vid",
          start: "top bottom",
          end: "bottom top",
          scrub: true,
        },
      },
    );

    // stats band
    gsap.fromTo(
      ".st-panel",
      { clipPath: "inset(6% 4% 6% 4% round 28px)" },
      {
        clipPath: "inset(0% 0% 0% 0% round 28px)",
        ease: "none",
        scrollTrigger: {
          trigger: ".st-panel",
          start: "top 95%",
          end: "top 45%",
          scrub: true,
        },
      },
    );
    gsap.from(".stc", {
      y: 70,
      opacity: 0,
      duration: 1.2,
      ease: "expo.out",
      stagger: 0.08,
      scrollTrigger: { trigger: ".st-grid", start: "top 85%" },
    });
    ScrollTrigger.create({
      trigger: ".st-grid",
      start: "top 80%",
      once: true,
      onEnter: () =>
        $$(".st-grid [data-to]").forEach((el, i) => count(el, 0.15 + i * 0.1)),
    });

    // case studies: horizontal while pinned on desktop, native swipe on mobile
    const mm = gsap.matchMedia();
    mm.add("(min-width: 900px)", () => {
      const pin = $("#cPin"),
        tr = $("#cTrack"),
        cards = $$(".ccard", tr);
      const dist = () => Math.max(0, tr.scrollWidth - innerWidth);
      gsap.to(tr, {
        x: () => -dist(),
        ease: "none",
        scrollTrigger: {
          trigger: pin,
          start: "center center",
          end: () => "+=" + dist(),
          scrub: 0.7,
          pin: true,
          invalidateOnRefresh: true,
          onUpdate: (s) => {
            $("#cBar").style.transform =
              "scaleX(" + (0.33 + s.progress * 0.67) + ")";
            $("#cCount").textContent =
              pad(
                Math.min(
                  cards.length,
                  1 + Math.round(s.progress * (cards.length - 1)),
                ),
              ) +
              " / " +
              pad(cards.length);
          },
        },
      });
    });
    gsap.from(".ccard", {
      y: 80,
      opacity: 0,
      duration: 1.2,
      ease: "expo.out",
      stagger: 0.1,
      scrollTrigger: { trigger: "#cTrack", start: "top 90%" },
    });
    $$("#cTrack .cc-media .phx").forEach((img) =>
      gsap.fromTo(
        img,
        { yPercent: -5 },
        {
          yPercent: 5,
          ease: "none",
          scrollTrigger: {
            trigger: "#cPin",
            start: "top bottom",
            end: "bottom top",
            scrub: true,
          },
        },
      ),
    );

    // added sections: cards rise in batches as they enter
    gsap.set(".up", { y: 60, opacity: 0 });
    ScrollTrigger.batch(".up", {
      start: "top 90%",
      once: true,
      onEnter: (b) =>
        gsap.to(b, {
          y: 0,
          opacity: 1,
          duration: 1.1,
          ease: "expo.out",
          stagger: 0.08,
          overwrite: true,
        }),
    });
    const stSteps = $$(".step");
    stSteps.forEach((st, i) => {
      if (i === stSteps.length - 1) return;
      gsap.to(st, {
        scale: 0.9 + i * 0.012,
        ease: "none",
        scrollTrigger: {
          trigger: stSteps[i + 1],
          start: "top bottom",
          end: "top 30%",
          scrub: true,
        },
      });
    });
    gsap.from(".phone", {
      y: 90,
      duration: 1.4,
      ease: "expo.out",
      scrollTrigger: { trigger: ".sys-a", start: "top 75%" },
    });
    gsap.from(".callpill", {
      y: -30,
      opacity: 0,
      duration: 0.9,
      ease: "back.out(1.6)",
      delay: 0.6,
      scrollTrigger: { trigger: ".sys-a", start: "top 75%" },
    });
    gsap.from("#zip span", {
      scale: 0,
      duration: 0.6,
      ease: "back.out(2)",
      stagger: { each: 0.04, from: "center" },
      scrollTrigger: { trigger: "#zip", start: "top 85%" },
    });
    gsap.to("#zip .you", {
      scale: 1.1,
      duration: 0.9,
      ease: "sine.inOut",
      yoyo: true,
      repeat: -1,
      delay: 1.6,
    });
    gsap.from("#calGrid span", {
      scale: 0.4,
      opacity: 0,
      duration: 0.5,
      ease: "back.out(2)",
      stagger: 0.012,
      scrollTrigger: { trigger: "#calGrid", start: "top 85%" },
    });

    // faq
    gsap.from(".fq", {
      y: 40,
      opacity: 0,
      duration: 1,
      ease: "expo.out",
      stagger: 0.05,
      scrollTrigger: { trigger: "#fBox", start: "top 85%" },
    });

    // contact panel opens up
    gsap.fromTo(
      "#ctPanel",
      { clipPath: "inset(10% 8% 10% 8% round 40px)" },
      {
        clipPath: "inset(0% 0% 0% 0% round 40px)",
        ease: "none",
        scrollTrigger: {
          trigger: "#ctPanel",
          start: "top 95%",
          end: "top 40%",
          scrub: true,
        },
      },
    );
    gsap.from(".ct-copy > *, .ct-body", {
      y: 30,
      opacity: 0,
      duration: 1,
      ease: "power3.out",
      stagger: 0.06,
      scrollTrigger: { trigger: "#ctPanel", start: "top 60%" },
    });

    // footer
    gsap.from(".f-grid > *", {
      y: 40,
      opacity: 0,
      duration: 1,
      ease: "expo.out",
      stagger: 0.08,
      scrollTrigger: { trigger: ".foot", start: "top 90%" },
    });

    addEventListener("load", () => ScrollTrigger.refresh());
  }

  // Treatments links in the header jump to a specific card
  DMC.onAnchor.push((a) => {
    if (a.dataset.tcard) tSet(+a.dataset.tcard);
  });

  // arriving from another page with a #hash (e.g. Book a Demo): land on it
  // once ScrollTrigger has added its pin spacers
  if (location.hash.length > 1)
    addEventListener("load", () => {
      const t = document.getElementById(location.hash.slice(1));
      if (!t) return;
      if (DMC.lenis)
        DMC.lenis.scrollTo(t, { immediate: true, force: true, offset: -90 });
      else t.scrollIntoView();
    });
})();
