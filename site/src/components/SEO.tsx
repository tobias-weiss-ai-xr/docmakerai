import Head from '@docusaurus/Head';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import React from 'react';

export default function SEO() {
  const { i18n, siteConfig } = useDocusaurusContext();

  return (
    <Head>
      <meta name="description" content="Complete SOGo user guide with step-by-step tutorials for email, calendar, contacts, and collaboration features." />
      <meta name="keywords" content="SOGo, webmail, groupware, email client, calendar, tutorial, user guide, documentation, open source" />
      <meta name="author" content="DocMaker AI" />

      <meta property="og:type" content="website" />
      <meta property="og:title" content="SOGo User Guide - Complete Tutorials for Email, Calendar & Collaboration" />
      <meta property="og:description" content="Master SOGo groupware with our comprehensive tutorials covering email, calendar, contacts, and collaboration workflows." />
      <meta property="og:image" content={`${siteConfig.url}${siteConfig.baseUrl}img/docusaurus-social-card.jpg`} />
      <meta property="og:url" content={`${siteConfig.url}${siteConfig.baseUrl}`} />
      <meta property="og:site_name" content={siteConfig.title} />
      <meta property="og:locale" content={i18n.currentLocale} />

      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content="SOGo User Guide" />
      <meta name="twitter:description" content="Learn SOGo through step-by-step tutorials. Email, calendar, contacts, and collaboration documentation." />
      <meta name="twitter:image" content={`${siteConfig.url}${siteConfig.baseUrl}img/docusaurus-social-card.jpg`} />

      <link rel="canonical" href={`${siteConfig.url}${siteConfig.baseUrl}`} />

      <script type="application/ld+json">
        {JSON.stringify({
          "@context": "https://schema.org",
          "@type": "SoftwareApplication",
          "name": siteConfig.title,
          "applicationCategory": "BusinessApplication",
          "operatingSystem": "Web",
          "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
          },
          "description": "Complete SOGo groupware documentation with step-by-step tutorials for email, calendar, contacts, and collaboration.",
          "author": {
            "@type": "Organization",
            "name": "DocMaker AI",
            "url": "https://github.com/tobias-weiss-ai-xr/docmakerai"
          },
          "softwareVersion": "5.0"
        })}
      </script>

      <script type="application/ld+json">
        {JSON.stringify({
          "@context": "https://schema.org",
          "@type": "HowTo",
          "name": "SOGo 5 User Guide",
          "description": "Learn how to use SOGo 5 webmail, calendar, contacts, and collaboration features through step-by-step tutorials.",
          "image": `${siteConfig.url}${siteConfig.baseUrl}img/logo.svg`,
          "supply": [
            {
              "@type": "HowToSupply",
              "name": "Web browser",
              "image": "https://img.icons8.com/color/96/000000/chrome.png"
            }
          ]
        })}
      </script>
    </Head>
  );
}
