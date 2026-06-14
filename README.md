# SOGo User Documentation

**Step-by-step tutorials and user guides for [SOGo Groupware](https://www.sogo.nu).**

This project provides end-user documentation for SOGo — the open-source groupware
solution for email, calendars, contacts, and tasks.

---

## Contents

| Topic | Description |
|-------|-------------|
| [Login](./site/docs/sogo-login.md) | Logging into SOGo |
| Calendar *(coming soon)* | Creating events, sharing calendars, CalDAV setup |
| Mail *(coming soon)* | Composing, reading, and organizing email |
| Contacts *(coming soon)* | Managing address books |
| Admin *(coming soon)* | Server configuration and user management |

---

## Local Development

### Prerequisites

- Node.js 20+

### Quick Start

```bash
# Install dependencies
cd site
npm install

# Start development server
npm run start
# → http://localhost:3000
```

### Build static site

```bash
cd site
npm run build
# Output: site/build/
```

---

## Project Structure

```
docmakerai/
├── site/                     # Docusaurus documentation site
│   ├── docs/                 # Tutorial markdown sources
│   │   ├── _category_.json   # Sidebar category config
│   │   └── sogo-login.md     # Login tutorial
│   ├── docusaurus.config.ts  # Site configuration
│   ├── sidebars.ts           # Navigation sidebar
│   ├── src/                  # Custom CSS
│   └── package.json          # Dependencies
├── Makefile                  # Development commands
└── README.md
```

---

## License

MIT
