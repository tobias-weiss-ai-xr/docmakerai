.PHONY: help dev build clean capture capture-all capture-sogo6 capture-sogo6-doc list install install-hooks

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-hooks: ## Install git hooks from .githooks/ (one-time per clone)
	git config core.hooksPath .githooks

dev: ## Start Docusaurus dev server
	cd site && npm run start

build: ## Build static site
	cd site && npm run build

clean: ## Clear Docusaurus cache + captured media
	cd site && npm run clear
	rm -rf capture/screenshots/* capture/gifs/*

capture: ## Capture screenshots/GIFs for a workflow (make capture wf=calendar-create-event)
	cd capture && python capture.py workflows/$(wf).yaml

capture-all: ## Run all capture workflows
	cd capture && python capture.py --all

capture-sogo6: ## Capture all SOGo 6 screenshots (requires local stack at localhost:3000)
	@echo "Running SOGo 6 screenshot capture pipeline..."
	@echo "  Target: http://localhost:3000 (sogo6-stalwart-openldap-dockerized)"
	@echo "  User:   lisa.mayer@example.org"
	@echo "  Note:   Pre-warming Next.js routes to avoid empty responses..."
	@for route in /en/auth/login /en/auth/login/pwd /en/u/0/INBOX /en/calendar; do \
		curl -sf -o /dev/null "http://localhost:3000$$route" 2>/dev/null & \
	done; \
	wait
	@echo "  Routes warmed."
	@echo ""
	cd capture && SOGO_URL=http://localhost:3000 \
		SOGO_USERNAME=lisa.mayer@example.org \
		SOGO_PASSWORD='UniMarburg2026!' \
		python run_screenshot_captures.py

capture-sogo6-doc: ## Capture a single SOGo 6 doc (make capture-sogo6-doc DOC=calendar-create-event)
	@echo "Running SOGo 6 capture for $(DOC)..."
	@echo "  Pre-warming Next.js routes..."
	@for route in /en/auth/login /en/auth/login/pwd /en/u/0/INBOX; do \
		curl -sf -o /dev/null "http://localhost:3000$$route" 2>/dev/null & \
	done; \
	wait
	@echo "  Routes warmed."
	cd capture && SOGO_URL=http://localhost:3000 \
		SOGO_USERNAME=lisa.mayer@example.org \
		SOGO_PASSWORD='UniMarburg2026!' \
		python run_single_screenshot.py \
		$$(pwd)/run_screenshot_captures.py record_$(DOC)

list: ## List available capture workflows
	cd capture && python capture.py --list

install: ## Install Python + Playwright dependencies
	pip install -r capture/requirements.txt
	python -m playwright install chromium
