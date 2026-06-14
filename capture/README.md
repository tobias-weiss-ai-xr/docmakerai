# Capture Pipeline

Automatically takes screenshots and creates animated GIFs from SOGo workflows.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Set environment
export SOGO_URL=https://demo.sogo.nu/SOGo/
export SOGO_USERNAME=demo
export SOGO_PASSWORD=demo
export SOGO_RECIPIENT=colleague@example.com
export EVENT_DATE=2026-06-15

# Run a single workflow
python capture.py workflows/calendar-create-event.yaml

# Run all workflows
python capture.py --all

# List available workflows
python capture.py --list
```

## Output

- Screenshots → `capture/screenshots/`
- GIFs → `capture/gifs/`
- Assets (auto-copied for site) → `site/docs/assets/`

## Workflow YAML Format

```yaml
name: "Workflow Name"
base_url: "${SOGO_URL}"
auth:
  username: "${SOGO_USERNAME}"
  password: "${SOGO_PASSWORD}"
steps:
  - id: step-name
    action: click           # navigate | click | type | select | wait
    selector: "css-selector"
    value: "input value"    # for type/select actions
    url: "https://..."      # for navigate action
    screenshot: file.png    # take screenshot (saved to screenshots/)
    gif_start: true         # begin GIF sequence
    gif_end: true           # end GIF sequence (gif_name required)
    gif_name: anim.gif      # output GIF filename
    wait_after: 2           # seconds to wait after action
    wait_before: 1          # seconds to wait before action
```

Values support `${ENV_VAR}` substitution from environment variables.

## Workflows

| File | Tutorial |
|------|----------|
| `calendar-create-event.yaml` | Create a Calendar Event |
| `calendar-recurring.yaml` | Set Up Recurring Event with Alarms |
| `mail-compose.yaml` | Compose and Send an Email |
