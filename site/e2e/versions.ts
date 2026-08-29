/**
 * Documentation versions under test.
 * Every version-agnostic spec loops over these; site-level specs stay single.
 */
export const VERSIONS = ['5', '6'] as const;

/** True when running against the live GitHub Pages deploy. Some hosting
 *  behaviors (trailing-slash 308s, explicit index.html serving, locale
 *  redirects) exist only there — gate hosting-semantics tests on it. */
export const ON_PROD_DEPLOY =
  !process.env.PLAYWRIGHT_BASE_URL ||
  process.env.PLAYWRIGHT_BASE_URL.includes('github.io');
