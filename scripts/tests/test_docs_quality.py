"""Regression tests for doc quality bugs fixed from SOGo 5 reviewer feedback.

Catches, before they ship again:
- ``: Description`` suffixes appended to table headers (was injected by
  accessibility/validate.py --fix, now removed)
- ``| |`` empty first cells in table rows (template bug that propagated)
- English ``## Accessibility`` sections left inside German docs
- informal German: ``Auto-Antwort`` (-> ``Automatische Antwort``)
- UI inaccuracies: ``linke Seitenleiste``/``left sidebar``, ``Zahnrad``/``gear icon``,
  ``Rechtsklick``/``right-click`` (SOGo 5 uses a top navigation bar + three-dot menu)
- footer/navbar links that point at a version path that does not exist
  (e.g. ``/5/`` instead of ``/sogo5/``)
"""

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE = REPO_ROOT / "site"
DOC_DIRS = [
    SITE / "versioned_docs" / "version-5",
    SITE / "versioned_docs" / "version-6",
    SITE / "i18n" / "de" / "docusaurus-plugin-content-docs" / "version-5",
    SITE / "i18n" / "de" / "docusaurus-plugin-content-docs" / "version-6",
]
DE_DIRS = [d for d in DOC_DIRS if "i18n" in str(d)]

# ROADMAP.md is English meta-content about the docs site, not SOGo docs
DE_EXCLUDE = {"ROADMAP.md"}


@pytest.fixture(scope="session")
def md_files():
    """All markdown files in the SOGo doc directories, keyed by display path."""
    files = {}
    for d in DOC_DIRS:
        if not d.exists():
            continue
        for p in sorted(d.glob("*.md")):
            files[str(p.relative_to(REPO_ROOT))] = p
    return files


def _read(file: Path) -> list[str]:
    return file.read_text(encoding="utf-8").splitlines()


def _violations(files: dict, pattern: str, flags=0) -> list[str]:
    """Return 'path:lineno' for every line matching pattern across all files."""
    out = []
    for name, path in files.items():
        for i, line in enumerate(_read(path), 1):
            if re.search(pattern, line, flags):
                out.append(f"{name}:{i}")
    return out


# ---------------------------------------------------------------------------
# table quality
# ---------------------------------------------------------------------------


def test_no_description_suffix_in_any_table_header(md_files):
    bad = _violations(md_files, r"\|\s*\w[\w ]*:\s*Description\s*\|")
    assert not bad, "Table headers must not have ': Description' suffix:\n" + "\n".join(bad)


def test_no_empty_first_cell_in_any_table(md_files):
    bad = _violations(md_files, r"^\|\s*\|")
    assert not bad, "Empty first table cell (| |):\n" + "\n".join(bad)


def test_no_table_row_wider_than_header(md_files):
    """A data row must never have more cells than its header row (overflow)."""
    bad = []
    for name, path in md_files.items():
        lines = _read(path)
        for i, line in enumerate(lines):
            if "|" not in line or i + 1 >= len(lines):
                continue
            if not re.match(r"^\s*\|[\-\s|:]+\|\s*$", lines[i + 1]):
                continue
            header_cols = line.count("|")
            j = i + 2
            while j < len(lines) and "|" in lines[j]:
                if lines[j].count("|") > header_cols:
                    bad.append(f"{name}:{j + 1}")
                j += 1
    assert not bad, "Table rows wider than header (overflow):\n" + "\n".join(bad)


def test_no_shifted_table_content(md_files):
    """A short row must not have an empty non-last cell (content-shift bug)."""
    bad = []
    for name, path in md_files.items():
        lines = _read(path)
        for i, line in enumerate(lines):
            if "|" not in line or i + 1 >= len(lines):
                continue
            if not re.match(r"^\s*\|[\-\s|:]+\|\s*$", lines[i + 1]):
                continue
            header_cols = line.count("|")
            j = i + 2
            while j < len(lines) and "|" in lines[j]:
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                row_cols = len(cells)
                if row_cols < header_cols and any(not c for c in cells[:-1]):
                    bad.append(f"{name}:{j + 1}")
                j += 1
    assert not bad, "Short table rows with empty middle cell (content shift):\n" + "\n".join(bad)


# ---------------------------------------------------------------------------
# links & assets
# ---------------------------------------------------------------------------


def test_no_broken_asset_links(md_files):
    """Every `](./assets/...)` reference must resolve to a real file."""
    bad = []
    for name, path in md_files.items():
        for i, line in enumerate(_read(path), 1):
            for ref in re.findall(r"\./assets/([^)\s]+)", line):
                target = path.parent / "assets" / ref.rstrip(")")
                if not target.exists():
                    bad.append(f"{name}:{i} -> assets/{ref}")
    assert not bad, "Broken asset links:\n" + "\n".join(bad)


def test_no_broken_internal_doc_links(md_files):
    """Every `](./sogo-*.md)` or `](./sogo-*)` link must resolve to a sibling doc."""
    bad = []
    for name, path in md_files.items():
        for i, line in enumerate(_read(path), 1):
            for ref in re.findall(r"\./(sogo-[^)#\s]+)(?:\.md)?", line):
                target = path.parent / f"{ref}.md"
                if not target.exists():
                    bad.append(f"{name}:{i} -> {ref}")
    assert not bad, "Broken internal doc links:\n" + "\n".join(bad)


def test_all_images_have_alt_text(md_files):
    bad = _violations(md_files, r"!\s*\[\s*\]\(")
    assert not bad, "Images without alt text (screen reader):\n" + "\n".join(bad)


def test_admonitions_are_balanced(md_files):
    """Every `:::` admonition opener must be closed with `:::`."""
    bad = []
    for name, path in md_files.items():
        in_block = None
        for i, line in enumerate(_read(path), 1):
            if line.startswith(":::"):
                in_block = (i, line) if in_block is None else None
        if in_block is not None:
            bad.append(f"{name}:{in_block[0]} ({in_block[1].strip()})")
    assert not bad, "Unbalanced ::: admonitions:\n" + "\n".join(bad)


# ---------------------------------------------------------------------------
# german i18n
# ---------------------------------------------------------------------------


def _de_files(md_files: dict) -> dict:
    return {
        n: p
        for n, p in md_files.items()
        if any(str(p).startswith(str(d)) for d in DE_DIRS) and p.name not in DE_EXCLUDE
    }


def test_de_files_use_german_accessibility_heading(md_files):
    files = _de_files(md_files)
    bad = [
        n
        for n, p in files.items()
        if any(re.match(r"^##\s*Accessibility\s*$", line) for line in _read(p))
    ]
    msg = "German files must use '## Barrierefreiheit', not '## Accessibility':\n"
    assert not bad, msg + "\n".join(bad)


def test_de_files_have_no_auto_antwort(md_files):
    files = _de_files(md_files)
    bad = _violations(files, r"Auto-Antwort")
    assert not bad, "Use 'Automatische Antwort', not 'Auto-Antwort':\n" + "\n".join(bad)


def test_de_shortcut_key_label_is_strg(md_files):
    """German Windows uses 'Strg'; DE docs must not use 'Ctrl'."""
    files = _de_files(md_files)
    bad = _violations(files, r"Ctrl")
    assert not bad, "Use 'Strg' (German keyboard label), not 'Ctrl':\n" + "\n".join(bad)


# ---------------------------------------------------------------------------
# SOGo 5 UI accuracy (all languages)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "pattern,what",
    [
        (r"linke\s*Seitenleiste", "linke Seitenleiste"),
        (r"left\s*sidebar", "left sidebar"),
        (r"Zahnrad", "Zahnrad (gear icon)"),
        (r"gear\s*icon", "gear icon"),
        (r"Rechtsklick|rechte[nm]?\s*Maustaste", "right-click (German)"),
        (r"right[- ]?click", "right-click"),
    ],
)
def test_no_outdated_ui_references(md_files, pattern, what):
    bad = _violations(md_files, pattern, flags=re.IGNORECASE)
    # Reviewer-verified exception: the settings gear exists and is called
    # "Zahnrad"/"gear icon" in the real UI (SOGo_5_Kritik: "immerhin stimmt
    # das Zahnrad diesmal"). Only flag gear words NOT tied to settings.
    if what in ("Zahnrad (gear icon)", "gear icon"):
        bad = [
            v
            for v in bad
            if not re.search(
                r"Einstellungen|Settings|settings|kein Zahnrad|no gear icon",
                _line(v),
                re.IGNORECASE,
            )
        ]
    assert not bad, f"'{what}' — SOGo 5 uses top nav + three-dot menu:\n" + "\n".join(bad)


def _line(ref: str) -> str:
    path, _, lineno = ref.rpartition(":")
    return _read(Path(path))[int(lineno) - 1]


# ---------------------------------------------------------------------------
# feedback taskfleet Wave 6 guards (T6.1, reviewer-verified phrases)
# ---------------------------------------------------------------------------


FORBIDDEN_PHRASES = [
    "Durch die Zeit",
    "Kontaktgruppen",
    "Schaltfläche **Verfassen**",
    "Schaltfläche **Suche**",
    "Schaltfläche Verfassen",
    "Schaltfläche Suche",
    "hilfsweise",
]


REQUIRED_CONTAINS = {
    "i18n/de/docusaurus-plugin-content-docs/version-{v}/sogo-mail-folders-filters.md": [
        "Beende die Filterverarbeitung",
        "Filter erstellen",
        "serverseitige E-Mail-Filterung",
    ],
    "i18n/de/docusaurus-plugin-content-docs/version-{v}/sogo-mail-signatures.md": [
        "IMAP-Konten",
        "Neue Identität",
    ],
}


def test_wave6_forbidden_phrases_absent():
    dirs = [
        SITE / "i18n/de/docusaurus-plugin-content-docs/version-5",
        SITE / "i18n/de/docusaurus-plugin-content-docs/version-6",
        SITE / "versioned_docs/version-5",
        SITE / "versioned_docs/version-6",
    ]
    bad = [
        f"{p.relative_to(SITE)}: {phrase}"
        for d in dirs
        for p in sorted(d.glob("*.md"))
        for phrase in FORBIDDEN_PHRASES
        if phrase in _read(p)
    ]
    assert not bad, "Reviewer-verified phrases that must not reappear:\n" + "\n".join(bad)


def test_wave6_required_phrases_present():
    missing = []
    for tpl, phrases in REQUIRED_CONTAINS.items():
        for v in ("5", "6"):
            path = SITE / tpl.format(v=v)
            text = path.read_text(encoding="utf-8") if path.exists() else ""
            missing += [f"{path.name} (v{v}): {p}" for p in phrases if p not in text]
    assert not missing, "Required verified phrases missing:\n" + "\n".join(missing)


# ---------------------------------------------------------------------------
# translation / version parity
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "dir_a,dir_b,what",
    [
        (DOC_DIRS[0], DOC_DIRS[2], "EN v5 vs DE v5"),
        (DOC_DIRS[1], DOC_DIRS[3], "EN v6 vs DE v6"),
        (DOC_DIRS[0], DOC_DIRS[1], "EN v5 vs EN v6"),
        (DOC_DIRS[2], DOC_DIRS[3], "DE v5 vs DE v6"),
    ],
)
def test_tutorial_page_parity(dir_a, dir_b, what):
    """Tutorial pages (sogo-*.md, excl. spec/gaps) must exist in every locale/version."""

    def tutorial_names(d):
        return {
            p.name
            for p in Path(d).glob("sogo-*.md")
            if "spec" not in p.name and "gaps" not in p.name
        }

    a, b = tutorial_names(dir_a), tutorial_names(dir_b)
    missing_in_b = sorted(a - b)
    extra_in_b = sorted(b - a)
    assert not missing_in_b and not extra_in_b, (
        f"{what} page set mismatch:\n  in A only: {missing_in_b}\n  in B only: {extra_in_b}"
    )


# ---------------------------------------------------------------------------
# config link integrity
# ---------------------------------------------------------------------------


def test_config_links_use_real_version_paths():
    """Any footer/navbar link to a version must use the version's configured path."""
    config = (SITE / "docusaurus.config.ts").read_text(encoding="utf-8")
    # versions map label->path, e.g. '5': {label: 'SOGo 5', path: 'sogo5'}
    paths = dict(re.findall(r"'?(\d+)'?:\s*\{[^}]*path:\s*'([^']+)'", config))
    assert paths, "No version paths found in docusaurus.config.ts"

    # any link target of the form /<n>/ must match a configured version path
    bad = []
    for target in re.findall(r"(?:to|href):\s*'(/[^']*)'", config):
        m = re.match(r"^/(\d+)/?$", target)
        if m and paths.get(m.group(1)) not in target:
            bad.append(f"{target!r} (version path is {paths[m.group(1)]!r})")
    assert not bad, "Version links must use configured path:\n" + "\n".join(bad)


# ---------------------------------------------------------------------------
# structural quality
# ---------------------------------------------------------------------------


def _tutorial_pages(md_files: dict) -> dict:
    return {
        n: p
        for n, p in md_files.items()
        if "sogo-" in p.name and "spec" not in p.name and "gaps" not in p.name
    }


def test_every_tutorial_page_has_accessibility_section(md_files):
    """Screen-reader users need the a11y section on every tutorial page."""
    bad = []
    for name, path in _tutorial_pages(md_files).items():
        needle = "Barrierefreiheit" if "i18n" in str(path) else "Accessibility"
        pat = re.compile(rf"^#{{1,3}}\s*{needle}\s*$", re.M)
        if not pat.search(path.read_text(encoding="utf-8")):
            bad.append(f"{name} (missing ## {needle})")
    assert not bad, "Tutorial pages must carry an accessibility section:\n" + "\n".join(bad)


def test_no_broken_same_file_anchors(md_files):
    """Every `](#heading)` must resolve to a heading slug in the same file."""

    def slugify(heading: str) -> str:
        return re.sub(
            r"[^a-zA-Z0-9\-\u00C0-\u024F\u0300-\u036f]+", "-", heading.strip().lower()
        ).strip("-")

    bad = []
    for name, path in _tutorial_pages(md_files).items():
        lines = _read(path)
        slugs = {
            slugify(m.group(1)) for m in (re.match(r"^#{1,6}\s+(.+)$", ln) for ln in lines) if m
        }
        for i, line in enumerate(lines, 1):
            for m in re.finditer(r"\]\(#([^)#\s]+)\)", line):
                if m.group(1).rstrip("-") not in slugs:
                    bad.append(f"{name}:{i} -> #{m.group(1)}")
    assert not bad, "Broken same-file anchor links:\n" + "\n".join(bad)


def test_no_trailing_whitespace(md_files):
    # 2 trailing spaces = Markdown hard line break (renders <br>), that's fine
    bad = []
    for name, path in md_files.items():
        for i, line in enumerate(_read(path), 1):
            stripped = line.rstrip()
            if stripped != line and len(line) - len(stripped) != 2:
                bad.append(f"{name}:{i}")
    assert not bad, "Trailing whitespace (markdown hygiene):\n" + "\n".join(bad)


def test_markdown_structural_hygiene(md_files):
    """Code fences balanced, images have closing parens, no missing front matter."""
    bad = []
    for name, path in _tutorial_pages(md_files).items():
        txt = path.read_text(encoding="utf-8")
        if txt.count("```") % 2 != 0:
            bad.append(f"{name}: unbalanced ``` fences")
        for m in re.finditer(r"!\[[^\]]*\]\([^)]*$", txt, re.M):
            bad.append(f"{name}: unterminated image: {m.group(0)[:40]}")
        if not re.search(r"^---$.*?^title:\s*.+?$.*?^description:\s*.+?$", txt, re.M | re.S):
            bad.append(f"{name}: missing title/description front matter")
    assert not bad, "Markdown structural issues:\n" + "\n".join(bad)


# ---------------------------------------------------------------------------
# version & translation cross-checks
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "doc_dir,version",
    [
        (SITE / "versioned_docs" / "version-5", "5"),
        (SITE / "versioned_docs" / "version-6", "6"),
        (SITE / "i18n" / "de" / "docusaurus-plugin-content-docs" / "version-5", "5"),
        (SITE / "i18n" / "de" / "docusaurus-plugin-content-docs" / "version-6", "6"),
    ],
)
def test_doc_version_labels_match_directory(doc_dir, version):
    """A file in version-6/docs must talk about SOGo 6, never SOGo 5."""
    other = "5" if version == "6" else "6"
    bad = []
    for p in doc_dir.glob("sogo-*.md"):
        if "spec" in p.name or "gaps" in p.name:
            continue
        for i, line in enumerate(_read(p), 1):
            if re.search(rf"SOGo\s+{other}\b", line):
                bad.append(f"{p.name}:{i}: {line.strip()[:60]}")
    assert not bad, (
        f"{doc_dir.name} must reference SOGo {version}, not SOGo {other}:\n" + "\n".join(bad)
    )


def test_every_doc_has_single_h1(md_files):
    bad = []
    for name, path in _tutorial_pages(md_files).items():
        h1 = [ln for ln in _read(path) if ln.startswith("# ")]
        if len(h1) != 1:
            bad.append(f"{name}: {len(h1)} H1 headings")
    assert not bad, "Each page must have exactly one H1:\n" + "\n".join(bad)


def test_no_empty_link_text(md_files):
    bad = _violations(md_files, r"!?\[\]\(")
    assert not bad, "Links/images with empty text/alt:\n" + "\n".join(bad)


@pytest.mark.parametrize(
    "version",
    ["version-5", "version-6"],
)
def test_step_schritt_count_matches_between_languages(version):
    """DE translation must not drop or invent procedure steps vs EN source."""
    en_dir = SITE / "versioned_docs" / version
    de_dir = SITE / "i18n" / "de" / "docusaurus-plugin-content-docs" / version
    bad = []
    for p in en_dir.glob("sogo-*.md"):
        if "spec" in p.name or "gaps" in p.name:
            continue
        de = de_dir / p.name
        if not de.exists():
            continue
        en = len(re.findall(r"^#{1,6}\s+Step\s+\d+", p.read_text(encoding="utf-8"), re.I | re.M))
        de_n = len(
            re.findall(
                r"^#{1,6}\s+Schritt\s+\d+",
                de.read_text(encoding="utf-8"),
                re.M,
            )
        )
        if en != de_n:
            bad.append(f"{p.name}: EN {en} steps vs DE {de_n} Schritte")
    assert not bad, "Step/Schritt count mismatch:\n" + "\n".join(bad)


def _sidebar_doc_ids(sidebar: dict) -> list[str]:
    """All doc ids referenced by a Docusaurus sidebar config."""
    ids = []

    def walk(items):
        for item in items:
            if isinstance(item, str):
                ids.append(item)
            elif isinstance(item, dict):
                walk(item.get("items", []))

    walk(sidebar.get("tutorialSidebar", []))
    return ids


def test_sidebar_ids_resolve_to_source_docs():
    """Every doc id in the versioned sidebars must exist as a version-5/6 EN file."""
    bad = []
    for version in ["version-5", "version-6"]:
        sb = json.loads((SITE / "versioned_sidebars" / f"{version}-sidebars.json").read_text())
        ids = _sidebar_doc_ids(sb)
        for doc_id in ids:
            if not (SITE / "versioned_docs" / version / f"{doc_id}.md").exists():
                bad.append(f"{version}: sidebar id '{doc_id}' has no doc file")
    assert not bad, "Sidebar references missing docs:\n" + "\n".join(bad)


# ---------------------------------------------------------------------------
# reviewer-feedback wording + step/table structure
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "pattern,what",
    [
        (r"Selbstbedienung", "Selbstbedienung (should be 'selbstständige Passwortänderung')"),
        (r"durch die Zeit navigieren", "'durch die Zeit navigieren' (should be 'in der Zeit')"),
        (r"großartige", "'großartige' (should be 'nützliche')"),
        (r"Jeder, oder", "'Jeder, oder' (stray comma)"),
        (r"Sie sind hier richtig", "'Sie sind hier richtig' (was reviewer-flagged wording)"),
    ],
)
def test_no_reviewer_flagged_german_phrases(md_files, pattern, what):
    bad = _violations(_de_files(md_files), pattern)
    assert not bad, f"{what}:\n" + "\n".join(bad)


def test_steps_are_sequential_within_section(md_files):
    """Within each ## section, Step/Schritt numbers restart at 1 and increment by 1."""
    from collections import Counter

    bad = []
    for name, path in _tutorial_pages(md_files).items():
        current: list[int] = []  # steps in the active ## section
        for line in _read(path):
            if re.match(r"^##\s+", line):
                current = []
                continue
            m = re.match(r"^###\s+(?:Step|Schritt)\s+(\d+)\b", line, re.I)
            if m:
                current.append(int(m.group(1)))
                if len(current) >= 2 and current[-1] != current[-2] + 1:
                    bad.append(f"{name}: sequence ...{current[-3:]} skips")
                elif any(c > 1 for c in Counter(current).values()):
                    bad.append(f"{name}: repeated step number in section: {current}")
    assert not bad, "Non-sequential step numbering inside a section:\n" + "\n".join(bad)


def test_no_duplicate_table_headers_in_one_table(md_files):
    """A table must not have two columns with the same header text."""
    bad = []
    for name, path in md_files.items():
        lines = _read(path)
        for i, line in enumerate(lines):
            if i + 1 >= len(lines) or not re.match(r"^\s*\|[-\s|:]+\|\s*$", lines[i + 1]):
                continue
            if "|" not in line:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != len(set(cells)):
                bad.append(f"{name}:{i + 1}: {cells}")
    assert not bad, "Duplicate table headers within a table:\n" + "\n".join(bad)


@pytest.mark.parametrize(
    "doc_dir",
    [
        SITE / "versioned_docs" / "version-5",
        SITE / "versioned_docs" / "version-6",
        SITE / "i18n" / "de" / "docusaurus-plugin-content-docs" / "version-5",
        SITE / "i18n" / "de" / "docusaurus-plugin-content-docs" / "version-6",
    ],
)
def test_no_orphaned_assets(doc_dir):
    """Every file in assets/ must be referenced by at least one doc."""
    assets_dir = doc_dir / "assets"
    if not assets_dir.exists():
        return  # version dirs without assets are fine
    refs = set()
    for p in doc_dir.glob("*.md"):
        refs |= set(re.findall(r"\./assets/([^)\s]+)", p.read_text(encoding="utf-8")))
    orphans = sorted(
        str(a.relative_to(SITE)) for a in assets_dir.iterdir() if a.is_file() and a.name not in refs
    )
    assert not orphans, "Orphaned asset files (not referenced by any doc):\n" + "\n".join(orphans)


# ---------------------------------------------------------------------------
# accessibility & inline formatting
# ---------------------------------------------------------------------------


def test_no_vague_link_text(md_files):
    """Screenreader users hear link text in isolation: 'here'/'hier' is useless."""
    vague = (
        r"\[\s*(?:here|click here|Click here|Here|this link|this page|"
        r"hier|Hier|dieser Link|diese Seite)\s*\]\("
    )
    bad = _violations(md_files, vague)
    assert not bad, "Vague link text (bad for screenreaders):\n" + "\n".join(bad)


def test_bold_markers_balanced_per_line(md_files):
    """** must open and close on the same line (no odd counts)."""
    bad = []
    for name, path in md_files.items():
        in_code = False
        for i, line in enumerate(_read(path), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if not in_code and line.count("**") % 2 == 1:
                bad.append(f"{name}:{i}: {line.strip()[:60]}")
    assert not bad, "Unbalanced ** markers:\n" + "\n".join(bad)


def test_ordered_lists_are_sequential(md_files):
    """Within one list block, numbers must count up (1. 2. 3., not 1. 1. 4.)."""
    bad = []
    for name, path in md_files.items():
        block: list[tuple[int, int]] = []  # (number, line_no)
        for i, line in enumerate([*_read(path), ""], 1):
            m = re.match(r"^(\s*)(\d+)[.)]\s", line)
            if m:
                block.append((int(m.group(2)), i))
                continue
            if len(block) >= 2:
                nums = [b[0] for b in block]
                if nums != list(range(nums[0], nums[0] + len(nums))):
                    bad.append(f"{name}: lines {[b[1] for b in block]}: {nums}")
            block = []
    assert not bad, "Non-sequential ordered list numbering:\n" + "\n".join(bad)


def test_no_mojibake(md_files):
    """No encoding artifacts (U+FFFD, double-encoded UTF-8) may appear."""
    bad = _violations(md_files, r"\ufffd|Ã[¤±©¼]|Â\s")
    assert not bad, "Encoding artifacts (mojibake):\n" + "\n".join(bad)


def test_no_bare_urls(md_files):
    """URLs must be links, code spans, or code blocks — not bare text."""
    bad = []
    for name, path in _tutorial_pages(md_files).items():
        in_code = False
        for i, line in enumerate(_read(path), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            s = re.sub(r"\[[^\]]*\]\([^)]*\)", "", line)  # md links
            s = re.sub(r"`[^`]*`", "", s)  # code spans
            s = re.sub(r"<[^>]+>", "", s)  # html/autolinks
            if re.search(r"https?://", s):
                bad.append(f"{name}:{i}: {line.strip()[:60]}")
    assert not bad, "Bare URLs (wrap in code spans/links):\n" + "\n".join(bad)


def test_no_duplicate_headings_within_page(md_files):
    """Non-step headings must be unique per page (Step N may repeat across parts)."""
    bad = []
    for name, path in _tutorial_pages(md_files).items():
        seen: dict[str, int] = {}
        for i, line in enumerate(_read(path), 1):
            m = re.match(r"^(#{1,4})\s+(.+?)\s*$", line)
            if not m or line.startswith("# ") or re.match(r"###\s+(?:Step|Schritt)\b", line, re.I):
                continue
            heading = m.group(2).lower()
            if heading in seen:
                bad.append(f"{name}:{i}: '{heading}' duplicates line {seen[heading]}")
            seen[heading] = i
    assert not bad, "Duplicate headings within a page:\n" + "\n".join(bad)


def test_no_empty_table_cells_beyond_first_column(md_files):
    """Empty first cells are tested elsewhere; here: no other cell may be empty."""
    bad = []
    for name, path in md_files.items():
        for i, line in enumerate(_read(path), 1):
            if not re.match(r"^\s*\|", line) or re.match(r"^\s*\|[-\s|:]+\|\s*$", line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            empties = [j for j, c in enumerate(cells[1:], 2) if c == ""]
            if empties:
                bad.append(f"{name}:{i}: empty cells at cols {empties}")
    assert not bad, "Empty table cells:\n" + "\n".join(bad)


def test_no_raw_html_formatting_tags(md_files):
    """Use Markdown (**bold**, _italic_) not <b>/<i>/<u>/<font>/<br>."""
    bad = _violations(_tutorial_pages(md_files), r"<(?:b|i|u|font|div|span|br)\b", re.I)
    assert not bad, "Raw HTML formatting tags:\n" + "\n".join(bad)


def test_no_three_consecutive_blank_lines(md_files):
    bad = []
    for name, path in md_files.items():
        run = 0
        for i, line in enumerate(_read(path), 1):
            run = run + 1 if not line.strip() else 0
            if run >= 3:
                bad.append(f"{name}:{i}")
    assert not bad, "3+ consecutive blank lines:\n" + "\n".join(bad)


@pytest.mark.parametrize("version", ["version-5", "version-6"])
def test_en_tutorial_pages_have_page_seo(version):
    """Every EN tutorial page must set PageSEO (title/description/keywords)."""
    en_dir = SITE / "versioned_docs" / version
    missing = sorted(
        p.name
        for p in en_dir.glob("sogo-*.md")
        if "spec" not in p.name and "gaps" not in p.name and "PageSEO" not in p.read_text()
    )
    assert not missing, f"{version}: EN tutorial pages missing PageSEO:\n" + "\n".join(missing)


# ---------------------------------------------------------------------------
# rendering & style invariants (round-3 sweep)
# ---------------------------------------------------------------------------


def test_no_punctuation_ending_headings(md_files):
    bad = _violations(md_files, r"^#{1,6}\s+.*[:.;!?,]\s*$", re.M)
    assert not bad, "Headings should not end with punctuation:\n" + "\n".join(bad)


@pytest.mark.parametrize("version", ["version-5", "version-6"])
def test_sidebar_label_parity(version):
    """EN and DE pages must both set (or both omit) sidebar_label."""
    en_dir = SITE / "versioned_docs" / version
    de_dir = SITE / "i18n" / "de" / "docusaurus-plugin-content-docs" / version
    bad = []
    for p in en_dir.glob("sogo-*.md"):
        if "spec" in p.name or "gaps" in p.name:
            continue
        de = de_dir / p.name
        if not de.exists():
            continue

        def _has_label(f: Path) -> bool:
            return bool(re.search(r"^sidebar_label:", f.read_text(encoding="utf-8"), re.M))

        if _has_label(p) != _has_label(de):
            bad.append(
                f"{p.name}: EN={'yes' if _has_label(p) else 'no'}"
                f" DE={'yes' if _has_label(de) else 'no'}"
            )
    assert not bad, "sidebar_label presence mismatch EN vs DE:\n" + "\n".join(bad)


@pytest.mark.parametrize("version", ["version-5", "version-6"])
def test_de_pages_have_no_page_seo(version):
    """DE pages use front matter only — an imported PageSEO means an EN copy-paste leak."""
    de_dir = SITE / "i18n" / "de" / "docusaurus-plugin-content-docs" / version
    leaked = sorted(
        p.name
        for p in de_dir.glob("sogo-*.md")
        if "spec" not in p.name and "gaps" not in p.name and "PageSEO" in p.read_text()
    )
    assert not leaked, f"{version}: PageSEO leaked into DE pages:\n" + "\n".join(leaked)


def test_no_empty_admonitions(md_files):
    bad = []
    for name, path in md_files.items():
        lines = _read(path)
        for i in range(len(lines) - 1):
            if re.match(r"^:::\w", lines[i]) and lines[i + 1].strip() == ":::":
                bad.append(f"{name}:{i + 1}")
    assert not bad, "Empty admonitions:\n" + "\n".join(bad)


def test_tables_have_blank_line_before(md_files):
    """A table header directly after prose breaks MDX rendering."""
    bad = []
    for name, path in md_files.items():
        lines = _read(path)
        for i, line in enumerate(lines):
            if not re.match(r"^\s*\|[-\s|:]+\|\s*$", line) or i < 2:
                continue
            before_header = lines[i - 2]  # i-1 is the header row itself
            if (
                before_header.strip()
                and not before_header.strip().startswith(("|", "```", ":", "#", ">"))
                and not re.match(r"^\s*\d", before_header)
            ):
                bad.append(f"{name}:{i - 1}: after '{before_header.strip()[:40]}'")
    assert not bad, "Table without blank line before:\n" + "\n".join(bad)


def test_doc_links_use_relative_dot_slash(md_files):
    """Doc links must be ](./sogo-x.md) — without ./ Docusaurus resolves differently."""
    bad = _violations(md_files, r"\]\(sogo-[a-z-]+\.md")
    assert not bad, "Doc link missing ./ prefix:\n" + "\n".join(bad)


def test_no_weak_alt_text(md_files):
    """Alt text must be descriptive (>3 chars, not 'img'/'image'/'Bild'/...)."""
    weak = re.compile(
        r"!\[\s*(?:(.{1,3})|(img|bild|image|screenshot|foto|picture|grafik))\s*\]", re.I
    )
    bad = []
    for name, path in md_files.items():
        for i, line in enumerate(_read(path), 1):
            if weak.search(line):
                bad.append(f"{name}:{i}: {line.strip()[:50]}")
    assert not bad, "Weak image alt text:\n" + "\n".join(bad)


# ---------------------------------------------------------------------------
# round-4 sweep: translation-leak & whitespace invariants
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("version", ["version-5", "version-6"])
def test_no_german_leaking_into_en(version):
    """EN tutorial pages must not contain German UI instruction phrases."""
    de_phrase = re.compile(
        r"\b(?:Öffnen Sie|Klicken Sie|Wählen Sie|Geben Sie|Navigieren Sie|"
        r"Schritt für Schritt|zum|zur|Einstellungen öffnen)\b"
    )
    en_dir = SITE / "versioned_docs" / version
    bad = []
    for p in en_dir.glob("sogo-*.md"):
        if "spec" in p.name or "gaps" in p.name:
            continue
        in_code = False
        for i, line in enumerate(_read(p), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if not in_code and de_phrase.search(line):
                bad.append(f"{p.name}:{i}: {line.strip()[:60]}")
    assert not bad, f"{version}: German leaked into EN docs:\n" + "\n".join(bad)


def test_no_tab_characters(md_files):
    bad = _violations(md_files, r"\t")
    assert not bad, "Tab characters (break Markdown alignment):\n" + "\n".join(bad)


def test_consistent_list_indentation(md_files):
    """Nested list indentation should use one style per file (no mixed 2/3/5-space)."""
    bad = []
    for name, path in md_files.items():
        indents = {len(m.group(1)) for ln in _read(path) if (m := re.match(r"^( +)[*-]\s", ln))}
        if len(indents) > 2:  # one base + one nesting level is normal
            bad.append(f"{name}: indent widths {sorted(indents)}")
    assert not bad, "Mixed list indentation:\n" + "\n".join(bad)


def test_no_duplicate_links_on_index(md_files):
    """index.md must not link the same tutorial twice (duplicate card)."""
    bad = []
    for name, path in md_files.items():
        if path.name != "index.md":
            continue
        links = re.findall(r"\]\(\./([a-z-]+)\.md\)", path.read_text(encoding="utf-8"))
        dups = sorted({x for x in links if links.count(x) > 1})
        if dups:
            bad.append(f"{name}: {dups}")
    assert not bad, "Duplicate links on index page:\n" + "\n".join(bad)


def test_admonition_types_are_valid(md_files):
    """Only Docusaurus admonition types; a typo renders as literal text."""
    valid = {"note", "tip", "info", "caution", "danger", "warning", "important"}
    bad = []
    for name, path in md_files.items():
        for i, line in enumerate(_read(path), 1):
            m = re.match(r"^:::([A-Za-z]+)\b", line)
            if m and m.group(1).lower() not in valid:
                bad.append(f"{name}:{i}: :::{m.group(1)}")
    assert not bad, "Unknown admonition type:\n" + "\n".join(bad)


# ---------------------------------------------------------------------------
# Screenshot sanity: blank / error-page captures must never ship again
# (T5.1: vacation step-1 image showed SOGo's
#  "An error occurred during object publishing" page — nearly pure white,
#  almost no edges, almost no colors).

#: files that are legitimately near-empty (verified live captures), as
#: (site-relative dir, filename) — name-only would skip future copies
_BLANK_ALLOWED = {("versioned_docs/version-6", "logout.png")}


def _blank_metrics(png: Path):
    from PIL import Image, ImageFilter, ImageStat

    im = Image.open(png).convert("RGB")
    small = im.resize((800, 500))
    edges = small.convert("L").filter(ImageFilter.FIND_EDGES)
    px = list(edges.getdata())
    edge_ratio = sum(1 for v in px if v > 40) / len(px)
    n_colors = len(set(im.resize((64, 40)).getdata()))
    luma = ImageStat.Stat(im.convert("L")).mean[0]
    return edge_ratio, n_colors, luma


@pytest.mark.parametrize("doc_dir", DOC_DIRS, ids=lambda d: d.name + "-" + d.parent.name)
def test_screenshots_are_not_blank_or_error_pages(doc_dir):
    """A screenshot that is almost white with almost no content is either a
    failed capture (SOGo error page) or a blank placeholder — both must not
    ship. Calibrated: real UI screenshots have luma <= 232, >= 97 quantized
    colors and >= 1.5% edge pixels; error pages sit at luma ~248 / ~33 colors."""
    bad = []
    for png in sorted((doc_dir / "assets").glob("*.png")):
        if (str(doc_dir.relative_to(SITE)), png.name) in _BLANK_ALLOWED:
            continue
        edge_ratio, n_colors, luma = _blank_metrics(png)
        if (luma > 238 and n_colors < 60) or (edge_ratio < 0.0125 and n_colors < 45):
            bad.append(f"{png.name}: luma={luma:.0f} colors={n_colors} edges={edge_ratio:.1%}")
    assert not bad, (
        "Blank/error-page screenshot(s) detected (failed captures must be "
        "re-taken or removed, never published):\n" + "\n".join(bad)
    )


# ---------------------------------------------------------------------------
# Image provenance: wrong-version screenshots must never ship again
# (the SOGo 5 logout doc showed SOGo 6's login page with a stale mockup arrow
#  pointing at the layout switch — site/image-provenance.json records, per
#  asset file, whether it is a SOGo 5 mockup, a SOGo 6 live capture, or
#  deliberately shared between versions)

_PROVENANCE = json.loads((SITE / "image-provenance.json").read_text(encoding="utf-8"))["assets"]


def test_provenance_manifest_is_current():
    """Every asset file has a provenance entry and every entry points at a
    real file — a new image without provenance cannot slip into a doc, and
    deleted files must not leave stale entries behind."""
    on_disk = {str(p.relative_to(SITE)) for d in DOC_DIRS for p in (d / "assets").glob("*.png")}
    listed = set(_PROVENANCE)
    missing = sorted(on_disk - listed)
    stale = sorted(listed - on_disk)
    assert not missing, (
        "images without provenance entry — classify them in "
        "site/image-provenance.json (kind: sogo5-mockup | sogo6-live | shared):\n"
        + "\n".join(missing)
    )
    assert not stale, "stale provenance entries (file deleted):\n" + "\n".join(stale)


@pytest.mark.parametrize("doc_dir", DOC_DIRS, ids=lambda d: d.name + "-" + d.parent.name)
def test_image_version_discipline(doc_dir):
    """v5 docs must not show SOGo 6 captures and v6 docs must not show SOGo 5
    mockups — the exact mixup behind the wrong logout screenshot. ``shared``
    assets (settings pages unchanged between versions, T5.1/T5.2 decision) are
    allowed for both; v6 references to SOGo 5 mockups are accepted only as
    flagged T5.3 waivers."""
    is_v5 = str(doc_dir).endswith("version-5")
    rel_dir = str(doc_dir.relative_to(SITE))
    bad = []
    for md in sorted(doc_dir.glob("*.md")):
        for name in re.findall(r"\]\(\./assets/([\w.-]+\.png)\)", md.read_text(encoding="utf-8")):
            entry = _PROVENANCE[f"{rel_dir}/assets/{name}"]
            kind = entry["kind"]
            if kind == "shared":
                continue
            if is_v5 and kind in ("sogo5-mockup", "sogo5-live"):
                continue
            if not is_v5 and kind == "sogo6-live":
                continue
            if (
                not is_v5
                and kind == "sogo5-mockup"
                and entry.get("waived")
                and "T5.3" in entry.get("note", "")
            ):
                continue  # known backlog, tracked in the manifest
            bad.append(f"{md.name}: {name} (kind={kind})")
    assert not bad, (
        "Wrong-version screenshot(s) wired into a doc — see "
        "site/image-provenance.json:\n" + "\n".join(bad)
    )


# ---------------------------------------------------------------------------
# SOGo 6 logout affordance: the live capture pipeline proves logout lives in
# the avatar menu ("Click your avatar and select Logout",
# capture/run_screenshot_captures.py:record_logout). The power icon is the
# SOGo 5 toolbar affordance and must not be claimed for SOGo 6 docs again.

_V6_FORBIDDEN_LOGOUT_CLAIMS = {
    "power icon": "SOGo 6 logout is the avatar menu, not a power icon",
    "Ein/Aus-Symbol": "SOGo 6 logout ist das Avatar-Menü, kein Ein/Aus-Symbol",
}


@pytest.mark.parametrize(
    "doc_dir",
    [d for d in DOC_DIRS if "version-6" in str(d)],
    ids=lambda d: "v6-" + ("de" if "i18n" in str(d) else "en"),
)
def test_sogo6_docs_do_not_claim_power_icon_logout(doc_dir):
    bad = [
        f"{md.name}: '{phrase}'"
        for md in sorted(doc_dir.glob("*.md"))
        for phrase in _V6_FORBIDDEN_LOGOUT_CLAIMS
        if phrase in md.read_text(encoding="utf-8")
    ]
    assert not bad, "SOGo 6 docs claim the SOGo 5 logout affordance:\n" + "\n".join(bad)
