import fs from "fs/promises";
import path from "path";

/** @type {import('./$types').PageServerLoad} */
export async function load() {
  const dataProcessedDir = path.join(process.cwd(), "static", "data_processed");

  try {
    const files = await fs.readdir(dataProcessedDir);
    const subreddits = files
      .filter((file) => file.endsWith("_analysis.json"))
      .map((file) => file.replace("_analysis.json", ""));

    return { subreddits };
  } catch (e) {
    // If the directory doesn't exist, return an empty array
    return { subreddits: [] };
  }
}
