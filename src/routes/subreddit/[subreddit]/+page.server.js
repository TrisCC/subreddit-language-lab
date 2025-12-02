import { error } from "@sveltejs/kit";
import fs from "fs/promises";
import path from "path";

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
  const subreddit = params.subreddit;
  const filePath = path.join(
    process.cwd(),
    "static",
    "data_processed",
    `${subreddit}_analysis.json`
  );

  try {
    const data = await fs.readFile(filePath, "utf-8");
    return {
      subreddit,
      analysis: JSON.parse(data),
    };
  } catch (e) {
    throw error(404, "Subreddit analysis not found");
  }
}

/** @type {import('./$types').EntryGenerator} */
export async function entries() {
  const dataProcessedDir = path.join(process.cwd(), "static", "data_processed");
  try {
    const files = await fs.readdir(dataProcessedDir);
    return files
      .filter((file) => file.endsWith("_analysis.json"))
      .map((file) => ({ subreddit: file.replace("_analysis.json", "") }));
  } catch (e) {
    return [];
  }
}
