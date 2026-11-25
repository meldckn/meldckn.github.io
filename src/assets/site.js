// Small progressive enhancements. The site works without this file.

// ---- Masonry: fill columns left-to-right so the order reads across rows ----
function columnCount() {
  if (window.matchMedia("(min-width: 1100px)").matches) return 3;
  if (window.matchMedia("(min-width: 640px)").matches) return 2;
  return 1;
}

function layoutMasonry(grid, count) {
  const cards = grid._cards || (grid._cards = [...grid.querySelectorAll(":scope > .card, .masonry-col > .card")]);
  const cols = Array.from({ length: count }, () => {
    const col = document.createElement("div");
    col.className = "masonry-col";
    return col;
  });
  const heights = new Array(count).fill(0);
  const CAPTION = 0.12; // caption + spacing, relative to column width
  for (const card of cards) {
    const img = card.querySelector("img");
    const w = Number(img?.getAttribute("width")) || 1;
    const h = Number(img?.getAttribute("height")) || 1;
    const i = heights.indexOf(Math.min(...heights));
    cols[i].appendChild(card);
    heights[i] += h / w + CAPTION;
  }
  grid.replaceChildren(...cols);
  grid.classList.add("is-laid-out");
  grid._count = count;
}

function initMasonry() {
  const grids = document.querySelectorAll("[data-masonry]");
  if (!grids.length) return;
  const run = () => {
    const n = columnCount();
    grids.forEach((g) => { if (g._count !== n) layoutMasonry(g, n); });
  };
  run();
  window.addEventListener("resize", run, { passive: true });
}

// ---- Gentle fade-up as things scroll into view ----
function initReveal() {
  const items = document.querySelectorAll(".card, .piece-hero, .piece-info, .rail-wrap");
  if (!("IntersectionObserver" in window)) return;
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      e.target.classList.add("is-visible");
      io.unobserve(e.target);
    }
  }, { rootMargin: "0px 0px -6% 0px", threshold: 0.01 });
  items.forEach((el, i) => {
    el.classList.add("reveal");
    // Slight stagger for items that start on screen together.
    el.style.transitionDelay = `${Math.min(i % 3, 2) * 70}ms`;
    io.observe(el);
  });
}

// ---- Carousel of smaller photos: arrow buttons ----
function initRails() {
  document.querySelectorAll(".rail-wrap").forEach((wrap) => {
    const rail = wrap.querySelector(".rail");
    const back = wrap.querySelector(".rail-prev");
    const fwd = wrap.querySelector(".rail-next");
    const update = () => {
      const max = rail.scrollWidth - rail.clientWidth;
      back.hidden = rail.scrollLeft <= 4;
      fwd.hidden = rail.scrollLeft >= max - 4;
    };
    [back, fwd].forEach((btn) => btn.addEventListener("click", () => {
      rail.scrollBy({ left: Number(btn.dataset.dir) * rail.clientWidth * 0.75, behavior: "smooth" });
    }));
    rail.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update, { passive: true });
    rail.querySelectorAll("img").forEach((img) => img.addEventListener("load", update));
    update();
  });
}

// ---- Lightbox: every photo/video on a piece page, with prev/next ----
function initLightbox() {
  const dialog = document.querySelector(".lightbox");
  if (!dialog || typeof dialog.showModal !== "function") return;
  const stage = dialog.querySelector(".lightbox-stage");
  const count = dialog.querySelector(".lightbox-count");
  // The main photo first, then everything in the carousel.
  const buttons = [...document.querySelectorAll(".hero-btn, .rail-item")];
  const items = buttons.map((btn) => ({
    btn,
    video: btn.dataset.video,
    poster: btn.dataset.poster,
    alt: btn.querySelector("img")?.alt || "",
  }));
  let current = 0;
  dialog.classList.toggle("single", items.length < 2);

  function show(i) {
    current = (i + items.length) % items.length;
    const item = items[current];
    let el;
    if (item.video) {
      el = document.createElement("video");
      el.src = item.video;
      el.poster = item.poster || "";
      el.controls = true;
      el.playsInline = true;
      el.autoplay = true;
    } else {
      el = document.createElement("img");
      el.src = item.btn.dataset.full;
      el.alt = item.alt;
    }
    stage.replaceChildren(el);
    count.textContent = `${current + 1} / ${items.length}`;
  }
  const open = (i) => { show(i); dialog.showModal(); };

  items.forEach((item, i) => item.btn.addEventListener("click", () => open(i)));
  dialog.querySelector(".lightbox-prev").addEventListener("click", () => show(current - 1));
  dialog.querySelector(".lightbox-next").addEventListener("click", () => show(current + 1));
  dialog.querySelector(".lightbox-close").addEventListener("click", () => dialog.close());
  // Clicking the empty area around the photo closes it.
  dialog.addEventListener("click", (e) => { if (e.target === dialog || e.target === stage) dialog.close(); });
  dialog.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") show(current - 1);
    if (e.key === "ArrowRight") show(current + 1);
  });
  dialog.addEventListener("close", () => { stage.replaceChildren(); });
}

document.addEventListener("DOMContentLoaded", () => {
  initMasonry();
  initReveal();
  initRails();
  initLightbox();
});
