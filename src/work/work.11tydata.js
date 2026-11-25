// Defaults for every piece page in src/work/<slug>/index.md
export default {
  layout: "piece.njk",
  section: "main",
  media: [],
  eleventyComputed: {
    slug: (data) => data.page.filePathStem.split("/").at(-2),
    permalink: (data) => `/work/${data.page.filePathStem.split("/").at(-2)}/`,
    dir: (data) => `work/${data.page.filePathStem.split("/").at(-2)}`,
  },
};
