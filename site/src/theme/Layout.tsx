import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import SEO from '@site/src/components/SEO';

export default function Layout({children, ...props}: any): React.JSX.Element {
  return (
    <>
      <SEO />
      <OriginalLayout {...props}>{children}</OriginalLayout>
    </>
  );
}
