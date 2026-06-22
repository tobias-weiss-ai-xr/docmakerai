import React from 'react';
import Layout from '@theme-original/Layout';
import SEO from '@site/src/components/SEO';

export default function Layout({children, ...props}: any): JSX.Element {
  return (
    <>
      <SEO />
      <Layout {...props}>{children}</Layout>
    </>
  );
}
