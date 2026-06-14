import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['sogo-login'],
    },
    {
      type: 'category',
      label: 'Calendar',
      items: [
        'sogo-calendar-create-event',
        'sogo-calendar-recurring',
        'sogo-calendar-share',
        'sogo-calendar-subscribe',
        'sogo-calendar-freebusy',
      ],
    },
    {
      type: 'category',
      label: 'Mail',
      items: [
        'sogo-mail-compose',
        'sogo-mail-signatures',
        'sogo-mail-folders-filters',
      ],
    },
    {
      type: 'category',
      label: 'Additional Features',
      items: [
        'sogo-contacts-add',
        'sogo-vacation',
      ],
    },
  ],
};

export default sidebars;
