import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';

export default function NotFound(): React.JSX.Element {
  return (
    <Layout title="Page not found">
      <main className="landing">
        <section className="landing__hero">
          <p className="landing__eyebrow">404</p>
          <h1>Page not found</h1>
          <p className="landing__lead">
            This address does not exist. Start from the landing page or open the
            SOGo 5 user guide, the nucleus of this project.
          </p>
          <p className="landing__actions">
            <Link className="button button--primary button--lg" to="/">
              Landing page
            </Link>
            <Link className="button button--secondary button--lg" to="/sogo5/">
              SOGo 5 user guide
            </Link>
          </p>
          <p className="landing__note">
            German: <Link to="/de/">Startseite</Link> ·{' '}
            <Link to="/de/sogo5/">SOGo-5-Benutzerhandbuch</Link>
          </p>
        </section>
      </main>
    </Layout>
  );
}
