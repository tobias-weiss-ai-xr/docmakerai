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

  url: process.env.SITE_URL || 'https://docs.contextual-intelligence.org',
  baseUrl: '/',

  organizationName: 'tobias-weiss-ai-xr',
  projectName: 'docmakerai',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
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
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
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
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Tutorials',
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
              label: 'SOGo Basics',
              to: '/category/sogo',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/tobias-weiss-ai-xr/docmakerai',
            },
            {
              label: 'SOGo',
              href: 'https://www.sogo.nu',
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
