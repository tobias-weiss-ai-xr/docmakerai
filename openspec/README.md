# OpenSpec — DocMaker AI

Living specifications for the SOGo documentation capture pipeline.

## Structure

```
openspec/
├── config.yaml              # Project configuration
├── specs/                   # Source of truth (current system behavior)
│   ├── auth-session/
│   │   └── spec.md
│   ├── calendar/
│   │   └── spec.md
│   ├── mail/
│   │   └── spec.md
│   ├── contacts/
│   │   └── spec.md
│   ├── preferences/
│   │   └── spec.md
│   └── capture-pipeline/
│       └── spec.md
└── changes/                 # Proposed updates (one folder per change)
    └── <change-name>/
        ├── proposal.md
        ├── design.md
        ├── tasks.md
        └── specs/           # Delta specs (ADDED/MODIFIED/REMOVED)
```

## How to use

### Read current behavior
Browse `specs/<domain>/spec.md` to understand what the system does today.

### Propose a change
1. Create `changes/<change-name>/proposal.md` — describe the "why" and "what"
2. Add `specs/<domain>/spec.md` delta — show ADDED/MODIFIED/REMOVED requirements
3. Optionally add `design.md` for technical approach
4. Add `tasks.md` as implementation checklist
5. On completion, merge delta into main `specs/`

### Spec format
- **Requirements** use RFC 2119 keywords: MUST, SHALL, SHOULD, MAY
- **Scenarios** use Given/When/Then format
- Each requirement MUST have at least one scenario

## Domains

| Domain | Covers |
|--------|--------|
| `auth-session` | Login, logout, credential handling, session state |
| `calendar` | Event creation, recurring events, edit/delete, views, sharing, subscriptions, free/busy, iCal import/export |
| `mail` | Compose, read, reply/forward/delete, folder management, filters, signatures |
| `contacts` | Add, edit/delete, import/export |
| `preferences` | Settings, password change, vacation auto-reply, global search |
| `capture-pipeline` | WorkflowRecorder, StepTracker, annotation engine, WebP/PNG output, asset management |
