/**
 * Site-crawl edge cases, driven by the deployed sitemap.
 *
 * Catches whole-site regressions that single-page tests miss: broken
 * deploys (page 404s), empty doc bodies (the DocItem swizzle bug class),
 * leaked markup in meta descriptions, duplicate titles, link rot, and
 * broken/hashed image URLs.
 */

import { test, expect } from '@playwright/test';
import { VERSIONS } from './versions';

const BASE = (
  process.env.PLAYWRIGHT_BASE_URL ||
  'https://tobias-weiss-ai-xr.github.io/docmakerai/'
).replace(/\/?$/, '/');

/** Sitemaps bake absolute production URLs — retarget them so the same
 *  crawl verifies local preview builds (PLAYWRIGHT_BASE_URL) and prod. */
const PROD = 'https://tobias-weiss-ai-xr.github.io/docmakerai/';

async function sitemapUrls(request: ReturnType<typeof import('@playwright/test').request>): Promise<string[]> {
  const res = await request.get('sitemap.xml');
  expect(res.status()).toBe(200);
  const xml = await res.text();
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) =>
    m[1].replace(PROD, BASE)
  );
}

/** Docusaurus canonical/og:url use the absolute siteConfig.url (so they are
 *  production-hosted even in local previews), make no promise about the
 *  trailing slash, and de pages differ from en only by the /de/ prefix.
 *  Compare pathnames (host + slash agnostic) so local and prod share one
 *  source of truth. */
function pageSeo(url: string) {
  const page = new URL(url).pathname.replace(/\/$/, ''); // /docmakerai/sogo5/x
  const isDe = page.includes('/de/');
  const en = isDe ? page.replace('/de/', '/') : page;
  const de = isDe ? page : page.replace('/docmakerai/', '/docmakerai/de/');
  return { en, de, page };
}

/** Compare an emitted URL to a page pathname ignoring host + trailing slash. */
function samePage(emitted: string, page: string) {
  return new URL(emitted).pathname.replace(/\/$/, '') === page;
}

/** Parse the three hreflang alternate <link>s from minified served HTML. */
function headAlternates(html: string): Record<string, string> {
  return Object.fromEntries(
    [...html.matchAll(/rel=alternate href=([^ >]*) hreflang=([a-zA-Z-]+)/g)].map(
      (m) => [m[2], m[1]] as const
    )
  );
}

test.describe('Site crawl', () => {
  test('sitemap lists both doc versions, German pages, and hreflang alternates', async ({ request }) => {
    const urls = await sitemapUrls(request);
    expect(urls.length).toBeGreaterThan(40);

    const byVersion = Object.fromEntries(
      VERSIONS.map((v) => [v, urls.filter((u) => u.includes(`/sogo${v}/`))])
    );
    for (const v of VERSIONS) {
      expect(
        byVersion[v].length,
        `sitemap should list sogo${v} pages`
      ).toBeGreaterThan(20);
      // The German tree must be discoverable too (tools/generate_sitemap.py)
      expect(
        urls.filter((u) => u.includes(`/de/sogo${v}/`)).length,
        `sitemap should list German sogo${v} pages`
      ).toBeGreaterThan(20);
    }
    for (const url of urls) {
      expect(url.startsWith(BASE), `${url} must live under ${BASE}`).toBe(true);
    }

    const xml = await (await request.get('sitemap.xml')).text();
    expect(xml, 'German pages need hreflang alternates').toContain(
      'hreflang="de"'
    );
    expect(xml, 'alternate cluster needs an x-default (en)').toContain(
      'hreflang="x-default"'
    );
  });

  test('robots.txt points to the sitemap', async ({ request }) => {
    const res = await request.get('robots.txt');
    expect(res.status()).toBe(200);
    const body = await res.text();
    expect(body).toContain('User-agent');
    // Absolute production sitemap URL (required for crawlers), path-checked
    // so the suite also passes against local preview servers.
    expect(body).toMatch(/^Sitemap: .+\/sitemap\.xml$/m);
  });

  for (const v of VERSIONS) {
    test.describe(`sogo${v} crawl`, () => {
      test('every page returns 200 with rendered, non-empty content', async ({ request }) => {
        test.setTimeout(120_000);
        const urls = (await sitemapUrls(request)).filter(
          (u) =>
            u.includes(`/docmakerai/sogo${v}/`) &&
            !u.includes('/de/')
        );
        expect(urls.length).toBeGreaterThan(20);

        const titles = new Set<string>();
        const imgSrcs = new Set<string>();
        for (const url of urls) {
          const res = await request.get(url);
          expect(res.status(), `${url} must return 200`).toBe(200);
          const html = await res.text();

          // Doc body must render and not be empty (DocItem swizzle bug class)
          const start = html.indexOf('theme-doc-markdown');
          expect(start, `${url} has no doc markdown region`).toBeGreaterThan(-1);
          const end = html.indexOf('</article>', start);
          const body = html.slice(start, end > -1 ? end : undefined);
          expect(
            body.length,
            `${url} doc body suspiciously small (empty-body regression?)`
          ).toBeGreaterThan(200);

          // Title must exist and be unique across the version
          const title = html.match(/<title[^>]*>([^<]+)<\/title>/)?.[1] ?? '';
          expect(title, `${url} has an empty title`).toBeTruthy();
          expect(
            titles.has(title),
            `duplicate title "${title}" (also used by another page)`
          ).toBe(false);
          titles.add(title);

          // Meta description must be clean, human text — no leaked markup.
          // Served HTML minifies attributes (name=description, unquoted).
          const desc = html.match(/name="?description"? content="?([^">]*)"?/)?.[1] ?? '';
          expect(
            desc.length,
            `${url} has a too-short meta description`
          ).toBeGreaterThan(30);
          expect(
            desc,
            `${url} leaks markup into the meta description`
          ).not.toContain('<');

          // Exactly one h1 per page (document outline integrity)
          const h1Count = (html.match(/<h1[ >]/g) ?? []).length;
          expect(h1Count, `${url} must have exactly one h1`).toBe(1);

          // Titles must carry the site-name suffix (config/branding
          // regression). Both the English and the locally-translated German
          // site name contain "SOGo" — do not encode the exact translation.
          expect(
            title,
            `${url} title must carry the site name`
          ).toMatch(/ \| SOGo/);

          // Seo/SEO.tsx used to hardcode canonical + og:url to the SITE ROOT,
          // collapsing every page's signal into the homepage — each page must
          // now point canonically at itself.
          const { en, de, page } = pageSeo(url);
          const canonical =
            html.match(/rel=canonical href=([^ >]*)/)?.[1] ?? '';
          expect(canonical, `${url} needs a canonical`).toBeTruthy();
          expect(
            samePage(canonical, page),
            `${url} canonical must match the page (not the site root)`
          ).toBe(true);
          const ogUrl = html.match(/property=og:url content=([^ >]*)/)?.[1] ?? '';
          expect(
            samePage(ogUrl, page),
            `${url} og:url must match the page (not the site root)`
          ).toBe(true);

          // Every page must cite en + de + x-default hreflang alternates
          const alts = headAlternates(html);
          expect(
            Object.keys(alts).sort(),
            `${url} must cite en, de and x-default alternates`
          ).toEqual(['de', 'en', 'x-default']);
          expect(samePage(alts.en, en), `${url} en alternate`).toBe(true);
          expect(samePage(alts.de, de), `${url} de alternate`).toBe(true);
          expect(
            samePage(alts['x-default'], en),
            `${url} x-default alternate`
          ).toBe(true);

          // Doc pages render breadcrumbs (category trail). Exception: the
          // custom meta/spec pages (sogo-gaps, sogo-spec-*) render outside
          // the breadcrumb layout by design.
          if (!/(sogo-gaps|sogo-spec-)/.test(url)) {
            expect(
              html.includes('theme-doc-breadcrumbs'),
              `${url} has no breadcrumbs`
            ).toBe(true);
          }

          // Every img must carry an alt attribute (may be empty for decor)
          for (const img of html.match(/<img[^>]*>/g) ?? []) {
            expect(
              img,
              `${url} has an img without alt: ${img.slice(0, 80)}`
            ).toMatch(/\salt=/);
          }

          // No leaked framework tokens rendered as text (JSX bug class)
          for (const tok of ['>undefined<', '>NaN<', 'lorem ipsum', '>TODO<']) {
            expect(
              html.toLowerCase().includes(tok.toLowerCase()),
              `${url} leaks "${tok}" into rendered content`
            ).toBe(false);
          }

          // Same-page anchors must point at existing heading ids
          const ids = new Set(
            [...html.matchAll(/\sid="?([^" >]+)/g)].map((m) => m[1])
          );
          for (const m of html.matchAll(/href="?#([^" >]+)/g)) {
            const frag = m[1];
            if (!frag || frag.startsWith('__')) continue; // docusaurus internals
            expect(
              ids.has(frag),
              `${url} has a broken anchor #${frag}`
            ).toBe(true);
          }

          // Collect image sources for the whole-version resolution check
          for (const m of html.matchAll(/<img[^>]*?src="?([^" >]+)/g)) {
            if (m[1].startsWith('/docmakerai/')) imgSrcs.add(m[1]);
          }
        }

        // Every embedded image across the version resolves (hashed-asset class)
        expect(imgSrcs.size, 'version should embed images').toBeGreaterThan(20);
        for (const src of imgSrcs) {
          const res = await request.get(src);
          expect(res.status(), `broken image ${src}`).toBeLessThan(400);
        }
      });

      test('index page internal links all resolve', async ({ page, request }) => {
        test.setTimeout(120_000);
        await page.goto(`sogo${v}/`);

        const hrefs = await page
          .locator('a[href^="/docmakerai/"]')
          .evaluateAll((els) => [
            ...new Set(
              els.map((e) => (e as HTMLAnchorElement).getAttribute('href') || '')
            ),
          ]);
        expect(hrefs.length, 'index page should link to many docs pages').toBeGreaterThan(10);

        for (const href of hrefs) {
          if (href.includes('#')) continue; // same-page fragments
          const res = await request.get(href);
          expect(res.status(), `broken internal link ${href}`).toBe(200);
        }
      });

      test('images on key pages resolve (hashed asset regression)', async ({ page, request }) => {
        test.setTimeout(120_000);
        for (const path of [`sogo${v}/`, `sogo${v}/sogo-login/`]) {
          await page.goto(path);
          const srcs = await page
            .locator('img[src]')
            .evaluateAll((els) =>
              els.map((e) => (e as HTMLImageElement).getAttribute('src') || '')
            );
          for (const src of srcs) {
            expect(src, `image without src on ${path}`).toBeTruthy();
            const res = await request.get(src);
            expect(
              res.status(),
              `broken image ${src} on ${path}`
            ).toBeLessThan(400);
          }
        }
      });
      test('German pages render cleanly (sitemap-driven)', async ({ request }) => {
        test.setTimeout(120_000);
        const deUrls = (await sitemapUrls(request)).filter((u) =>
          u.includes(`/de/sogo${v}/`)
        );
        expect(deUrls.length, `German sogo${v} pages in sitemap`).toBeGreaterThan(
          20
        );

        const titles = new Set<string>();
        for (const url of deUrls) {
          const res = await request.get(url);
          expect(res.status(), `${url} must return 200`).toBe(200);
          const html = await res.text();

          // Localized pages are real pages: one h1, unique title, doc body
          const h1Count = (html.match(/<h1[ >]/g) ?? []).length;
          expect(h1Count, `${url} must have exactly one h1`).toBe(1);
          const title = html.match(/<title[^>]*>([^<]+)<\/title>/)?.[1] ?? '';
          expect(title, `${url} has an empty title`).toBeTruthy();
          expect(
            titles.has(title),
            `duplicate German title "${title}"`
          ).toBe(false);
          titles.add(title);
          const start = html.indexOf('theme-doc-markdown');
          expect(start, `${url} has no doc markdown region`).toBeGreaterThan(-1);

          // Localized meta descriptions must be clean human text too
          const desc = html.match(/name="?description"? content="?([^"]*)"?/)?.[1] ?? '';
          expect(
            desc.length,
            `${url} has a too-short meta description`
          ).toBeGreaterThan(30);
          expect(
            desc,
            `${url} leaks markup into the meta description`
          ).not.toContain('<');

          // Same canonical/og/alternate invariants as English pages — the
          // localization must not regress SEO wiring either.
          expect(
            title,
            `${url} title must carry the site name`
          ).toMatch(/ \| SOGo/);
          const { en, de, page } = pageSeo(url);
          const canonical =
            html.match(/rel=canonical href=([^ >]*)/)?.[1] ?? '';
          expect(canonical, `${url} needs a canonical`).toBeTruthy();
          expect(
            samePage(canonical, page),
            `${url} canonical must match the page (not the site root)`
          ).toBe(true);
          const ogUrl = html.match(/property=og:url content=([^ >]*)/)?.[1] ?? '';
          expect(
            samePage(ogUrl, page),
            `${url} og:url must match the page (not the site root)`
          ).toBe(true);
          const alts = headAlternates(html);
          expect(
            Object.keys(alts).sort(),
            `${url} must cite en, de and x-default alternates`
          ).toEqual(['de', 'en', 'x-default']);
          expect(samePage(alts.en, en), `${url} en alternate`).toBe(true);
          expect(samePage(alts.de, de), `${url} de alternate`).toBe(true);
          expect(
            samePage(alts['x-default'], en),
            `${url} x-default alternate`
          ).toBe(true);

          // No leaked framework tokens or template boilerplate
          for (const tok of ['>undefined<', '>NaN<', 'lorem ipsum', '>TODO<']) {
            expect(
              html.toLowerCase().includes(tok.toLowerCase()),
              `${url} leaks "${tok}" into rendered content`
            ).toBe(false);
          }

          // Same-page anchors must point at existing heading ids
          const ids = new Set(
            [...html.matchAll(/\sid="?([^" >]+)/g)].map((m) => m[1])
          );
          for (const m of html.matchAll(/href="?#([^" >]+)/g)) {
            const frag = m[1];
            if (!frag || frag.startsWith('__')) continue;
            expect(
              ids.has(frag),
              `${url} has a broken anchor #${frag}`
            ).toBe(true);
          }
        }
      });
    });
  }

  test('German index page links all resolve', async ({ request }) => {
    test.setTimeout(120_000);
    const res = await request.get('de/sogo5/');
    expect(res.status()).toBe(200);
    const html = await res.text();

    const hrefs = [
      ...new Set(
        [...html.matchAll(/href="?(\/docmakerai\/[^" >#]+)/g)].map((m) => m[1])
      ),
    ];
    expect(hrefs.length, 'de index should link to many pages').toBeGreaterThan(10);
    for (const href of hrefs) {
      const r = await request.get(href);
      expect(r.status(), `broken internal link ${href}`).toBe(200);
    }
  });

  test('unlisted template page stays reachable but noindexed and out of the sitemap', async ({
    request,
  }) => {
    // accessibility-section-template.md is unlisted: it must NOT be crawled
    // into the sitemap (Docusaurus emits robots noindex — our sitemap
    // generator re-implements that filter) yet stay accessible by direct URL.
    const inSitemap = (await sitemapUrls(request)).some((u) =>
      u.includes('accessibility-section-template')
    );
    expect(inSitemap, 'unlisted page must not appear in the sitemap').toBe(false);

    const res = await request.get('sogo5/accessibility-section-template/');
    expect(res.status(), 'unlisted page stays reachable').toBe(200);
    const html = await res.text();
    expect(html, 'unlisted page must carry robots noindex').toContain('noindex');
  });
});
