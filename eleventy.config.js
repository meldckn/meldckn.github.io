import fs from "node:fs";
import path from "node:path";
import Image from "@11ty/eleventy-img";

const IMAGE_WIDTHS = [600, 1200, 1800];

// Responsive <picture> for a photo stored in src/ (path relative to src/).
async function image(src, alt, sizes = "100vw", attrs = {}) {
  const meta = await Image(path.join("src", src), {
    widths: IMAGE_WIDTHS,
    formats: ["webp", "jpeg"],
    outputDir: "_site/img/",
    urlPath: "/img/",
    sharpJpegOptions: { quality: 82, progressive: true },
    sharpWebpOptions: { quality: 80 },
  });
  return Image.generateHTML(meta, {
    alt,
    sizes,
    loading: attrs.eager ? "eager" : "lazy",
    decoding: "async",
    ...(attrs.style ? { style: attrs.style } : {}),
    ...(attrs.class ? { class: attrs.class } : {}),
    ...(attrs.eager ? { fetchpriority: "high" } : {}),
  });
}

// URL of the largest generated JPEG (used by the lightbox).
async function imageFull(src) {
  const meta = await Image(path.join("src", src), {
    widths: IMAGE_WIDTHS,
    formats: ["webp", "jpeg"],
    outputDir: "_site/img/",
    urlPath: "/img/",
  });
  return meta.jpeg.at(-1).url;
}

export default function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/assets");
  // Favicon: pick a set from src/favicons/ ("cloud-i" or "textured").
  const FAVICON = "cloud-i";
  eleventyConfig.addPassthroughCopy({
    [`src/favicons/${FAVICON}/favicon.ico`]: "favicon.ico",
    [`src/favicons/${FAVICON}/favicon.png`]: "favicon.png",
    [`src/favicons/${FAVICON}/apple-touch-icon.png`]: "apple-touch-icon.png",
  });
  eleventyConfig.addPassthroughCopy("src/CNAME");
  // Videos and their poster frames are served as-is next to each piece page.
  eleventyConfig.addPassthroughCopy("src/work/**/*.{mp4,mov,webm}");
  eleventyConfig.addPassthroughCopy("src/work/**/*-poster.jpg");

  eleventyConfig.addAsyncShortcode("image", image);
  eleventyConfig.addAsyncShortcode("imageFull", imageFull);

  eleventyConfig.addFilter("srcExists", (file) => fs.existsSync(path.join("src", file)));
  eleventyConfig.addFilter("isVideo", (file) => /\.(mp4|mov|webm)$/i.test(file));
  eleventyConfig.addFilter("posterFor", (file) => file.replace(/\.[^.]+$/, "-poster.jpg"));
  eleventyConfig.addFilter("inSection", (pieces, section) =>
    pieces.filter((p) => p.data.section === section));

  const pieces = (api) =>
    api.getFilteredByGlob("src/work/*/index.md")
      .filter((p) => !p.data.hidden)
      .sort((a, b) => (a.data.order ?? 999) - (b.data.order ?? 999));
  eleventyConfig.addCollection("pieces", pieces);
  // Pieces with a page of their own (for Previous / Next links).
  eleventyConfig.addCollection("piecePages", (api) =>
    pieces(api).filter((p) => !p.data.linkTo));

  eleventyConfig.setServerOptions({ showAllHosts: false });

  return {
    dir: { input: "src", output: "_site", includes: "_includes" },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
}
