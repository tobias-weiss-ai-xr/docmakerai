import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'index',
    {
      type: 'category',
      label: 'Erste Schritte',
      items: ['sogo-login', 'sogo-logout'],
    },
    {
      type: 'category',
      label: 'Grundfunktionen',
      items: ['sogo-preferences', 'sogo-password-change', 'sogo-vacation'],
    },
    {
      type: 'category',
      label: 'Kalender',
      items: [
        'sogo-calendar-create-event',
        'sogo-calendar-recurring',
        'sogo-calendar-views',
        'sogo-calendar-edit-delete',
        'sogo-calendar-ical',
        'sogo-calendar-share',
        'sogo-calendar-subscribe',
        'sogo-calendar-freebusy',
      ],
    },
    {
      type: 'category',
      label: 'E-Mail',
      items: [
        'sogo-mail-read',
        'sogo-mail-compose',
        'sogo-mail-signatures',
        'sogo-mail-folder-management',
        'sogo-mail-reply-forward-delete',
        'sogo-mail-folders-filters',
      ],
    },
    {
      type: 'category',
      label: 'Kontakte',
      items: [
        'sogo-contacts-add',
        'sogo-contacts-edit-delete',
        'sogo-contacts-import-export',
      ],
    },
    {
      type: 'category',
      label: 'Werkzeuge',
      items: ['sogo-global-search'],
    },
    {
      type: 'category',
      label: 'Fortgeschritten',
      items: [
        'sogo-delegation',
        'sogo-tasks',
        'sogo-resource-booking',
      ],
    },
  ],
};

export default sidebars;
