import React, {useState, useEffect} from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import voteTopics from '@site/src/data/vote-topics.json';

interface VoteData {
  hot: number;
  slop: number;
}

const CACHE_KEY = 'docmakerai-votes';
const CACHE_TTL = 5 * 60 * 1000;

function getDiscussionUrl(discussionId: number): string {
  return `https://github.com/tobias-weiss-ai-xr/docmakerai/discussions/${discussionId}`;
}

function getCachedVotes(slug: string): VoteData | null {
  try {
    const raw = sessionStorage.getItem(`${CACHE_KEY}:${slug}`);
    if (!raw) return null;
    const {data, ts} = JSON.parse(raw);
    if (Date.now() - ts > CACHE_TTL) return null;
    return data;
  } catch {
    return null;
  }
}

function setCachedVotes(slug: string, votes: VoteData): void {
  sessionStorage.setItem(
    `${CACHE_KEY}:${slug}`,
    JSON.stringify({data: votes, ts: Date.now()}),
  );
}

async function fetchVotes(discussionId: number): Promise<VoteData> {
  const res = await fetch(
    `https://api.github.com/repos/tobias-weiss-ai-xr/docmakerai/discussions/${discussionId}/reactions?per_page=100`,
    {headers: {Accept: 'application/vnd.github+json'}},
  );
  if (!res.ok) return {hot: 0, slop: 0};
  const reactions: Array<{content: string; user: {login: string}}> =
    await res.json();
  const hot = reactions.filter((r) => r.content === '+1').length;
  const slop = reactions.filter((r) => r.content === '-1').length;
  return {hot, slop};
}

function extractSlug(): string {
  const path = window.location.pathname;
  const match = path.match(/\/(?:docmakerai\/)?([a-z][\w-]*)/);
  return match ? match[1] : '';
}

function DocVoteWidgetInner(): React.JSX.Element | null {
  const slug = extractSlug();
  const discussionId = (voteTopics as Record<string, number>)[slug];

  const [votes, setVotes] = useState<VoteData | null>(null);

  useEffect(() => {
    if (!discussionId) return;
    const cached = getCachedVotes(slug);
    if (cached) {
      setVotes(cached);
      return;
    }
    fetchVotes(discussionId).then((v) => {
      setVotes(v);
      setCachedVotes(slug, v);
    });
  }, [discussionId, slug]);

  if (!discussionId || votes === null) return null;

  const discussionUrl = getDiscussionUrl(discussionId);
  const total = votes.hot + votes.slop;

  return (
    <div className="doc-vote-widget">
      <p className="doc-vote-prompt">
        Was this page helpful?
      </p>
      <div className="doc-vote-buttons">
        <a
          href={`${discussionUrl}#discussion-comment-1`}
          target="_blank"
          rel="noopener noreferrer"
          className="doc-vote-btn doc-vote-btn--hot"
          title="Mark as helpful"
        >
          <span className="doc-vote-emoji" aria-hidden="true">🔥</span>
          <span className="doc-vote-label">Hot</span>
          <span className="doc-vote-count">{votes.hot}</span>
        </a>
        <a
          href={`${discussionUrl}#discussion-comment-1`}
          target="_blank"
          rel="noopener noreferrer"
          className="doc-vote-btn doc-vote-btn--slop"
          title="Flag for improvement"
        >
          <span className="doc-vote-emoji" aria-hidden="true">💩</span>
          <span className="doc-vote-label">Slop</span>
          <span className="doc-vote-count">{votes.slop}</span>
        </a>
      </div>
      {total > 0 && (
        <p className="doc-vote-meta">
          {Math.round((votes.hot / total) * 100)}% helpful
        </p>
      )}
      <style>{`
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
      `}</style>
    </div>
  );
}

export default function DocVoteWidget(): React.JSX.Element {
  return <BrowserOnly>{() => <DocVoteWidgetInner />}</BrowserOnly>;
}
