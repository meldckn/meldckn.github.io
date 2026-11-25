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
  const items = document.querySelectorAll(".card, .media-item");
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

// ---- Lightbox for piece photos ----
function initLightbox() {
  const dialog = document.querySelector(".lightbox");
  if (!dialog || typeof dialog.showModal !== "function") return;
  const img = dialog.querySelector("img");
  document.querySelectorAll(".zoom").forEach((btn) => {
    btn.addEventListener("click", () => {
      const thumb = btn.querySelector("img");
      img.src = btn.dataset.full;
      img.alt = thumb?.alt || "";
      dialog.showModal();
    });
  });
  dialog.addEventListener("click", () => dialog.close());
  dialog.addEventListener("close", () => { img.removeAttribute("src"); });
}

document.addEventListener("DOMContentLoaded", () => {
  initMasonry();
  initReveal();
  initLightbox();
});
