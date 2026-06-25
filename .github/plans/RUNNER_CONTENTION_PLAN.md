# Runner Resource Contention — Fix Plan

## Current State

All 7 self-hosted jobs across 4 workflows use `runs-on: [self-hosted, linux]` → single `legions-docmaker-runner` → serial execution.

**Workflows competing for the same runner:**
- CI: `python-quality`, `accessibility-check`, `build-site`
- Deploy: `build`, `deploy`
- Preview: `preview`
- Rollback: `rollback`

**Concurrency groups are workflow-local** — they don't prevent cross-workflow contention.

## Recommended Fix: Second Runner + Label Routing

### Step 1: Register a second runner on legions

```bash
# SSH into legions (192.168.42.42), then:
mkdir -p ~/actions-runner-ci && cd ~/actions-runner-ci

# Download runner bundle (same version as existing)
curl -o actions-runner-linux-x64-2.319.1.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.319.1/actions-runner-linux-x64-2.319.1.tar.gz
tar xzf actions-runner-linux-x64-2.319.1.tar.gz

# Register with CI-specific labels
./config.sh --url https://github.com/tobias-weiss-ai-xr/docmakerai \
  --token <TOKEN> \
  --name legions-docmaker-runner-ci \
  --labels linux,legions,ci \
  --unattended

# Install as systemd service
sudo ./svc.sh install
sudo ./svc.sh start
```

Existing runner (`legions-docmaker-runner`) keeps labels `linux,legions,deploy`.

### Step 2: Update workflow runs-on labels

| Workflow | Job | New runs-on |
|---|---|---|
| CI | `python-quality` | `[self-hosted, linux, ci]` |
| CI | `accessibility-check` | `[self-hosted, linux, ci]` |
| CI | `build-site` | `[self-hosted, linux, ci]` |
| Deploy | `build` | `[self-hosted, linux, deploy]` |
| Deploy | `deploy` | `[self-hosted, linux, deploy]` |
| Preview | `preview` | `[self-hosted, linux, deploy]` |
| Rollback | `rollback` | `[self-hosted, linux, deploy]` |

GitHub-hosted `ubuntu-latest` jobs (cleanup-artifacts, detect-changes, skip-deploy) are unaffected.

### Step 3: Verify

- Push a PR → CI runs on `legions-docmaker-runner-ci`
- Push to main → Deploy runs on `legions-docmaker-runner`
- Both run in parallel without queuing

## Alternative: Single Runner with Workflow-Specific Labels (No Second Runner)

If a second runner is not feasible, update the single runner's labels:
```bash
# On legions, reconfigure existing runner
cd ~/actions-runner
./config.sh --remove --token <TOKEN>
./config.sh --url https://github.com/tobias-weiss-ai-xr/docmakerai \
  --token <TOKEN> \
  --name legions-docmaker-runner \
  --labels linux,legions,ci,deploy,preview \
  --unattended
```

Then all workflows target `[self-hosted, linux]` as before (no YAML changes needed).
This doesn't fix contention — jobs still queue — but enables future label-based routing.

## Branch Protection Rules

Configure in GitHub repo: Settings → Branches → Add rule (main):

- [x] Require a pull request before merging (1 approval)
- [x] Require status checks to pass before merging
  - [x] `ci/python-tests`
  - [x] `deployment/production` (only for deploy workflow)
- [x] Require branches to be up-to-date
- [x] Do not allow bypassing the above settings
- [ ] Include administrators (optional)

This separates CI checks from the deploy gate: CI must pass before merge, deploy runs after merge.
