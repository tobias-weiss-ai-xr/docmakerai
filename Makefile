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
	@echo "  User:   testuser@example.org"
	@echo ""
	@if [ -z "$$(docker compose -f /home/weissto_local/git/sogo/sogo-live/sogo6-stalwart-openldap-dockerized/docker-compose.yaml ps -q sogo6-ui 2>/dev/null)" ]; then \
		echo "⚠️  Local SOGo 6 stack not running. Start it with:"; \
		echo "   cd /home/weissto_local/git/sogo/sogo-live/sogo6-stalwart-openldap-dockerized && make start"; \
		exit 1; \
	fi
	cd capture && SOGO_URL=http://localhost:3000 \
		SOGO_USERNAME=testuser@example.org \
		SOGO_PASSWORD=password123 \
		python run_screenshot_captures.py

capture-sogo6-doc: ## Capture a single SOGo 6 doc (make capture-sogo6-doc DOC=calendar-create-event)
	@echo "Running SOGo 6 capture for $(DOC)..."
	cd capture && SOGO_URL=http://localhost:3000 \
		SOGO_USERNAME=testuser@example.org \
		SOGO_PASSWORD=password123 \
		python run_single_screenshot.py \
		$$(pwd)/run_screenshot_captures.py record_$(DOC)

list: ## List available capture workflows
	cd capture && python capture.py --list

install: ## Install Python + Playwright dependencies
	pip install -r capture/requirements.txt
	python -m playwright install chromium
