/**
 * DocMaker AI — Remark Plugin for Automatic PageSEO Injection
 *
 * Injects <PageSEO /> component with frontmatter-derived props into
 * every documentation page. The component import is resolved by Webpack
 * at bundle time — no config-time require needed.
 *
 * Usage in docusaurus.config.ts:
 *   remarkPlugins: [require('./plugins/remark-plugin-content-docs')],
 */

function buildPageSEOProps(frontmatter) {
  const props = [];
  const title = frontmatter.title || '';
  if (!title) return '';

  const description = frontmatter.description || frontmatter.sidebar_label || '';
  const keywords = frontmatter.keywords || [];
  const image = frontmatter.image || undefined;

  props.push(`title="${title.replace(/"/g, '&quot;')}"`);
  if (description) props.push(`description="${description.replace(/"/g, '&quot;')}"`);
  if (keywords.length > 0) {
    props.push(`keywords={[${keywords.map(k => `"${k.replace(/"/g, '&quot;')}"`).join(', ')}]}`);
  }
  if (image) props.push(`image="${image.replace(/"/g, '&quot;')}"`);

  return props.join(' ');
}

function isMdxImport(node) {
  return node.type === 'mdxjsEsm' && /^import\s/.test(String(node.value || ''));
}

function isPageSEO(node) {
  return node.type === 'mdxjsEsm' && /<PageSEO\s/.test(String(node.value || ''));
}

function remarkInjectPageSEO() {
  return function transformer(tree, file) {
    if (tree.children && tree.children.some(isPageSEO)) return;

    const frontmatter = file.data?.frontmatter || {};
    const propsStr = buildPageSEOProps(frontmatter);
    if (!propsStr) return;

    const hasImport = tree.children && tree.children.some(
      (node) => isMdxImport(node) && String(node.value || '').includes('PageSEO')
    );

    const insertNodes = [];
    if (!hasImport) {
      insertNodes.push({
        type: 'mdxjsEsm',
        value: "import PageSEO from '@site/src/components/PageSEO'",
        data: { estree: null },
      });
    }
    insertNodes.push({
      type: 'mdxjsEsm',
      value: `<PageSEO ${propsStr} />`,
      data: { estree: null },
    });

    if (tree.children && tree.children.length > 0) {
      tree.children.unshift(...insertNodes);
    } else if (tree.children) {
      tree.children = insertNodes;
    }
  };
}

module.exports = remarkInjectPageSEO;
