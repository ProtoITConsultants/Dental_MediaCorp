const { chromium } = require("playwright-core");
const path = require("path");
const { pathToFileURL } = require("url");
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe" });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 2.4 });
  await p.goto(pathToFileURL(path.join(__dirname, "screen.html")).href, { waitUntil: "load", timeout: 90000 });
  await p.waitForTimeout(2500);
  await p.screenshot({ path: path.join(__dirname, "screen.png") });
  await b.close();
  console.log("ok");
})();
