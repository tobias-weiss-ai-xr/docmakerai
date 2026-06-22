import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Head from '@docusaurus/Head';
import React from 'react';

type PageSEOProps = {
  title?: string;
  description?: string;
  keywords?: string[];
  image?: string;
  locale?: string;
  canonical?: string;
  noindex?: boolean;
};

export default function PageSEO({
  title,
  description,
  keywords = [],
  image,
  locale,
  canonical,
  noindex = false,
}: PageSEOProps) {
  const { i18n, siteConfig } = useDocusaurusContext();

  const finalTitle = title
    ? `${title} | SOGo ${i18n.currentLocale === 'de' ? 'Nutzerhandbuch' : 'User Guide'}`
    : siteConfig.title;

  const finalDescription = description ?? siteConfig.tagline;
  const finalImage = image ?? `${siteConfig.url}${siteConfig.baseUrl}img/docusaurus-social-card.jpg`;
  const finalLocale = locale ?? i18n.currentLocale;

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": finalTitle,
    "description": finalDescription,
    "image": finalImage,
    "datePublished": "2024-01-01",
    "dateModified": new Date().toISOString().split('T')[0],
    "author": {
      "@type": "Organization",
      "name": "DocMaker AI"
    }
  };

  return (
    <Head>
      <title>{finalTitle}</title>
      <meta name="description" content={finalDescription} />
      <meta name="keywords" content={[...keywords, "SOGo", "webmail", "groupware", "email tutorial"].join(', ')} />
      <meta name="author" content="DocMaker AI" />

      {noindex && <meta name="robots" content="noindex, nofollow" />}

      <meta property="og:type" content="article" />
      <meta property="og:title" content={finalTitle} />
      <meta property="og:description" content={finalDescription} />
      <meta property="og:image" content={finalImage} />
      <meta property="og:locale" content={finalLocale} />

      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={finalTitle} />
      <meta name="twitter:description" content={finalDescription} />
      <meta name="twitter:image" content={finalImage} />

      {canonical && <link rel="canonical" href={canonical} />}

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }} />
    </Head>
  );
}
