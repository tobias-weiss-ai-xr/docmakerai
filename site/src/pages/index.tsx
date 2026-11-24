import React from 'react';
import LandingPage from '@site/src/components/LandingPage';
import type {LandingStrings} from '@site/src/components/LandingPage';

/**
 * Root landing page (en). Introduces the project — the SOGo User Guide built
 * by DocMaker AI — and points visitors at its two doors: SOGo 5 (the nucleus
 * of this project) and the openEduSuite it belongs to.
 */
const en: LandingStrings = {
  seoTitle: 'DocMaker AI — Step-by-step SOGo tutorials',
  seoDescription:
    'DocMaker AI builds the SOGo User Guide from real screen recordings: step-by-step tutorials for SOGo 5 and SOGo 6, plus the openEduSuite of open-source apps behind one login.',
  keywords: [
    'DocMaker AI',
    'SOGo User Guide',
    'SOGo 5',
    'SOGo 6',
    'openEduSuite',
    'groupware tutorials',
  ],
  heroAlt: 'DocMaker AI — Automated screenshot capture pipeline',
  title: 'Step-by-step guides, captured from the real UI',
  tagline: 'The SOGo User Guide — built by DocMaker AI',
  lead: 'DocMaker AI turns real screen recordings into annotated, step-by-step tutorials. This project documents SOGo Groupware in every supported version, and the wider openEduSuite that SOGo belongs to.',
  cardsLabel: 'Where to start',
  nucleus: {
    badge: 'The nucleus of this project',
    title: 'SOGo 5 User Guide',
    body: 'Complete tutorials for email, calendar, contacts, preferences and advanced groupware features — the core everything else in this project documents.',
    cta: 'Open the SOGo 5 guide',
  },
  suite: {
    badge: 'The bigger picture',
    title: 'openEduSuite',
    body: 'The open-source digital workplace for higher education: SOGo, Nextcloud, XWiki, OpenProject, BigBlueButton and more behind one single sign-on.',
    cta: 'Explore the suite',
  },
  sogo6: {
    title: 'SOGo 6 Tutorials',
    body: 'The newest SOGo generation — the same guides, adapted to the SOGo 6 interface.',
    cta: 'Open the SOGo 6 guide',
  },
  aboutTitle: 'How this documentation is made',
  aboutBody: (
    <>
      Every tutorial starts as a real Playwright recording of the SOGo UI.
      DocMaker AI annotates each step, checks the captures for quality, and
      assembles them into animated illustrations — so you always see exactly
      what to click, type and expect. Want to know more about the pipeline, or
      report an issue?{' '}
      <a href="https://github.com/tobias-weiss-ai-xr/docmakerai">
        Head over to the project on GitHub
      </a>
      {' '}or visit{' '}
      <a href="https://www.sogo.nu">sogo.nu</a>.
    </>
  ),
};

export default function Home(): React.JSX.Element {
  return <LandingPage strings={en} />;
}
