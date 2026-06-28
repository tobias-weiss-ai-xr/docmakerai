.PHONY: help dev build clean capture capture-all list install install-hooks

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

list: ## List available capture workflows
	cd capture && python capture.py --list

install: ## Install Python + Playwright dependencies
	pip install -r capture/requirements.txt
	python -m playwright install chromium
