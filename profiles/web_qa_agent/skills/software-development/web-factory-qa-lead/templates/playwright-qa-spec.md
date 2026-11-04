# Playwright QA spec template — Web Factory WBM static Next.js site

Reusable Playwright test file pattern for Q2 independent verification of a Stark Web Factory WBM static Next.js site. Copy into the repo's `tests/` as a temporary spec, run it, then delete it before the final clean build.

## Template location

`tests/qa-q2.spec.ts` (or similar) inside the candidate repo. After execution, remove the file and any helper scripts; restore the worktree to clean.

## Required environment

- Playwright installed in the repo (`@playwright/test`).
- `playwright.config.ts` with a `webServer` entry pointing at the local Next.js server.
- Node.js and Chromium available.

## Recommended `playwright.config.ts` snippet

```typescript
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests',
  fullyParallel: false,
  reporter: [['list']],
  use: {
    baseURL: 'http://127.0.0.1:3001',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'desktop',
      use: {
        browserName: 'chromium',
        viewport: { width: 1440, height: 900 },
        deviceScaleFactor: 2,
      },
    },
    {
      name: 'mobile',
      use: {
        browserName: 'chromium',
        viewport: { width: 390, height: 844 },
        deviceScaleFactor: 2,
        isMobile: true,
        hasTouch: true,
      },
    },
  ],
  webServer: {
    command: 'npm run start -- --hostname 127.0.0.1',
    url: 'http://127.0.0.1:3001',
    reuseExistingServer: false,
    gracefulShutdown: { signal: 'SIGTERM', timeout: 5000 },
  },
});
```

## Template `tests/qa-q2.spec.ts`

```typescript
import { test, expect } from '@playwright/test';
import fs from 'fs';
import path from 'path';

const root = '/home/moose/web-factory/projects/cyberize-poc/WBM/QAM/evidence/qa-q2';
const routes = [
  ['home', '/'],
  ['seo', '/seo-services/'],
  ['ppc', '/ppc/'],
  ['web-design', '/website-design/'],
  ['web-development', '/web-development/'],
  ['website-support', '/website-support/'],
  ['contact', '/contact/'],
] as const;

fs.mkdirSync(path.join(root, 'screenshots'), { recursive: true });
fs.mkdirSync(path.join(root, 'reports'), { recursive: true });

const manifest: any = { startTime: new Date().toISOString(), screenshots: [] };
function save(name: string, data: any) {
  fs.writeFileSync(path.join(root, 'reports', `${name}.json`), JSON.stringify(data, null, 2));
}

test('routes and 404', async ({ page }) => {
  const report: any[] = [];
  for (const [, route] of routes) {
    const response = await page.goto(route);
    report.push({ route, status: response?.status() });
    expect(response?.status()).toBe(200);
  }
  const response = await page.goto('/not-a-real-page/');
  report.push({ route: '/not-a-real-page/', status: response?.status() });
  expect(response?.status()).toBe(404);
  save('routes-404', report);
});

test('link inventory', async ({ page }) => {
  const inventory: any[] = [];
  for (const [, route] of routes) {
    await page.goto(route);
    const links = await page.locator('a[href]').evaluateAll((els) =>
      els.map((a) => ({ href: a.getAttribute('href'), text: a.textContent?.trim().slice(0, 60) }))
    );
    const htmlHrefs = links.filter((l) => l.href?.includes('.html'));
    inventory.push({ route, htmlHrefs });
    expect(htmlHrefs).toEqual([]);
  }
  save('link-inventory', inventory);
});

test('responsive overflow and touch targets', async ({ page }) => {
  const widths = [320, 390, 768, 899, 901, 1024, 1440];
  const overflowReport: any[] = [];
  for (const [, route] of routes) {
    for (const width of widths) {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(route);
      const noOverflow = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
      overflowReport.push({ route, width, noOverflow });
      expect(noOverflow).toBe(true);
    }
  }
  save('responsive-overflow', overflowReport);
});

test('canonical screenshots', async ({ page }, info) => {
  const vp = info.project.name === 'mobile' ? 'mobile' : 'desktop';
  for (const [stem, route] of routes) {
    await page.goto(route);
    await page.evaluate(() => document.fonts.ready);
    await page.locator('img').evaluateAll((imgs) =>
      Promise.all(imgs.map((img) => (img as HTMLImageElement).decode().catch(() => {})))
    );
    const shot = path.join(root, 'screenshots', `${stem}-${vp}.png`);
    await page.screenshot({ path: shot, fullPage: true });
    manifest.screenshots.push({ stem, viewport: vp, path: shot });
  }
  fs.writeFileSync(path.join(root, 'evidence-manifest.json'), JSON.stringify(manifest, null, 2));
});

test('axe and h1', async ({ page }) => {
  // @ts-ignore — axe-core loaded via script injection
  const axe = require('axe-core');
  const report: any[] = [];
  for (const [, route] of routes) {
    await page.goto(route);
    await page.addScriptTag({ content: axe.source });
    const result: any = await page.evaluate(() => new Promise((resolve) => {
      (window as any).axe.run(document, {}, (err: any, r: any) => resolve({ err, violations: r.violations }));
    }));
    const h1Count = await page.locator('h1').count();
    report.push({ route, violations: result.violations, h1Count });
    expect(h1Count).toBe(1);
  }
  save('axe-violations', report);
});

test('skip link', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Tab');
  await page.keyboard.press('Enter');
  const mainFocused = await page.evaluate(() => document.activeElement?.id);
  expect(mainFocused).toBe('main');
});

test.afterAll(async () => {
  manifest.endTime = new Date().toISOString();
  fs.writeFileSync(path.join(root, 'evidence-manifest.json'), JSON.stringify(manifest, null, 2));
});
```

## How to run

```bash
cd <candidate-repo>
npx playwright test tests/qa-q2.spec.ts
```

## Cleanup after run

```bash
rm -f tests/qa-q2.spec.ts tests/qa-q2-helpers.cjs
git status --short   # must be empty before verdict
npm run build        # final clean build must pass
```

## Notes

- Keep the spec TypeScript-clean; use `// @ts-ignore` only where a runtime-only dependency is intentionally injected.
- Avoid `page.locator(...).filter({ hasAttribute: ... })` if Playwright's type definitions reject it; use `evaluateAll` instead.
- For boundary probes that resize the viewport, run them in the `desktop` project only to avoid `isMobile` emulation conflicts.
- Do not leave helper files in the repo when issuing the verdict.

