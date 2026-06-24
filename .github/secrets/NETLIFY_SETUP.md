# Required GitHub Secrets for Preview Deployments

## Overview

The `Preview Deploy` workflow requires two Netlify secrets to create preview URLs for pull requests.

## Required Secrets

### 1. NETLIFY_AUTH_TOKEN

Personal access token from Netlify for authentication.

**How to create:**

1. Go to [Netlify User Settings](https://app.netlify.com/user/applications#personal-access-tokens)
2. Click "New access token"
3. Description: "GitHub Actions Preview Deployments"
4. Expiration: "No expiration" or set date
5. Click "Generate token"
6. Copy the token (starts with `nfp_`)

**Add to GitHub:**

1. Go to repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `NETLIFY_AUTH_TOKEN`
4. Value: paste the Netlify token (e.g., `nfp_xxxxxxxxxxxxxxxxxx`)

### 2. NETLIFY_SITE_ID

Unique identifier for your Netlify site.

**How to find:**

1. Go to [Netlify Dashboard](https://app.netlify.com)
2. Select your site from the list
3. Go to "Site settings" → "General"
4. Find "Site information" section
5. Copy "Site ID" (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

**Add to GitHub:**

1. Go to repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `NETLIFY_SITE_ID`
4. Value: paste the site ID (e.g., `1234abcd-5678-90ef-ghij-klmnopqrstuv`)

## Configuration

### Automatic Preview Deployments

With secrets configured, preview deployments automatically trigger on:

- Pull requests opened to `main` branch
- Pull requests synced (new commits pushed)
- Pull requests reopened

### Manual Preview Deployments

Trigger manually anytime:

1. Go to repository → Actions
2. Select "Preview Deploy" workflow
3. Click "Run workflow"
4. Select branch and confirm

## Creating a Netlify Site (If Needed)

### Option A: Import Existing GitHub Pages Site

1. Go to [Netlify](https://app.netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Select "GitHub"
4. Choose `tobias-weiss-ai-xr/docmakerai` repository
5. Configure build settings:
   - Build command: `cd site && npm run build`
   - Publish directory: `site/build`
6. Click "Deploy site"

### Option B: Create New Netlify Site with Different Domain

1. Go to [Netlify](https://app.netlify.com)
2. Click "Add new site" → "Manual deploy"
3. Choose upload folder or manual configuration
4. Configure custom domain (if desired)
5. Get site ID from settings

## Testing Preview Deployments

### Manual Test

Test without creating a real pull request:

1. Make any change to a file
2. Commit changes
3. Create a test branch: `git checkout -b test-preview`
4. Push branch: `git push origin test-preview`
5. Create PR on GitHub
6. Preview URL will be posted as comment on PR

### Workflow Dispatch Test

Test preview workflow manually:

1. Go to Actions → Preview Deploy
2. Click "Run workflow"
3. Select `main` branch
4. Confirm

## Troubleshooting

### Preview Deploy Fails

**Error:** `NETLIFY_AUTH_TOKEN not found`

**Solution:** Add the secret to GitHub repository settings

**Error:** `NETLIFY_SITE_ID not found`

**Solution:** Add the site ID secret to GitHub repository settings

**Error:** `401 Unauthorized`

**Solution:** Verify Netlify token is valid and has proper permissions

**Error:** `Site not found`

**Solution:** Verify Netlify site ID is correct and site exists

### Preview URL Not Posted

**Error:** No comment posted on PR

**Solution:**
1. Check GitHub Actions logs for error
2. Verify `gh` CLI permissions
3. Check repository settings allow issues/comments

### Slow Preview Deployments

**Problem:** Preview deployments take too long

**Solutions:**
1. Use English-only build (current default)
2. Increase Netlify cache
3. Deploy only changed pages (incremental deployment)

## Security Best Practices

### Token Management

- ✅ Use dedicated Netlify token (not personal account token)
- ✅ Set token expiration (use rotation)
- ✅ Limit token permissions (minimal access)
- ✅ Monitor token usage
- ❌ Never commit secrets to repository
- ❌ Never share tokens publicly

### Access Control

- Repository administrators only should manage secrets
- Use different tokens for different environments
- Rotate tokens regularly
- Monitor GitHub Actions usage logs

## Cost Considerations

**Netlify Pricing:**
- Free tier: 100GB bandwidth, 300 build minutes/month
- Pro tier: 400GB bandwidth, 1000 build minutes/month
- Enterprise: Unlimited

**Preview Usage:**
- Each preview deployment counts as build time
- Preview sites count toward bandwidth
- Consider build time vs deployment speed trade-offs

## Alternatives to Netlify

If Netlify is not available, consider:

### Vercel
- Free tier: 100GB bandwidth, 6000 build minutes/month
- Better for Next.js, similar for static sites
- Setup: Add `VERCEL_TOKEN` and `VERCEL_ORG_ID` secrets

### Cloudflare Pages
- Free tier: Unlimited bandwidth, 500 builds/month
- Fast global CDN
- Setup: Add `CLOUDFLARE_API_TOKEN` secret

### GitHub Pages PR Previews
- Built into GitHub (no secrets needed)
- Slower deployment but free
- Check out `gh-pages-preview` action

## Integration with Existing Workflows

### Main Deploy Workflow
- Runs on every push to `main`
- Deploys to `gh-pages` branch (production)
- No Netlify secrets needed

### CI Workflow
- Runs quality checks
- Does not deploy
- Works independently of preview deploy

### Preview Deploy Workflow
- Runs on pull requests
- Deploys to Netlify preview URLs
- Requires Netlify secrets

## References

- [Netlify Personal Access Tokens](https://app.netlify.com/user/applications#personal-access-tokens)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Actions/prepare GH Pages Deployment](https://topic.trys.at/deploy-preview-setup-thm with python)
- [DocMaker AI Deployments Documentation](/.github/workflows/README.md)
