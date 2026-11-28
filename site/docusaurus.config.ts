import {themes as prismThemes} from 'prism-react-renderer';
import type {Config, Plugin} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

/**
 * Split stable vendor code out of the application shell (main.js).
 *
 * main.js is eager on every route; react/react-dom/scheduler alone are
 * ~150 KB raw in it. Extracting them into a separate chunk changes their
 * cache behaviour: the vendor chunk hash stays stable across deploys, so
 * returning visitors keep it cached while app code (main.js) rotates.
 * Same for the eagerly-included search runtime (lunr + language trimmers).
 * Total JS is unchanged; the largest single chunk and main.js shrink.
 * Measured 2026-11-28 (see docs/performance.md).
 */
function vendorSplitPlugin(): Plugin {
  return {
    name: 'vendor-split',
    configureWebpack(_config, isServer) {
      if (isServer) {
        return {};
      }
      if (isServer) {
        return {};
      }
      return {
        optimization: {
          splitChunks: {
            cacheGroups: {
              framework: {
                test: /[\\/]node_modules[\\/](react|react-dom|scheduler)[\\/]/,
                name: 'framework',
                chunks: 'all',
                priority: 60,
                enforce: true,
                reuseExistingChunk: true,
              },
              search: {
                test: /[\\/]node_modules[\\/](@easyops-cn[\\/][^\\/]+|lunr[^\\/]*)[\\/]/,
                name: 'search',
                chunks: 'all',
                priority: 55,
                enforce: true,
                reuseExistingChunk: true,
              },
            },
          },
        },
      };
    },
  };
}

const config: Config = {
  title: 'SOGo User Guide',
  tagline: 'Step-by-step tutorials for SOGo groupware',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://tobias-weiss-ai-xr.github.io',
  baseUrl: process.env.FORCE_BASE_URL || '/docmakerai/',

  organizationName: 'tobias-weiss-ai-xr',
  projectName: 'docmakerai',

  onBrokenLinks: 'warn',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'de'],
    localeConfigs: {
      en: { label: 'English' },
      de: { label: 'Deutsch' },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          path: 'docs',
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
          editUrl: undefined,
          lastVersion: '5',
          includeCurrentVersion: false,
          versions: {
            '5': {
              label: 'SOGo 5',
              path: 'sogo5',
            },
            '6': {
              label: 'SOGo 6',
              path: 'sogo6',
            },
          },
          remarkPlugins: [],
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    vendorSplitPlugin,
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'suite',
        path: 'suite-docs',
        routeBasePath: 'suite',
        sidebarPath: './suite-sidebars.ts',
        editUrl: undefined,
        breadcrumbs: true,
      },
    ],
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['en', 'de'],
        indexDocs: true,
        indexPages: true,
        docsRouteBasePath: ['/', 'suite'],
        docsDir: ['docs', 'suite-docs', 'versioned_docs'],
        searchBarPosition: 'right',
        highlightSearchTermsOnTargetPage: true,
      },
    ],
  ],

  themeConfig: {
    image: 'img/social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
      navbar: {
        title: 'SOGo User Guide',
        logo: {
          alt: 'SOGo User Guide Logo',
          src: 'img/logo.svg',
          // Default brand target; src/theme/Navbar/Logo overrides this
          // per version (brand follows the version being read).
          href: '/sogo5/',
        },
        items: [
          { to: '/suite', label: 'openEduSuite', position: 'left' },
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'SOGo',
          },
          {
            type: 'docsVersionDropdown',
            position: 'right',
            dropdownItemsAfter: [],
            dropdownActiveClassDisabled: true,
          },
          {
            type: 'localeDropdown',
            position: 'right',
          },
          {
            href: 'https://github.com/tobias-weiss-ai-xr/docmakerai',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'SOGo',
            items: [
              {
                label: 'SOGo 5 Basics',
                to: '/sogo5/',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'openEduSuite',
                to: '/suite/',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/tobias-weiss-ai-xr/docmakerai',
              },
              {
                label: 'openedusuite.org',
                href: 'https://www.openedusuite.org',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} DocMaker AI. Built with Docusaurus.`,
      },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
