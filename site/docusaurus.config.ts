import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

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
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
      navbar: {
        title: 'SOGo User Guide',
        logo: {
          alt: 'SOGo Logo',
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
            label: 'Tutorials',
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
            title: 'Tutorials',
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
