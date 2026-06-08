.PHONY: help capture generate site dev clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

capture: ## Run capture against SOGo demo
	cd capture && python -m capture capture \
		--workflow workflows/sogo-login.yaml \
		--url https://demo.sogo.nu/SOGo/ \
		--output ../tutorials/sogo/login/

capture-all: ## Run all SOGo workflows
	for wf in capture/workflows/*.yaml; do \
		name=$$(basename "$$wf" .yaml); \
		dir=$${name#sogo-}; \
		cd capture && python -m capture capture \
			--workflow "$$wf" \
			--url https://demo.sogo.nu/SOGo/ \
			--output "../tutorials/sogo/$$dir/" || true; \
	done

generate: ## Generate single tutorial from capture
	cd generator && python -m generator generate \
		--capture-dir ../tutorials/sogo/login/ \
		--output ../tutorials/sogo/login/README.md

generate-all: ## Generate all tutorials
	cd generator && python -m generator generate \
		--capture-dir ../tutorials/ \
		--output ../tutorials/

site: ## Start Docusaurus dev server
	cd site && npm run start

site-build: ## Build Docusaurus site
	cd site && npm run build

docker-build: ## Build all Docker images
	docker compose build

docker-up: ## Start all services
	docker compose up -d

docker-up-full: ## Start all services including RAG
	docker compose --profile full up -d

dev: ## Run full pipeline: capture -> generate -> site
	$(MAKE) capture && $(MAKE) generate && $(MAKE) site

clean: ## Clean generated files
	rm -rf tutorials/sogo/*/capture-result.json
	rm -rf tutorials/sogo/*/*.png
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
