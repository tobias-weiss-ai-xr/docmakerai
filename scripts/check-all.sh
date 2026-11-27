#!/usr/bin/env bash
# check-all.sh — unified pre-push gate script (--fast / --full / --e2e)
#
# Runs every quality check the project's CI pipeline would run, all from one
# command. Intended to be executed before pushing (locally, in a pre-push
# hook, or as a CI job) so that a push never lands broken code.
#
# Usage:
#   scripts/check-all.sh [mode]
#
# Modes:
#   --fast   Quick gate: shell + Python syntax, ruff lint, unit tests.
#            This is the default when no mode is given.
#   --full   Fast plus: ruff format check, TypeScript typecheck and the
#            dual-locale Docusaurus build.
#   --e2e    Full plus: Playwright end-to-end test suite.
#   -h|--help
#            Show this help and exit.
#
# Exit status: 0 when every selected check passes, 1 otherwise. A step that
# cannot run (tool not installed) prints a warning and is skipped so the gate
# stays usable on machines with only part of the toolchain installed.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

MODE="fast"

usage() {
  sed -n '2,$p' "${BASH_SOURCE[0]}" |
    awk '{ if ($0 ~ /^#/) { line = $0; sub(/^# ?/, "", line); if (line != "") print line } else exit }'
}

case "${1:-}" in
  "" | --fast) MODE="fast" ;;
  --full) MODE="full" ;;
  --e2e) MODE="e2e" ;;
  -h | --help)
    usage
    exit 0
    ;;
  *)
    echo "error: unknown mode '$1'" >&2
    echo
    usage
    exit 2
    ;;
esac

have() {
  command -v "$1" >/dev/null 2>&1
}

run_step() {
  local desc="$1"
  shift
  echo
  echo "==> $desc"
  "$@"
}

echo "DocMaker AI pre-push gate (mode: $MODE)"
echo "Repository root: $ROOT"

run_fast() {
  echo
  echo "### Fast gate: syntax + lint + unit tests"

  run_step "Shell syntax (bash -n)" \
    bash -n scripts/check-all.sh scripts/runner-health.sh \
    scripts/seed-doc-votes.sh .githooks/pre-commit

  run_step "Python syntax (py_compile)" \
    python3 -m py_compile scripts/check_coverage_trend.py \
    scripts/translate_accessibility.py scripts/annotate_screenshots.py \
    scripts/convert_to_mp4.py scripts/fix_table_bugs.py \
    scripts/generate_docs_from_specs.py accessibility/validate.py

  if have ruff; then
    run_step "Ruff lint (capture/, scripts/, accessibility/)" \
      ruff check capture/ scripts/ accessibility/
  else
    echo "!! ruff not found — skipping lint (pip install ruff)"
  fi

  if have pytest; then
    run_step "Python unit tests (scripts/tests, accessibility/tests)" \
      python3 -m pytest scripts/tests accessibility/tests -q
  else
    echo "!! pytest not found — skipping unit tests (pip install pytest)"
  fi
}

run_full() {
  run_fast

  echo
  echo "### Full gate: format + typecheck + site build"

  if have ruff; then
    run_step "Ruff format check (capture/, scripts/, accessibility/)" \
      ruff format --check capture/ scripts/ accessibility/
  fi

  if have npm; then
    if [ ! -d site/node_modules ]; then
      run_step "npm install (site dependencies)" npm install --prefix site
    fi
    run_step "TypeScript typecheck" npm --prefix site run typecheck
    run_step "Docusaurus build (locale en)" npm --prefix site run build -- --locale en
    run_step "Docusaurus build (locale de)" npm --prefix site run build -- --locale de
  else
    echo "!! npm not found — skipping typecheck and site build"
  fi
}

run_e2e() {
  run_full

  echo
  echo "### E2E gate: Playwright end-to-end tests"

  if have npm; then
    run_step "Playwright e2e suite" npm --prefix site run test:e2e
  else
    echo "!! npm not found — skipping e2e tests"
  fi
}

case "$MODE" in
  fast) run_fast ;;
  full) run_full ;;
  e2e) run_e2e ;;
esac

echo
echo "✔ check-all ($MODE) passed — ready to push."
