#!/bin/bash
set -euo pipefail

RUNNER_SERVICE="actions.runner.tobias-weiss-ai-xr-docmakerai.docmaker-ci-runner.service"
RUNNER_NAME="docmaker-ci-runner"
REPO="tobias-weiss-ai-xr/docmakerai"
LOG="/var/log/runner-health.log"
STALE_THRESHOLD_MIN=10

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"
}

runner_is_stuck() {
  local runner_status
  runner_status=$(gh api "/repos/$REPO/actions/runners" 2>/dev/null)
  local is_busy
  is_busy=$(echo "$runner_status" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data['runners']:
    if r['name'] == '$RUNNER_NAME':
        print(r['busy'])
        break
")
  if [ "$is_busy" != "True" ]; then
    return 1
  fi

  local has_active_run
  has_active_run=$(gh run list --repo "$REPO" --limit 5 2>/dev/null | grep -c "in_progress" || true)
  if [ "$has_active_run" -gt 0 ]; then
    return 1
  fi

  local has_queued_run
  has_queued_run=$(gh run list --repo "$REPO" --limit 5 2>/dev/null | grep -c "queued" || true)
  if [ "$has_queued_run" -eq 0 ]; then
    return 1
  fi

  local oldest_queued_seconds
  oldest_queued_seconds=$(gh run list --repo "$REPO" --limit 5 --json "createdAt,status" 2>/dev/null | python3 -c "
import sys, json, datetime
runs = json.load(sys.stdin)
for r in runs:
    if r['status'] == 'queued':
        created = datetime.datetime.fromisoformat(r['createdAt'].replace('Z', '+00:00'))
        age = (datetime.datetime.now(datetime.timezone.utc) - created).total_seconds()
        print(int(age))
        break
" 2>/dev/null || echo "0")

  if [ "$oldest_queued_seconds" -lt $((STALE_THRESHOLD_MIN * 60)) ]; then
    return 1
  fi

  return 0
}

log "Checking runner health..."
if runner_is_stuck; then
  log "RUNNER STUCK: busy=$is_busy, queued=$has_queued_run. Restarting service..."
  sudo systemctl restart "$RUNNER_SERVICE"
  sleep 5
  if systemctl is-active --quiet "$RUNNER_SERVICE"; then
    log "Runner restarted successfully."
  else
    log "FAILED to restart runner!"
    exit 1
  fi
else
  log "Runner healthy."
fi
