## [2026-06-27 08:52] Task: Set up second runner for true CI/Deploy parallelization

### What was done
1. SSH'd into `legion` machine (192.168.42.42) via the existing SSH config
2. Created a new runner directory `~/actions-runner-docmaker-ci` by copying the existing runner archive
3. Registered `docmaker-ci-runner` with only `ci` label (no `deploy`)
4. Installed and started as systemd service via `sudo ./svc.sh install && sudo ./svc.sh start`
5. Removed `ci` label from `legions-docmaker-runner` via GitHub API (`DELETE /repos/{owner}/{repo}/actions/runners/23/labels/ci`)
6. Removed stale `tobi-legion` runner (id 22) via GitHub API (`DELETE /repos/{owner}/{repo}/actions/runners/22`)

### Final runner configuration
- **docmaker-ci-runner** (ONLINE) — labels: `self-hosted, Linux, X64, legions, ci` — handles CI jobs only
- **legions-docmaker-runner** (ONLINE) — labels: `self-hosted, Linux, X64, legions, deploy` — handles deploy jobs only

### Workflow YAML mapping (already correct after previous changes)
- CI jobs → `runs-on: [self-hosted, linux, ci]`
- Deploy/Preview/Rollback jobs → `runs-on: [self-hosted, linux, deploy]`

### Access details
- Legion SSH: `ssh legion` (HostName 192.168.42.42, User weiss, key ~/.ssh/id_ed25519_ansible)
- Runner dir: `~/actions-runner-docmaker-ci/`
- Runner service: `actions.runner.tobias-weiss-ai-xr-docmakerai.docmaker-ci-runner.service`
- Runner registration token: Generated via `gh api --method POST /repos/{owner}/{repo}/actions/runners/registration-token`

### Token
- Runner registration tokens are obtained via the POST endpoint, not GET: `gh api --method POST /repos/{owner}/{repo}/actions/runners/registration-token --jq '.token'`
- Tokens expire after a short time and must be generated just before use

### Runner existing archive
- Legion already had `~/actions-runner/runner.tar.gz` (119 MB, version 2.335.1)
- Could copy to new directory and re-extract: `cp ~/actions-runner/runner.tar.gz ~/actions-runner-docmaker-ci/ && cd ~/actions-runner-docmaker-ci && tar xzf runner.tar.gz && rm runner.tar.gz`

### Label management via API
- Remove label: `DELETE /repos/{owner}/{repo}/actions/runners/{runner_id}/labels/{label_name}`
- Remove runner: `DELETE /repos/{owner}/{repo}/actions/runners/{runner_id}`
- Runner IDs visible in: `gh api /repos/{owner}/{repo}/actions/runners`
