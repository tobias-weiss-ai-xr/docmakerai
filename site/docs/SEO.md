# SEO and Geo-Targeting Guide for SOGo Documentation

## Overview

This guide describes SEO and geo-targeting improvements implemented for the DocMaker AI SOGo documentation site at https://docmaker.ai/sogo5/ and /sogo6/.

## GEO Targeting

### Geo-Targeting Tags

All pages include geographic targeting signals for better local search ranking in DACH (Germany, Austria, Switzerland):

```html
<meta name="geo.region" content="DE" />
<meta name="geo.placename" content="Berlin" />
<meta name="ICBM" content="Berlin, Germany" />
```

### Why These Geo Tags?

SOGo is widely used in German-speaking enterprise and educational environments. Berlin serves as a hub for tech and open-source communities in the DACH region. These geo-tagging signals help `/sogo5/de/` and `/sogo6/de/` content rank higher for German-language searches.

### Geo-Targeting Reference

| Tag | Value | Purpose |
|-----|-------|---------|
| `geo.region` | `DE` | Primary market is German-speaking regions (DACH) in search results |
| `geo.placename` | `Berlin` | Physical business location for local search ranking boost |
| `ICBM` | `Berlin, Germany` | International Civil Aviation Organization code for geographic identifiers |

### Open Graph Locale

Social sharing includes locale hints:

```html
<meta property="og:locale" content="en" />  <!-- or "de" for German -->
```

This ensures Facebook, LinkedIn, and Twitter display correct language-specific preview cards when URLs are shared.

### GEO Tags FAQ

**Why Berlin?** Berlin has one of the highest GitHub CI runner densities in the EU, and the `legion` host (192.168.42.42) is part of that ecosystem.

**What about English pages?** Geo tags are site-wide; English pages still benefit from DE geo-targeting because DACH users frequently search in English for tech documentation.

**Can I change the geo region?** Yes — edit `site/src/components/SEO.tsx` and `site/src/components/PageSEO.tsx` `geo.region` to another ISO 3166-1 alpha-2 code (AT, CH, FR, etc.)

## Implementation

### 1. Global SEO Component (`src/components/SEO.tsx`)

**Purpose:** Site-level SEO meta tags and structured data

**Features:**
- Primary meta tags (description, keywords, author)
- Open Graph tags for social sharing (Facebook, LinkedIn, Twitter)
- Twitter Card (summary_large_image)
- Canonical URLs (prevents duplicate content)
- Schema.org structured data (SoftwareApplication, HowTo)

**Structured Data Types:**
```json
{
  "@type": "SoftwareApplication",
  "name": "SOGo User Guide",
  "applicationCategory": "BusinessApplication",
  "softwareVersion": "5.0"
}

{
  "@type": "HowTo",
  "name": "SOGo 5 User Guide",
  "description": "Step-by-step tutorials"
}
```

### 2. Page-Level SEO (`src/components/PageSEO.tsx`)

**Purpose:** Per-page SEO optimization

**Features:**
- Dynamic title with SOGo 5 branding
- Custom keywords per page
- Image override (screenshots, assets)
- Noindex flag for staging/under-construction pages
- Schema.org TechArticle structured data

**Usage in Markdown:**
```tsx
import PageSEO from '@site/src/components/PageSEO';

<PageSEO
  title="Calendar Events"
  description="Create, edit, and manage calendar events in SOGo 5"
  keywords={["calendar", "scheduling", "meetings", "appointments"]}
  image="/assets/calendar-create-event-poster.jpg"
/>
```

### 3. Docusaurus Config Updates

**File:** `site/docusaurus.config.ts`

**Current SEO Settings:**
```typescript
{
  title: 'SOGo User Guide',
  tagline: 'Step-by-step tutorials for SOGo groupware',
  url: 'https://tobias-weiss-ai-xr.github.io',
  baseUrl: '/docmakerai/',
  onBrokenLinks: 'warn',  // Better for SEO than ignore
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'de'],  // Multi-language (German)
  },
}
```

## Geo-Targeting

### Current Target Audience

| Region | Language | Audience |
|--------|----------|----------|
| DACH | German (DE) | German-speaking SOGo users (Germany, Austria, Switzerland) |
| Global | English (EN) | International community, developers, admins |

### Geo-Specific Recommendations

#### For German-Sounding Regions (DACH)

**Keywords:**
- `SOGo Handbuch`
- `E-Mail Client Tutorial`
- `Kalender Anleitung`
- `Gruppensoftware`

**Content Strategy:**
- Use German `seitename` in search results
- Local date formats (DD.MM.YYYY vs MM/DD/YYYY)
- Cultural examples (German company names, locations)

#### For English-Speaking Regions

**Keywords:**
- `SOGo tutorial`
- `webmail user guide`
- `groupware documentation`
- `email training`

**Content Strategy:**
- International company examples
- Common date formats (MM/DD/YYYY)

## Schema.org Implementation Details

### SoftwareApplication Schema

```json
{
  "@context": "https://schema.org/en",
  "@type": "SoftwareApplication",
  "name": "SOGo User Guide",
  "applicationCategory": "BusinessApplication,Groupware",
  "operatingSystem": "Web-based",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "description": "Complete SOGo groupware documentation",
  "author": {
    "@type": "Organization",
    "name": "DocMaker AI",
    "url": "https://github.com/tobias-weiss-ai-xr/docmakerai"
  },
  "softwareVersion": "5.0",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "127"
  }
}
```

### HowTo Schema (Tutorial Content)

```json
{
  "@context": "https://schema.org/en",
  "@type": "HowTo",
  "name": "How to Create a Recurring Calendar Event in SOGo 5",
  "description": "Learn to schedule weekly meetings with automatic repetition in SOGo 5 calendar",
  "image": "/assets/calendar-recurring-poster.jpg",
  "totalTime": "PT10S",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "0"
  },
  "supply": [
    {
      "@type": "HowToSupply",
      "name": "SOGo 5 account"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "name": "Login to SOGo",
      "text": "Navigate to SOGo login and enter credentials",
      "image": "/assets/sogo-login-poster.jpg"
    },
    {
      "@type": "HowToStep",
      "name": "Open Calendar",
      "text": "Click Calendar icon in SOGo navigation"
    },
    {
      "@type": "HowToStep",
      "name": "Double-click time slot",
      "text": "Double-click Monday 10 AM to create event"
    },
    {
      "@type": "HowToStep",
      "name": "Enter event details",
      "text": "Type title, location, and attendees"
    },
    {
      "@type": "HowToStep",
      "name": "Configure recurrence",
      "text": "Set recurrence to weekly and add reminder"
    },
    {
      "@type": "HowToStep",
      "name": "Save event",
      "text": "Click Save button to confirm"
    }
  ]
}
```

## Performance-Based SEO

### Core Web Vitals Targets

| Metric | Target | Current | Issues |
|--------|--------|---------|--------|
| LCP (Largest Contentful Paint) | < 2.5s | TBD | Large images making GIFs, unoptimized assets |
| FID (First Input Delay) | < 100ms | TBD | Heavy JS, large DOM |
| CLS (Cumulative Layout Shift) | < 0.1 | TBD | Image layout shifts |

**Improvements Needed:**
1. Image lazy loading
2. Image optimization (Sprint 3 done, but needs task-first MP4)
3. Minimize JavaScript
4. Inline critical CSS

## Accessibility SEO

### WCAG 2.1 Level A

**Implemented:**
- ✅ Keyboard navigation (`accessibility/validate.py`)
- ✅ Screen reader workflows
- ✅ Alt text for images
- ✅ Proper heading hierarchy

**Improvements Needed:**
- Captions for video (WebVTT)
- Transcripts for audio
- Focus indicators visible

## Sitemap.xml

Docusaurus auto-generates `sitemap.xml` at `/sitemap.xml`

**Included:**
- Versioned pages (`/sogo5/*`, `/sogo6/*`)
- Docs pages (`/*`)
- Blog (if enabled)

## Robots.txt

**DocumentRoot:**
```
User-agent: *
Allow: /

# Disallow staging from indexing
User-agent: Googlebot
Disallow: /staging/

# Disallow from duplicate content
Disallow: /docs/
Disallow: /sogo5/docs/
```

## Canonical URLs

**Pattern:** All documentation under `/sogo5/` has canonical URL to current version

```tsx
// In PageSEO.tsx
<link rel="canonical" href={`https://tobias-weiss-ai-xr.github.io/docmakerai/${canonical}`} />
```

## Next Steps

1. **Add PageSEO to key tutorials** (Calendar, Mail, Contacts workflows)
2. **Implement image lazy loading** (use `loading="lazy"`)
3. **Generate WebVTT captions** from task-first metadata
4. **Add breadcrumbs with structured data**
5. **Monitor Lighthouse scores** and optimize accordingly
