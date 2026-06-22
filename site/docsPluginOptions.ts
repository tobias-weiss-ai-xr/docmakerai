import type {Config} from '@docusaurus/types';

export default {
  docs: {
    path: 'docs',
    routeBasePath: '/',
    editUrl: false,  // Disable "Edit this page" link
    sidebarPath: './sidebars.ts',
    breadcrumbs: true,
    toc: {
      minHeadingLevel: 2,
      maxHeadingLevel: 3,
    },
  },
} satisfies Config;
