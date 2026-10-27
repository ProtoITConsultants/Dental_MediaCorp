/* =========================================================
   Dental Media Corp: service pages (services/<slug>/)
   Hero intro and scroll reveals. Needs site.js (window.DMC) first.
   ========================================================= */
(() => {
  const { $, $$, reduce, hasG, arrived } = window.DMC;
  if (!hasG || reduce) return;

  // hero intro: same beats as the home hero. When the page transition brought
  // us here the photo is already on screen at full size, so only the copy moves.
  const hero = $(".sp-hero"),
    media = $(".h-media", hero),
    at = arrived ? [0, 0.1, 0.15, 0.4, 0.5] : [0, 0.4, 0.75, 1.05, 1.15];
  const tl = gsap.timeline({ delay: arrived ? 0 : 0.1 });
  if (!arrived)
    tl.from(media, { scale: 1.25, duration: 2, ease: "expo.out" }, at[0]);
  tl.from(
    ".nav",
    { y: -30, opacity: 0, duration: 1, ease: "power3.out" },
    at[1],
  )
    .from(
      $$("h1 .ln > span", hero),
      { yPercent: 110, duration: 1.2, ease: "expo.out", stagger: 0.09 },
      at[2],
    )
    .from(
      $$(".h-fade", hero),
      { y: 30, opacity: 0, duration: 1, ease: "power3.out", stagger: 0.08 },
      at[3],
    )
    .from(
      $$(".h-pop", hero),
      {
        y: 40,
        opacity: 0,
        scale: 0.94,
        duration: 1,
        ease: "back.out(1.4)",
        stagger: 0.1,
      },
      at[4],
    );
  gsap.to(media, {
    yPercent: 6,
    ease: "none",
    scrollTrigger: {
      trigger: $(".h-card", hero),
      start: "top top",
      end: "bottom top",
      scrub: true,
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

  // cards rise in batches as they enter
  gsap.set(".sp-up", { y: 60, opacity: 0 });
  ScrollTrigger.batch(".sp-up", {
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
})();
