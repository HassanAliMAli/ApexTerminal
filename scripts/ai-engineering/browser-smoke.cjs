const path = require("node:path");
const os = require("node:os");

const root = process.env.AI_TOOLS_HOME || path.join(os.homedir(), ".local/share/apex-ai");
const { chromium } = require(path.join(root, "npm/node_modules/playwright"));
const { AxeBuilder } = require(path.join(root, "npm/node_modules/@axe-core/playwright"));

const fixture = `<!doctype html><html lang="en"><head><title>Fixture</title></head>
<body><main><h1>Fixture</h1><button onclick="this.textContent='Confirmed'">Confirm</button></main></body></html>`;

async function verify() {
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  try {
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto("data:text/html," + encodeURIComponent(fixture));
    await page.getByRole("button", { name: "Confirm" }).click({ timeout: 5_000 });
    await page.getByRole("button", { name: "Confirmed" }).waitFor({ timeout: 5_000 });
    const { violations } = await new AxeBuilder({ page }).analyze();
    if (violations.length > 0) {
      throw new Error("axe violations: " + violations.map(({ id }) => id).join(", "));
    }
    console.log("Playwright click passed. axe reported zero violations.");
  } finally {
    await browser.close();
  }
}

verify().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
