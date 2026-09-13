import React, {type ReactNode} from 'react';
import Logo from '@theme/Logo';
import {useLocation} from '@docusaurus/router';

/**
 * Brand follows the version being read: pages under /sogo6/ link home to
 * /sogo6/, /sogo5/ pages to /sogo5/. Everything else keeps the configured
 * default (/sogo5/). Passed as `to`, which Logo spreads over its computed
 * config href (props spread wins), so no upstream copy is needed.
 */
export default function NavbarLogo(): ReactNode {
  const {pathname} = useLocation();
  const match = pathname.match(/\/sogo([56])\//);
  const versionHome = match ? `/sogo${match[1]}/` : '/sogo5/';
  return (
    <Logo
      className="navbar__brand"
      imageClassName="navbar__logo"
      titleClassName="navbar__title text--truncate"
      {...({to: versionHome} as any)}
    />
  );
}
