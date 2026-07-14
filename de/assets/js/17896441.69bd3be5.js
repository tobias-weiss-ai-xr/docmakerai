"use strict";(self.webpackChunktmp_docmakerai_site=self.webpackChunktmp_docmakerai_site||[]).push([["106"],{710(e,o,t){t.d(o,{A:()=>u});var r=t(4848),a=t(6540),n=t(9526),s={};let i="docmakerai-votes";async function c(e){let o=await fetch(`https://api.github.com/repos/tobias-weiss-ai-xr/docmakerai/discussions/${e}/reactions?per_page=100`,{headers:{Accept:"application/vnd.github+json"}});if(!o.ok)return{hot:0,slop:0};let t=await o.json();return{hot:t.filter(e=>"+1"===e.content).length,slop:t.filter(e=>"-1"===e.content).length}}function l(){let e,o=(e=window.location.pathname.match(/\/(?:docmakerai\/)?([a-z][\w-]*)/))?e[1]:"",t=s[o],[n,l]=(0,a.useState)(null);if((0,a.useEffect)(()=>{if(!t)return;let e=function(e){try{let o=sessionStorage.getItem(`${i}:${e}`);if(!o)return null;let{data:t,ts:r}=JSON.parse(o);if(Date.now()-r>3e5)return null;return t}catch{return null}}(o);e?l(e):c(t).then(e=>{l(e),sessionStorage.setItem(`${i}:${o}`,JSON.stringify({data:e,ts:Date.now()}))})},[t,o]),!t||null===n)return null;let d=`https://github.com/tobias-weiss-ai-xr/docmakerai/discussions/${t}`,m=n.hot+n.slop;return(0,r.jsxs)("div",{className:"doc-vote-widget",children:[(0,r.jsx)("p",{className:"doc-vote-prompt",children:"Was this page helpful?"}),(0,r.jsxs)("div",{className:"doc-vote-buttons",children:[(0,r.jsxs)("a",{href:`${d}#discussion-comment-1`,target:"_blank",rel:"noopener noreferrer",className:"doc-vote-btn doc-vote-btn--hot",title:"Mark as helpful",children:[(0,r.jsx)("span",{className:"doc-vote-emoji","aria-hidden":"true",children:"\u{1F525}"}),(0,r.jsx)("span",{className:"doc-vote-label",children:"Hot"}),(0,r.jsx)("span",{className:"doc-vote-count",children:n.hot})]}),(0,r.jsxs)("a",{href:`${d}#discussion-comment-1`,target:"_blank",rel:"noopener noreferrer",className:"doc-vote-btn doc-vote-btn--slop",title:"Flag for improvement",children:[(0,r.jsx)("span",{className:"doc-vote-emoji","aria-hidden":"true",children:"\u{1F4A9}"}),(0,r.jsx)("span",{className:"doc-vote-label",children:"Slop"}),(0,r.jsx)("span",{className:"doc-vote-count",children:n.slop})]})]}),m>0&&(0,r.jsxs)("p",{className:"doc-vote-meta",children:[Math.round(n.hot/m*100),"% helpful"]}),(0,r.jsx)("style",{children:`
        .doc-vote-widget {
          margin: 2.5rem 0 1rem;
          padding: 1.25rem 1.5rem;
          border: 1px solid var(--ifm-color-emphasis-300);
          border-radius: 8px;
          background: var(--ifm-background-secondary);
          text-align: center;
        }
        .doc-vote-prompt {
          font-size: 0.95rem;
          font-weight: 600;
          margin: 0 0 0.75rem;
          color: var(--ifm-color-emphasis-800);
        }
        .doc-vote-buttons {
          display: flex;
          gap: 0.75rem;
          justify-content: center;
        }
        .doc-vote-btn {
          display: inline-flex;
          align-items: center;
          gap: 0.4rem;
          padding: 0.5rem 1rem;
          border: 1px solid var(--ifm-color-emphasis-300);
          border-radius: 6px;
          background: var(--ifm-button-background-color);
          color: var(--ifm-font-color-base);
          text-decoration: none;
          font-size: 0.9rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.15s ease;
        }
        .doc-vote-btn:hover {
          border-color: var(--ifm-color-primary);
          background: var(--ifm-color-primary-dark);
          color: #fff;
        }
        .doc-vote-emoji { font-size: 1.1rem; }
        .doc-vote-count {
          font-weight: 700;
          font-variant-numeric: tabular-nums;
        }
        .doc-vote-meta {
          font-size: 0.8rem;
          color: var(--ifm-color-emphasis-600);
          margin: 0.5rem 0 0;
        }
      `})]})}function d(){return(0,r.jsx)(n.A,{children:()=>(0,r.jsx)(l,{})})}var m=t(6437);function u(e){return(0,r.jsx)(m.A,{...e,children:(0,r.jsx)(d,{})})}}}]);