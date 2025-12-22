import fs from "fs/promises";
import path from "path";

export const prerender = true;
export const trailingSlash = "always";

/** @type {import('./$types').LayoutServerLoad} */
export async function load() {
  const dataProcessedDir = path.join(process.cwd(), "static", "data_processed");
  try {
    const files = await fs.readdir(dataProcessedDir);
    const subreddits = files
      .filter((file) => file.endsWith("_analysis.json"))
      .map((file) => file.replace("_analysis.json", ""));
    return {
      subreddits,
    };
  } catch (e) {
    return {
      subreddits: [],
    };
  }
}
