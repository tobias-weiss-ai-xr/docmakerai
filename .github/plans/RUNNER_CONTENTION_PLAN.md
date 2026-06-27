# Runner Resource Contention — Fix Plan

## ✅ IMPLEMENTED — 2026-06-27

## Final Configuration

| Runner | Labels | Status | Job Type |
|---|---|---|---|
| `docmaker-ci-runner` | `self-hosted, Linux, X64, legions, ci` | ✅ ONLINE | CI jobs |
| `legions-docmaker-runner` | `self-hosted, Linux, X64, legions, deploy` | ✅ ONLINE | Deploy jobs |

### What Was Done

1. **Created `docmaker-ci-runner`** on legion (192.168.42.42):
   - Directory: `~/actions-runner-docmaker-ci/`
   - Copied existing runner archive (v2.335.1, 119MB) from `~/actions-runner/runner.tar.gz`
   - Registered with token via `gh api --method POST /repos/{repo}/actions/runners/registration-token`
   - Labels: `linux,legions,ci` (no `deploy`)
   - Installed + started as systemd service: `sudo ./svc.sh install && sudo ./svc.sh start`
   - Service: `actions.runner.tobias-weiss-ai-xr-docmakerai.docmaker-ci-runner.service`

2. **Stripped `ci` label from `legions-docmaker-runner`:**
   - API call: `DELETE /repos/tobias-weiss-ai-xr/docmakerai/actions/runners/23/labels/ci`
   - Now deploy-only: works with `[self-hosted, linux, deploy]` workflows

3. **Removed stale `tobi-legion` runner** (id 22, was offline):
   - API call: `DELETE /repos/tobias-weiss-ai-xr/docmakerai/actions/runners/22`

4. **Workflow YAMLs already aligned** (changed in previous session):
   - CI jobs → `[self-hosted, linux, ci]`
   - Deploy/Preview/Rollback → `[self-hosted, linux, deploy]`

### Verification

- `gh api /repos/{repo}/actions/runners` shows 2 runners, both online
- `sudo systemctl is-active` confirms both services `active` on legion
- No stale runners remain
- CI jobs route to `docmaker-ci-runner`, Deploy jobs to `legions-docmaker-runner`
- Jobs can run simultaneously without contention

## Branch Protection Rules (Not Yet Implemented)
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
