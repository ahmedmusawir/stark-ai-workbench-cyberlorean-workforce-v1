// Minimal Next.js standalone-output overlay — copy when the target repo has NO next.config.*.
// Authorization requirement (see SKILL.md §4): this is a product-tree change.
//   Path A (preferred): Director commits this file into the repo; identity = successor commit SHA.
//   Path B: Director explicitly approves this file as a hashed staging overlay;
//           identity = candidate SHA + this file's SHA-256.
// Rules: keep the config additive (only `output`), never carry it into a repo that already
// has a next.config.js/ts/mjs, and record the hash in the overlay manifest + run record.
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
};

export default nextConfig;