#!/usr/bin/env node
/**
 * axe-docs-check.mjs — local accessibility gate for the built Docusaurus site.
 *
 * Spawns the built-site server (site/build via `docusaurus serve`), runs axe-core
 * against the SOGo mail-compose pages (EN + DE) and fails on serious/critical
 * violations. Moderate/minor findings are printed as warnings only.
 *
 * Usage: node scripts/axe-docs-check.mjs   (after `npm run build`)
 */
import { spawn } from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const PORT = 3461;
const BASE = `http://localhost:${PORT}/docmakerai/`;
const PAGES = [
  { url: `${BASE}sogo5/sogo-mail-compose/`, label: "EN /sogo5/sogo-mail-compose/" },
  // Full dual-locale builds serve German under /de/…; single-locale `build --locale de`
  // puts German at the site root. Probe /de/ first, fall back to the root URL.
  { url: `${BASE}de/sogo5/sogo-mail-compose/`, alt: `${BASE}sogo5/sogo-mail-compose/`, label: "DE sogo-mail-compose" },
];
const TIMEOUT_MS = 120_000;

/** Walk up from the script location to the repo root (dir containing site/). */
function findRepoRoot() {
  let dir = path.dirname(fileURLToPath(import.meta.url));
  for (let i = 0; i < 6; i++) {
    if (fs.existsSync(path.join(dir, "site", "package.json"))) return dir;
    dir = path.dirname(dir);
  }
  throw new Error("repo root (with site/) not found from script location");
}

const repoRoot = findRepoRoot();
const siteDir = path.join(repoRoot, "site");
const buildDir = path.join(siteDir, "build");
if (!fs.existsSync(buildDir)) {
  console.error("FATAL: site/build missing — run `npm run build -- --locale en && npm run build -- --locale de` first.");
  process.exit(2);
}

// Resolve axe-core source + playwright from site/node_modules (script may be
// invoked from repo root or site/).
const siteRequire = createRequire(path.join(siteDir, "package.json"));
const axeSource = fs.readFileSync(siteRequire.resolve("axe-core/axe.min.js"), "utf8");
let chromium;
try {
  ({ chromium } = siteRequire("playwright-core"));
} catch {
  ({ chromium } = siteRequire("@playwright/test"));
}

function waitForServer(url, timeoutMs) {
  const start = Date.now();
  return new Promise((resolve, reject) => {
    const poll = () => {
      const req = http.get(url, (res) => {
        res.resume();
        if (res.statusCode === 200) return resolve();
        retry();
      });
      req.on("error", retry);
      req.setTimeout(2000, () => { req.destroy(); retry(); });
    };
    const retry = () => {
      if (Date.now() - start > timeoutMs) return reject(new Error(`server not ready at ${url}`));
      setTimeout(poll, 700);
    };
    poll();
  });
}

function summarize(violations) {
  const serious = violations.filter((v) => v.impact === "serious" || v.impact === "critical");
  const minor = violations.filter((v) => v.impact !== "serious" && v.impact !== "critical");
  for (const v of violations) {
    const nodes = v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ");
    console.log(`  [${v.impact}] ${v.id} — ${v.help} — nodes: ${nodes}`);
  }
  return { serious, minor };
}

let server;
let failed = false;
try {
  server = spawn("npx", ["docusaurus", "serve", "--dir", "build", "--port", String(PORT)], {
    cwd: siteDir,
    stdio: "ignore",
    detached: true,
  });
  await waitForServer(`${BASE}`, TIMEOUT_MS);
  console.log(`server ready on ${BASE}`);

  const browser = await chromium.launch();
  const page = await browser.newPage();

  for (const entry of PAGES) {
    let url = entry.url;
    let res = await page.goto(url, { waitUntil: "networkidle", timeout: 60_000 });
    if ((!res || res.status() !== 200) && entry.alt) {
      url = entry.alt;
      res = await page.goto(url, { waitUntil: "networkidle", timeout: 60_000 });
    }
    if (!res || res.status() !== 200) throw new Error(`HTTP ${res ? res.status() : "?"} for ${url}`);
    await page.addScriptTag({ content: axeSource });
    const results = await page.evaluate(() =>
      axe.run(document, {
        resultTypes: ["violations"],
        runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"] },
      })
    );
    console.log(`\n=== ${entry.label} (${url}): ${results.violations.length} violation type(s)`);
    const { serious, minor } = summarize(results.violations);
    if (serious.length > 0) { failed = true; console.log(`  -> FAIL: ${serious.length} serious/critical finding(s)`); }
    if (minor.length > 0) console.log(`  -> warn: ${minor.length} moderate/minor finding(s) (advisory)`);
  }

  await browser.close();
} catch (err) {
  console.error("FATAL:", err.message);
  failed = true;
} finally {
  if (server) {
    try { process.kill(-server.pid, "SIGTERM"); } catch { server.kill("SIGTERM"); }
  }
}
process.exit(failed ? 1 : 0);
