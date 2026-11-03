// Accessibility check for the built book (WCAG 2.1 A and AA rules of axe-core).
//
// Usage, from a folder where axe-core and puppeteer-core are installed:
//   npm i axe-core puppeteer-core
//   CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
//     node /path/to/scripts/check_accessibility.mjs /path/to/_build/html [screenshot_dir]
//
// Every page is checked in light mode and in dark mode. The script exits with
// status 1 if axe reports any violation. With a screenshot folder, it also saves
// a full-page PNG of each page in each mode for a visual check.
import { createRequire } from "node:module";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const require = createRequire(path.join(process.cwd(), "noop.js"));
const puppeteer = require("puppeteer-core");
const axeSource = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");

const root = path.resolve(process.argv[2] || "_build/html");
const shots = process.argv[3];
const chrome = process.env.CHROME ||
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css",
  ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png",
  ".jpg": "image/jpeg", ".ico": "image/x-icon", ".woff2": "font/woff2" };

// On GitHub Pages the site is built with BASE_URL=/<repository>; strip it here.
const baseUrl = (process.env.BASE_URL || "").replace(/\/$/, "");
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (baseUrl && p.startsWith(baseUrl)) p = p.slice(baseUrl.length) || "/";
  let f = path.join(root, p);
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, "index.html");
  if (!fs.existsSync(f)) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { "Content-Type": types[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});
await new Promise((r) => server.listen(0, r));
const base = `http://localhost:${server.address().port}`;

const pages = fs.readdirSync(root)
  .filter((d) => fs.existsSync(path.join(root, d, "index.html")))
  .map((d) => `/${d}/`);
pages.unshift("/");

const browser = await puppeteer.launch({ executablePath: chrome, headless: true,
  args: ["--no-sandbox"] });
let total = 0;
for (const scheme of ["light", "dark"]) {
  for (const p of pages) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 900 });
    await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: scheme }]);
    await page.goto(base + baseUrl + p, { waitUntil: "networkidle0" });
    await page.evaluate(axeSource);
    const result = await page.evaluate(async () =>
      await window.axe.run(document, {
        runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] },
      }));
    const n = result.violations.reduce((s, v) => s + v.nodes.length, 0);
    total += n;
    console.log(`${scheme.padEnd(5)} ${p.padEnd(22)} violations: ${n}` +
      `  (passed rules: ${result.passes.length}, needs review: ${result.incomplete.length})`);
    for (const v of result.violations) {
      console.log(`   - ${v.id} [${v.impact}] ${v.help}`);
      for (const node of v.nodes.slice(0, 5)) console.log(`       ${node.target.join(" ")}`);
    }
    if (shots) {
      fs.mkdirSync(shots, { recursive: true });
      const name = (p === "/" ? "index" : p.replaceAll("/", "")) + `-${scheme}.png`;
      await page.screenshot({ path: path.join(shots, name), fullPage: true });
    }
    await page.close();
  }
}
await browser.close();
server.close();
console.log(total === 0 ? "No WCAG 2.1 A/AA violations found." : `${total} violations found.`);
process.exit(total === 0 ? 0 : 1);
