// Defaults for every piece page in src/work/<slug>/index.md
export default {
  layout: "piece.njk",
  section: "main",
  media: [],
  eleventyComputed: {
    slug: (data) => data.page.filePathStem.split("/").at(-2),
    // Gallery-only cards (linkTo: <slug>) get no page of their own.
    permalink: (data) => data.linkTo ? false : `/work/${data.page.filePathStem.split("/").at(-2)}/`,
    dir: (data) => `work/${data.page.filePathStem.split("/").at(-2)}`,
  },
};
