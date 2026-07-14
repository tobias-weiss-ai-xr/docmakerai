import React from 'react';
import DocVoteWidget from '@site/src/components/DocVoteWidget';
import OriginalDocItemLayout from '@theme-original/DocItem/Layout';

export default function DocItemLayout(props: any): React.JSX.Element {
  return (
    <OriginalDocItemLayout {...props}>
      <DocVoteWidget />
    </OriginalDocItemLayout>
  );
}
