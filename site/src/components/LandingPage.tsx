import React, {type ReactNode} from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import useBaseUrl from '@docusaurus/useBaseUrl';
import PageSEO from '@site/src/components/PageSEO';

/**
 * Copy for one locale of the root landing page (en + de wrappers in
 * src/pages/). Everything the landing page says lives here so the two
 * locale pages stay thin and the copy is greppable in one file.
 */
export type LandingStrings = {
  seoTitle: string;
  seoDescription: string;
  keywords: string[];
  heroAlt: string;
  title: string;
  tagline: string;
  lead: string;
  cardsLabel: string;
  nucleus: {
    badge: string;
    title: string;
    body: string;
    cta: string;
  };
  suite: {
    badge: string;
    title: string;
    body: string;
    cta: string;
    iconAlt: string;
  };
  sogo6: {
    title: string;
    body: string;
    cta: string;
  };
  aboutTitle: string;
  aboutBody: ReactNode;
};

export default function LandingPage({strings}: {strings: LandingStrings}): React.JSX.Element {
  return (
    <Layout title={strings.seoTitle}>
      <PageSEO
        title={strings.seoTitle}
        description={strings.seoDescription}
        keywords={strings.keywords}
      />
      <div className="landing">
        <section className="landing-hero">
          <img
            src={useBaseUrl('/img/teaser.svg')}
            alt={strings.heroAlt}
            className="landing-hero__img"
          />
          <h1>{strings.title}</h1>
          <p className="landing-hero__tagline">{strings.tagline}</p>
          <p className="landing-hero__lead">{strings.lead}</p>
        </section>

        <section className="landing-cards" aria-label={strings.cardsLabel}>
          <Link to="/sogo5/" className="landing-card landing-card--nucleus">
            <span className="landing-card__badge">{strings.nucleus.badge}</span>
            <h2>{strings.nucleus.title}</h2>
            <p>{strings.nucleus.body}</p>
            <span className="landing-card__cta">{strings.nucleus.cta} →</span>
          </Link>
          <Link to="/suite/" className="landing-card landing-card--suite">
            <img
              src={useBaseUrl('/img/openedusuite-logo.svg')}
              alt={strings.suite.iconAlt}
              className="landing-card__logo"
              width={56}
              height={56}
            />
            <span className="landing-card__badge">{strings.suite.badge}</span>
            <h2>{strings.suite.title}</h2>
            <p>{strings.suite.body}</p>
            <span className="landing-card__cta">{strings.suite.cta} →</span>
          </Link>
          <Link to="/sogo6/" className="landing-card landing-card--sogo6">
            <h2>{strings.sogo6.title}</h2>
            <p>{strings.sogo6.body}</p>
            <span className="landing-card__cta">{strings.sogo6.cta} →</span>
          </Link>
        </section>

        <section className="landing-about">
          <h2>{strings.aboutTitle}</h2>
          <p>{strings.aboutBody}</p>
        </section>
      </div>
    </Layout>
  );
}
