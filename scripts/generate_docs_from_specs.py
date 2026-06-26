#!/usr/bin/env python3
"""
Generate Docusaurus MDX documentation pages from OpenSpec specification files.

Reads spec files from openspec/specs/<domain>/spec.md and produces
supplementary spec-based guide pages in site/docs/ with frontmatter,
PageSEO component, step-by-step instructions, and scenario reference tables.

Usage:
    python3 scripts/generate_docs_from_specs.py

Requirements: Python 3.8+ standard library only (re, pathlib, sys).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = REPO_ROOT / "openspec" / "specs"
OUTPUT_DIR = REPO_ROOT / "site" / "docs"

# Spec domain -> output filename mapping.
# Each spec file lives at: openspec/specs/<domain>/spec.md
# Capture-pipeline is internal tooling — skipped.
SPEC_TARGETS: dict[str, str] = {
    "auth-session": "sogo-spec-auth-session.md",
    "calendar": "sogo-spec-calendar.md",
    "mail": "sogo-spec-mail.md",
    "contacts": "sogo-spec-contacts.md",
    "preferences": "sogo-spec-preferences.md",
}

SEO_KEYWORDS: dict[str, str] = {
    "auth-session": "SOGo 5, login, logout, session, authentication, spec",
    "calendar": "SOGo 5, calendar, events, recurring, sharing, iCal, free/busy, spec",
    "mail": "SOGo 5, mail, email, compose, reply, forward, folders, filters, signatures, spec",
    "contacts": "SOGo 5, contacts, address book, vCard, import, export, spec",
    "preferences": "SOGo 5, preferences, settings, password, vacation, global search, spec",
}

# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def _normalize_shall(text: str) -> str:
    """Replace SHALL/SHOULD/MAY with present-tense forms for documentation."""
    text = text.replace(" SHALL ", " will ")
    text = text.replace(" SHALL.", ".")
    text = text.replace(" SHALL,", ",")
    text = text.replace(" SHOULD ", " should ")
    text = text.replace(" SHOULD.", ".")
    text = text.replace(" MAY ", " may ")
    text = text.replace(" MAY.", ".")
    return text


def _make_title(domain: str) -> str:
    """Generate an H1 title from the domain name."""
    return f"{domain.replace('-', ' ').title()} — Spec-Based Guide"


def _make_description(purpose: str) -> str:
    """Truncate purpose text to a ~150-char description."""
    flat = purpose.replace("\n", " ").strip()
    if len(flat) > 155:
        flat = flat[:152].rstrip() + "..."
    return flat


def _make_sidebar_label(domain: str) -> str:
    return f"{domain.replace('-', ' ').title()} Specification Guide"


def _step_title_from_when(when: str) -> str:
    """Derive an imperative step title from a WHEN clause."""
    action = when.strip().rstrip(".")
    action = re.sub(
        r"^the\s+(?:user|capture pipeline|pipeline|login function|recorder)\s+",
        "",
        action,
        flags=re.IGNORECASE,
    )
    if not action:
        return when.strip().rstrip(".")

    # Convert 3rd-person singular verbs to imperative by stripping
    # trailing "s" (or "ies" -> "y" for words like "carries").
    # Regex allows hyphens (e.g. "double-clicks" -> "double-click")
    # and handles end-of-string with no trailing space.

    # Step 1: "ies" -> "y" (e.g. "carries" -> "carry")
    action = re.sub(
        r"^([A-Za-z-]+)ies(?:\s|$)",
        lambda m: m.group(1)[:-1] + "y ",
        action,
    )

    # Step 2: Strip trailing "s" for most verbs
    # This turns "clicks" -> "click", "navigates" -> "navigate",
    # "starts" -> "start", but also "focuses" -> "focuse"
    action = re.sub(
        r"^([A-Za-z-]+)s(?:\s|$)",
        lambda m: m.group(1) + " ",
        action,
    )

    # Step 3: Correct known over-stripping from the "s" rule.
    # "focuses" -> Step 2 produces "focuse" -> correct to "focus"
    action = re.sub(
        r"^focuse(?:\s|$)",
        lambda m: "focus ",
        action,
    )

    return (action[0].upper() + action[1:]).strip()


def _step_description_from_when(when: str) -> str:
    """Generate a natural prose description of the step action."""
    desc = when.strip().rstrip(".")
    if re.match(r"^the\s+", desc, re.IGNORECASE):
        # If it starts with "the", it's already phrased as a statement
        desc = desc[0].upper() + desc[1:]
    else:
        desc = "The user " + desc[0].lower() + desc[1:]
    desc = _normalize_shall(desc)
    # Tweak pipeline-internal phrasing to be more user-facing
    desc = re.sub(
        r"(?i)\bthe capture pipeline\b",
        "you",
        desc,
    )
    desc = re.sub(
        r"(?i)\bthe login function\b",
        "the system",
        desc,
    )
    desc = re.sub(
        r"(?i)\bthe (pipeline|recorder)\b",
        "the system",
        desc,
    )
    desc = re.sub(r"(?i)^The user the (pipeline|recorder|system)\s+", "The system ", desc)
    # Ensure first character is uppercase
    desc = desc[0:1].upper() + desc[1:]
    # Clean up doubling from the replacements
    desc = desc.replace("The user you will", "You will")
    desc = desc.replace("The user you ", "You ")
    desc = re.sub(r"\s+", " ", desc).strip()
    return desc


_INTERNAL_GIVEN_PHRASES = (
    "known to produce blank",
    "workflow is being recorded",
    "workflow is known",
    "has been extracted",
    "has occurred in a dedicated",
    "with video recording",
    "no environment variables are set",
)


def _is_user_prerequisite(given: str) -> bool:
    """Return True if a GIVEN clause describes a real user-facing precondition."""
    lower = given.lower()
    return not any(phrase in lower for phrase in _INTERNAL_GIVEN_PHRASES)


# ---------------------------------------------------------------------------
# Spec file parser
# ---------------------------------------------------------------------------


def parse_spec(filepath: Path) -> dict[str, Any]:
    """Parse a single spec.md file and return a structured dictionary.

    Returns:
        {
            "domain": str,
            "source_files": str,
            "last_updated": str,
            "purpose": str,
            "requirements": [
                {
                    "name": str,
                    "prose": str,
                    "scenarios": [
                        {
                            "name": str,
                            "given": str,
                            "when": str,
                            "thens": [str],
                            "ands": [str],
                        }
                    ],
                }
            ],
            "technical_notes": { str: str },  # key -> value
        }
    """
    content = filepath.read_text(encoding="utf-8")

    # --- domain ---
    domain_m = re.search(r"^#\s+(\S+)\s+Specification", content, re.MULTILINE)
    domain = domain_m.group(1) if domain_m else filepath.parent.name

    # --- metadata blockquote ---
    source_files = ""
    last_updated = ""
    m = re.search(r"^>\s*Source files:\s*(.+)$", content, re.MULTILINE)
    if m:
        source_files = m.group(1).strip()
    m = re.search(r"^>\s*Last updated:\s*(.+)$", content, re.MULTILINE)
    if m:
        last_updated = m.group(1).strip()

    # --- Purpose (content between ## Purpose and next ## heading) ---
    purpose = ""
    pm = re.search(r"## Purpose\n(.+?)\n## ", content, re.DOTALL)
    if pm:
        purpose = pm.group(1).strip()

    # --- split into requirement blocks ---
    # The content between ## Requirements and ## Technical Notes (or EOF)
    req_zone_m = re.search(
        r"## Requirements\n(.+?)(?=\n## Technical Notes|\Z)",
        content,
        re.DOTALL,
    )
    req_zone = req_zone_m.group(1) if req_zone_m else ""

    # Split on "### Requirement:" headings
    raw_reqs = re.split(r"\n(?=### Requirement: )", req_zone)
    requirements: list[dict[str, Any]] = []

    for raw in raw_reqs:
        raw = raw.strip()
        if not raw:
            continue

        name_m = re.search(r"^### Requirement:\s*(.+)$", raw, re.MULTILINE)
        if not name_m:
            continue
        req_name = name_m.group(1).strip()

        # Prose between heading line and first h4 (or end)
        prose_m = re.search(
            r"### Requirement: .+?\n\n(.+?)(?=\n\n#### Scenario: |\Z)",
            raw,
            re.DOTALL,
        )
        req_prose = prose_m.group(1).strip() if prose_m else ""

        # --- scenarios ---
        raw_scenarios = re.split(r"\n(?=#### Scenario: )", raw)
        scenarios: list[dict[str, Any]] = []

        for sraw in raw_scenarios:
            sraw = sraw.strip()
            if not sraw.startswith("#### Scenario:"):
                continue
            sc_name_m = re.search(r"^#### Scenario:\s*(.+)$", sraw, re.MULTILINE)
            if not sc_name_m:
                continue
            sc_name = sc_name_m.group(1).strip()

            given = ""
            when = ""
            thens: list[str] = []
            ands: list[str] = []

            # Parse line-by-line inside the scenario body
            for line in sraw.splitlines():
                stripped = line.strip()
                # Match bullet-pointed GIVEN / WHEN / THEN / AND
                m2 = re.match(r"^-\s+\*\*(GIVEN|WHEN|THEN|AND)\*\*\s+(.+)", stripped)
                if not m2:
                    continue
                keyword = m2.group(1)
                value = m2.group(2).strip()

                if keyword == "GIVEN" and not given:
                    given = value
                elif keyword == "WHEN" and not when:
                    when = value
                elif keyword == "THEN":
                    thens.append(value)
                elif keyword == "AND":
                    ands.append(value)

            scenarios.append(
                {
                    "name": sc_name,
                    "given": given,
                    "when": when,
                    "thens": thens,
                    "ands": ands,
                }
            )

        requirements.append({"name": req_name, "prose": req_prose, "scenarios": scenarios})

    # --- Technical Notes ---
    technical_notes: dict[str, str] = {}
    tn_m = re.search(r"## Technical Notes\n(.+)", content, re.DOTALL)
    if tn_m:
        tn_text = tn_m.group(1).strip()
        for item in re.finditer(r"^-\s+\*\*([^*]+)\*\*:\s*(.+)", tn_text, re.MULTILINE):
            key = item.group(1).strip()
            val = item.group(2).strip()
            technical_notes[key] = val

    return {
        "domain": domain,
        "source_files": source_files,
        "last_updated": last_updated,
        "purpose": purpose,
        "requirements": requirements,
        "technical_notes": technical_notes,
    }


# ---------------------------------------------------------------------------
# Document generator
# ---------------------------------------------------------------------------

_DOMAIN_DISPLAY_NAMES = {
    "auth-session": "SOGo Authentication and Sessions",
    "calendar": "SOGo Calendar",
    "mail": "SOGo Mail",
    "contacts": "SOGo Contacts",
    "preferences": "SOGo Preferences",
}


def _domain_display(domain: str) -> str:
    return _DOMAIN_DISPLAY_NAMES.get(domain, domain.replace("-", " ").title())


_DOMAIN_DEPENDENCY_LINKS = {
    "auth-session": "sogo-spec-auth-session",
    "capture-pipeline": "capture-pipeline",
}


# Deps that map to no generated doc — skip instead of linking to /dev/null.
_SKIP_DEP_KEYS = frozenset(
    {
        "playwright",
        "capture-pipeline",
        "capture-pipeline-domain",
        "capture-pipeline-domain-workflowrecorder",
    }
)


def _dep_link(dep_name: str) -> str | None:
    """Map a dependency name to a doc link path, or None if no doc exists."""
    key = dep_name.lower().strip().replace(" ", "-").replace("(", "").replace(")", "")
    if key in _SKIP_DEP_KEYS:
        return None
    known = _DOMAIN_DEPENDENCY_LINKS.get(key)
    if known:
        return known
    for domain, slug in SPEC_TARGETS.items():
        if domain in key:
            return slug.replace(".md", "")
    return None


def generate_doc(spec: dict[str, Any]) -> str:
    """Render a parsed spec into a complete MDX document string."""
    domain = spec["domain"]
    purpose = spec["purpose"]
    requirements = spec["requirements"]
    tn = spec["technical_notes"]

    display = _domain_display(domain)
    title = _make_title(domain)
    description = _make_description(purpose)
    sidebar_label = _make_sidebar_label(domain)
    keywords = SEO_KEYWORDS.get(domain, f"SOGo 5, spec, {domain}")

    lines: list[str] = []

    lines.append("---")
    lines.append(f'title: "{title}"')
    lines.append(f'description: "{description}"')
    lines.append(f'sidebar_label: "{sidebar_label}"')
    lines.append("---")
    lines.append("")

    lines.append("import PageSEO from '@site/src/components/PageSEO';")
    lines.append("")
    lines.append(f'<PageSEO title="{title}" description="{description}" keywords="{keywords}" />')
    lines.append("")

    lines.append(f"# {display}")
    lines.append("")

    purpose_paragraphs = purpose.split("\n\n")
    for para in purpose_paragraphs[:3]:
        lines.append(para.strip())
        lines.append("")

    all_givens: list[str] = []
    seen_givens: set[str] = set()
    for req in requirements:
        for sc in req["scenarios"]:
            g = sc["given"]
            if g and g not in seen_givens and _is_user_prerequisite(g):
                seen_givens.add(g)
                all_givens.append(g)

    if all_givens:
        lines.append("## Prerequisites")
        lines.append("")
        for g in all_givens:
            item = g[0].upper() + g[1:] if g else g
            item = re.sub(r"^An?\s+", "", item)
            lines.append(f"- {item}")
        has_auth = any("authenticated" in g.lower() for g in all_givens)
        if not has_auth:
            lines.append("- You are logged into SOGo 5")
        lines.append("")

    lines.append("## Step-by-Step Instructions")
    lines.append("")

    for _req_idx, req in enumerate(requirements):
        req_name = req["name"]
        req_prose = req["prose"]
        scenarios = req["scenarios"]

        lines.append(f"### {req_name}")
        lines.append("")

        if req_prose:
            prose = _normalize_shall(req_prose)
            lines.append(prose)
            lines.append("")

        for sc_idx, sc in enumerate(scenarios):
            step_num = sc_idx + 1
            step_title = _step_title_from_when(sc["when"])
            lines.append(f"#### Step {step_num}: {step_title}")
            lines.append("")

            if sc["when"]:
                when_desc = _step_description_from_when(sc["when"])
                lines.append(when_desc)
                lines.append("")

            # Expected results from THEN + AND
            all_results = sc["thens"] + sc["ands"]
            if all_results:
                lines.append("**Expected result:**")
                lines.append("")
                for r in all_results:
                    lines.append(f"- {_normalize_shall(r)}")
                lines.append("")

            # Check if this scenario is explicitly about blank capture handling.
            # Only flag scenarios whose name contains "blank" (e.g. "Blank capture
            # handling", "Blank capture fallback") — NOT generic scenarios that
            # happen to share a word with a workflow name in Known issues.
            is_known_blank = "blank" in sc["name"].lower()

            if is_known_blank:
                lines.append(":::note")
                lines.append(
                    "This workflow is known to produce blank captures "
                    "in the current pipeline. "
                    "The documentation describes the expected behavior textually."
                )
                lines.append(":::")
                lines.append("")

            if "annotation" in sc["name"].lower() or "highlight" in sc["name"].lower():
                lines.append(":::tip")
                lines.append(
                    "During recording the system automatically overlays step "
                    "headers and UI highlights (red circles, arrows) on each frame."
                )
                lines.append(":::")
                lines.append("")

    if tn.get("Known issues"):
        lines.append("## Troubleshooting")
        lines.append("")
        lines.append(tn["Known issues"])
        lines.append("")

    if tn.get("Dependencies"):
        dep_items = [
            d.strip() for d in tn["Dependencies"].replace(", ", ",").split(",") if d.strip()
        ]
        dep_links = []
        for dep in dep_items:
            slug = _dep_link(dep)
            if slug is None:
                continue
            title = dep.replace("-pipeline", "").replace("-", " ").title().strip()
            dep_links.append(f"- [{title}](./{slug})")
        if dep_links:
            lines.append("## Related Sections")
            lines.append("")
            lines.extend(dep_links)
            lines.append("")

    if tn.get("Implementation"):
        lines.append("## Implementation Reference")
        lines.append("")
        impl = tn["Implementation"]
        # If the value already contains backtick-wrapped items, preserve them
        # as-is instead of double-wrapping in a single backtick pair.
        if "`" in impl:
            lines.append(f"Source: {impl}")
        else:
            lines.append(f"Source: `{impl}`")
        lines.append("")

    lines.append("## Appendix: Scenario Reference")
    lines.append("")
    lines.append("| Scenario | Precondition | Action | Expected Result |")
    lines.append("|---|---|---|---|")
    for req in requirements:
        for sc in req["scenarios"]:
            given = (sc["given"] or "—").replace("|", "\\|")
            when = (sc["when"] or "—").replace("|", "\\|")
            thens = sc["thens"] or ["—"]
            then_text = "; ".join(_normalize_shall(t) for t in thens).replace("|", "\\|")
            lines.append(f"| {sc['name']} | {given} | {when} | {then_text} |")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Main entry point: parse all specs and write generated docs."""
    if not SPECS_DIR.is_dir():
        print(f"Error: specs directory not found: {SPECS_DIR}", file=sys.stderr)
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = 0
    skipped = 0
    errors = 0

    for domain, out_name in sorted(SPEC_TARGETS.items()):
        spec_path = SPECS_DIR / domain / "spec.md"
        if not spec_path.is_file():
            print(f"Warning: spec not found: {spec_path}", file=sys.stderr)
            skipped += 1
            continue

        try:
            spec = parse_spec(spec_path)
            doc = generate_doc(spec)
            out_path = OUTPUT_DIR / out_name
            out_path.write_text(doc, encoding="utf-8")
            print(f"  ✓ {domain:20s} → {out_name}")
            generated += 1
        except Exception as exc:
            print(f"  ✗ {domain:20s} error: {exc}", file=sys.stderr)
            errors += 1

    print()
    print(f"Done: {generated} generated, {skipped} skipped, {errors} errors")

    if errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
