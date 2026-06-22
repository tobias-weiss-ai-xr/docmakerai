/**
 * DocMaker AI — Remark Plugin for Automatic PageSEO Injection
 *
 * Automatically injects <PageSEO /> component into every documentation page.
 * Uses frontmatter metadata (title, description, keywords, image) to populate
 * per-page SEO meta tags without manual MDX imports.
 *
 * Usage in docusaurus.config.ts:
 *   remarkPlugins: [
 *     require('./plugins/remark-plugin-content-docs').createRemarkPlugin({
 *       PageSEO: require('../src/components/PageSEO').default,
 *     }),
 *   ],
 */

const { visit } = require('unist-util-visit');

/**
 * Escapes special XML/JSX characters in string values.
 */
function escapeJsx(value) {
  if (typeof value !== 'string') return String(value);
  return value
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '\\n');
}

/**
 * Build JSX attribute string from frontmatter data.
 */
function buildPageSEOProps(frontmatter) {
  const props = [];
  const title = frontmatter.title || '';
  const description = frontmatter.description || frontmatter.sidebar_label || '';
  const keywords = frontmatter.keywords || [];
  const image = frontmatter.image || undefined;

  if (title) props.push(`title="${escapeJsx(title)}"`);
  if (description) props.push(`description="${escapeJsx(description)}"`);
  if (keywords.length > 0) {
    props.push(`keywords={[${keywords.map((k) => `"${escapeJsx(k)}"`).join(', ')}]}`);
  }
  if (image) props.push(`image="${escapeJsx(image)}"`);

  return props.join(' ');
}

/**
 * Check if an mdast node is an MDX ESM import statement.
 */
function isMdxImport(node) {
  return node.type === 'mdxjsEsm' && /^import\s/.test(String(node.value || ''));
}

/**
 * Check if an mdast node is an MDX JSX element referencing PageSEO.
 */
function isPageSEO(node) {
  return (
    node.type === 'mdxjsEsm' &&
    /<PageSEO\s/.test(String(node.value || ''))
  );
}

/**
 * Creates the remark plugin instance.
 *
 * @param {object} options
 * @param {React.ComponentType} options.PageSEO - The PageSEO component (injected by config)
 * @returns {function} Remark plugin function
 */
function createRemarkPlugin({ PageSEO } = {}) {
  return function remarkInjectPageSEO() {
    return function transformer(tree, file) {
      const alreadyHasPageSEO = tree.children && tree.children.some(isPageSEO);
      if (alreadyHasPageSEO) return;

      const frontmatter = file.data?.frontmatter || {};
      const title = frontmatter.title || '';
      if (!title) return;

      const propsStr = buildPageSEOProps(frontmatter);
      if (!propsStr) return;

      const hasPageSEOImport = tree.children && tree.children.some(
        (node) => isMdxImport(node) && String(node.value || '').includes('PageSEO')
      );

      const insertNodes = [];

      if (!hasPageSEOImport) {
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
  };
}

module.exports = { createRemarkPlugin };
