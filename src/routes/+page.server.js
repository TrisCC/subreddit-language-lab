import fs from "fs/promises";
import path from "path";

/** @type {import('./$types').PageServerLoad} */
export async function load() {
  const metadataFile = path.join(process.cwd(), "static", "data_processed", "all_subreddit_metadata.json");

  try {
    const metadataContent = await fs.readFile(metadataFile, "utf-8");
    const metadata = JSON.parse(metadataContent);
    const subreddits = Object.keys(metadata);
    return { subreddits, metadata };
  } catch (e) {
    // If the file doesn't exist, return an empty array
    return { subreddits: [], metadata: {} };
  }
}
