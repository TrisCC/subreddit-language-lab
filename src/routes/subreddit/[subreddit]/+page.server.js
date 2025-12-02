import { error } from "@sveltejs/kit";
import fs from "fs/promises";
import path from "path";

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
  const subreddit = params.subreddit;
  const filePath = path.join(
    process.cwd(),
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
