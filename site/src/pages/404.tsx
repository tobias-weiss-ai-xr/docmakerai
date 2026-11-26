import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function NotFound(): React.JSX.Element {
  const {i18n} = useDocusaurusContext();
  const de = i18n.currentLocale === 'de';

  return (
    <Layout title={de ? 'Seite nicht gefunden' : 'Page not found'}>
      <main className="landing">
        <section className="landing__hero">
          <p className="landing__eyebrow">404</p>
          <h1>{de ? 'Seite nicht gefunden' : 'Page not found'}</h1>
          <p className="landing__lead">
            {de
              ? 'Diese Adresse existiert nicht. Starten Sie auf der Startseite oder öffnen Sie das SOGo-5-Benutzerhandbuch, den Kern dieses Projekts.'
              : 'This address does not exist. Start from the landing page or open the SOGo 5 user guide, the nucleus of this project.'}
          </p>
          <p className="landing__actions">
            <Link className="button button--primary button--lg" to="/">
              {de ? 'Startseite' : 'Landing page'}
            </Link>
            <Link className="button button--secondary button--lg" to="/sogo5/">
              {de ? 'SOGo-5-Benutzerhandbuch' : 'SOGo 5 user guide'}
            </Link>
          </p>
        </section>
      </main>
    </Layout>
  );
}
