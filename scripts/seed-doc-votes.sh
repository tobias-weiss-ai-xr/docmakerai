#!/usr/bin/env bash
# seed-doc-votes.sh — Create GitHub Discussions for doc voting
#
# Creates one GitHub Discussion per doc page in the "Doc Feedback" category.
# Populates site/src/data/vote-topics.json with slug → discussion_id mapping.
#
# Prerequisites:
#   - gh CLI installed and authenticated
#   - GitHub repo Discussions enabled
#
# Usage:
#   ./scripts/seed-doc-votes.sh

set -euo pipefail

REPO="tobias-weiss-ai-xr/docmakerai"
CATEGORY_NAME="Doc Feedback"
OUTPUT_FILE="site/src/data/vote-topics.json"

echo "Ensuring 'Doc Feedback' discussion category exists..."
gh api graphql -f query='
query {
  repository(owner: "tobias-weiss-ai-xr", name: "docmakerai") {
    discussionCategories(first: 50) {
      nodes {
        id
        name
        slug
      }
    }
  }
}' > /dev/null

CATEGORY_ID=$(gh api graphql -f query='
query {
  repository(owner: "tobias-weiss-ai-xr", name: "docmakerai") {
    discussionCategories(first: 50) {
      nodes {
        id
        name
        slug
      }
    }
  }
}' --jq ".data.repository.discussionCategories.nodes[] | select(.name == \"$CATEGORY_NAME\") | .id")

if [ -z "$CATEGORY_ID" ] || [ "$CATEGORY_ID" = "null" ]; then
  echo "Creating '$CATEGORY_NAME' discussion category..."
  CATEGORY_ID=$(gh api graphql -f query='
  mutation {
    createDiscussionCategory(
      input: {
        repositoryId: "$(gh api graphql -f query='{ repository(owner:"tobias-weiss-ai-xr",name:"docmakerai") { id } }' --jq '.data.repository.id')",
        name: "'"$CATEGORY_NAME"'",
        description: "Community voting on documentation quality",
        emoji: "🗳️"
      }
    ) { category { id } }
  }' --jq '.data.createDiscussionCategory.category.id')
fi

echo "Category ID: $CATEGORY_ID"

echo "Seeding discussions for sogo-*.md docs..."
SLUGS=$(ls site/docs/sogo-*.md | xargs -n1 basename | sed 's/\.md$//')

echo "{" > "$OUTPUT_FILE"

FIRST=true
for slug in $SLUGS; do
  title="[$slug] Rate this documentation"
  body="## Doc Feedback: $slug

React to this discussion to rate the **$slug** documentation page.

- 👍 **+1 (Hot)** = This page is helpful and accurate
- 👎 **-1 (Slop)** = This page needs improvement

Discussion: https://tobias-weiss-ai-xr.github.io/docmakerai/$slug/"

  discussion_id=$(gh api graphql -f query='
  mutation {
    createDiscussion(
      input: {
        repositoryId: "$(gh api graphql -f query='{ repository(owner:"tobias-weiss-ai-xr",name:"docmakerai") { id } }' --jq '.data.repository.id')",
        categoryId: "'"$CATEGORY_ID"'",
        title: "'"$title"'",
        body: "'$(echo "$body" | jq -Rs '.')'"
      }
    ) { discussion { number } }
  }' --jq '.data.createDiscussion.discussion.number')

  echo "  Created: $slug → #$discussion_id"

  if [ "$FIRST" = true ]; then
    FIRST=false
  else
    echo "," >> "$OUTPUT_FILE"
  fi
  echo "  \"$slug\": $discussion_id" >> "$OUTPUT_FILE"

  sleep 1
done

echo "}" >> "$OUTPUT_FILE"

echo ""
echo "Done! Vote topics written to $OUTPUT_FILE"
echo "Run 'npm run build' to pick up the changes."
