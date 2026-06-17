import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'SOGo 5 User Guide',
  tagline: 'Step-by-step tutorials for SOGo 5 groupware',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: process.env.SITE_URL || 'https://tobias-weiss-ai-xr.github.io',
  baseUrl: process.env.BASE_URL || '/docmakerai/',

  organizationName: 'tobias-weiss-ai-xr',
  projectName: 'docmakerai',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

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
      title: 'SOGo 5 User Guide',
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
              to: '/',
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
