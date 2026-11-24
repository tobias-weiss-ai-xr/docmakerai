import React from 'react';
import LandingPage from '@site/src/components/LandingPage';
import type {LandingStrings} from '@site/src/components/LandingPage';

/**
 * Root landing page (de). Docusaurus picks this up for the de locale (the
 * localized content path shadows src/pages/index.tsx), so /de/ renders it.
 */
const de: LandingStrings = {
  seoTitle: 'DocMaker AI — Schritt-für-Schritt-SOGo-Anleitungen',
  seoDescription:
    'DocMaker AI erstellt das SOGo Benutzerhandbuch aus echten Bildschirmaufnahmen: Schritt-für-Schritt-Anleitungen für SOGo 5 und SOGo 6 sowie die openEduSuite — offene Anwendungen hinter einem Login.',
  keywords: [
    'DocMaker AI',
    'SOGo Benutzerhandbuch',
    'SOGo 5',
    'SOGo 6',
    'openEduSuite',
    'Groupware-Anleitungen',
  ],
  heroAlt: 'DocMaker AI — Automatisierte Screenshot-Pipeline',
  title: 'Schritt-für-Schritt-Anleitungen, direkt aus der echten Oberfläche',
  tagline: 'Das SOGo Benutzerhandbuch — erstellt von DocMaker AI',
  lead: 'DocMaker AI macht aus echten Bildschirmaufnahmen kommentierte Schritt-für-Schritt-Anleitungen. Dieses Projekt dokumentiert die SOGo Groupware in allen unterstützten Versionen sowie die openEduSuite, zu der SOGo gehört.',
  cardsLabel: 'Wo Sie starten können',
  nucleus: {
    badge: 'Der Kern dieses Projekts',
    title: 'SOGo 5 Benutzerhandbuch',
    body: 'Vollständige Anleitungen für E-Mail, Kalender, Kontakte, Einstellungen und erweiterte Groupware-Funktionen — der Kern, um den sich alles andere in diesem Projekt dreht.',
    cta: 'Zum SOGo-5-Handbuch',
  },
  suite: {
    badge: 'Der größere Zusammenhang',
    title: 'openEduSuite',
    body: 'Der Open-Source-Digital-Arbeitsplatz für Hochschulen: SOGo, Nextcloud, XWiki, OpenProject, BigBlueButton und mehr hinter einem einzigen Single Sign-On.',
    cta: 'Zur openEduSuite',
  },
  sogo6: {
    title: 'SOGo-6-Anleitungen',
    body: 'Die neueste SOGo-Generation — dieselben Anleitungen, angepasst an die Oberfläche von SOGo 6.',
    cta: 'Zu den SOGo-6-Anleitungen',
  },
  aboutTitle: 'Wie diese Dokumentation entsteht',
  aboutBody: (
    <>
      Jede Anleitung beginnt als echte Playwright-Aufzeichnung der
      SOGo-Oberfläche. DocMaker AI kommentiert jeden Schritt, prüft die
      Aufnahmen auf Qualität und setzt sie zu animierten Illustrationen
      zusammen — so sehen Sie immer genau, was Sie klicken, eingeben und
      erwarten können. Mehr über die Pipeline oder einen Fehler melden?{' '}
      <a href="https://github.com/tobias-weiss-ai-xr/docmakerai">
        Besuchen Sie das Projekt auf GitHub
      </a>{' '}
      oder{' '}
      <a href="https://www.sogo.nu">sogo.nu</a>.
    </>
  ),
};

export default function Home(): React.JSX.Element {
  return <LandingPage strings={de} />;
}
