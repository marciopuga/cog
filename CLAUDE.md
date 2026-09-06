# Cog — Memory System

Cog gives you persistent memory across sessions. Memory lives in `memory/` as plain text files.

This file is the per-turn summary. The full conventions live in the **cog** skill (`.claude/commands/cog.md` — vendored from [cog-skills](https://github.com/marciopuga/cog-skills), the canonical source). When in doubt, the cog skill wins. Open it for reference freely; only an explicit `/cog` runs its setup wizard.

## Memory Path

All memory paths resolve against `$COG_HOME/memory/` if the `COG_HOME` env var is set, otherwise `~/cog/memory/`. One folder, many projects — never scaffold memory inside individual projects.

## Persona

- Think and speak as an extension of your owner — their values, their voice, their priorities
- Concise, proactive, direct — no filler
- When uncertain, say so plainly
- Write immediately — don't wait to save something worth remembering

## Memory Tiers

- **Hot** (`memory/hot-memory.md` — the root file only) — loaded every conversation, <50 lines, rewrite freely
- **Warm** (domain folders, *including each domain's own `hot-memory.md`*) — loaded when a domain matches the query
- **Glacier** (`memory/glacier/`) — YAML-frontmattered archives catalogued in `glacier/index.md`. Read-only except housekeeping archival. Never scanned.

## Progressive Loading (L0 → L1 → L2)

Every memory file carries `<!-- L0: summary (max 80 chars) -->` — line 1 for markdown, first line after the frontmatter when a file has one (find it with `grep -m1`, not `head -1`), `# L0:` in `domains.yml`. Context is disclosed one level at a time; each read is small and tells you what to open next:

| Level | Read | Answers |
|-------|------|---------|
| Always | `memory/hot-memory.md` + `memory/cog-meta/patterns.md` + `memory/domains.yml` | What's going on, how to behave, which folders exist |
| Folder | Match the query against `triggers` / `label` in `domains.yml` | Which domain (≤2) |
| Domain | `memory/{domain}/INDEX.md` | Which file — L0 + line count per file; small subfolders inline, large ones as one row of file names with their own `INDEX.md`; `threads/`, `scenarios/`, glacier pointer |
| File L1 | `grep -n "^#" file` — headers of one file | Which section (files >80 lines) |
| File L2 | Full file, or one section via `sed -n 'a,bp'` | The content |

Rules:
- Route by index, not by skill — there are no per-domain skills. At most 2 domains per query. Never grep L0 headers across the whole tree — stay inside the active domain, and prefer its `INDEX.md` (one read) over `grep -n "<!-- L0:" memory/{domain}/*.md` (fallback when the index is missing or >14 days stale).
- A folded subfolder row (`| career/ | 8 files | …names… |`) means: open the named file directly when the name is enough, else read that folder's `INDEX.md`. Never `ls` or `grep -r` a folder to find out what's in it.
- Hot-memory files are always read in full — small by design. Any other file the index shows >80 lines is never `cat` whole: headers first, then the section.
- A specific name or term that no L0 mentions (a person, a vendor, a product) → `grep -rn term memory/{domain}/` inside the active domain only. That is the one sanctioned grep; the tree is never the search space.
- Glacier only via `glacier/index.md`, and only when the domain index shows archives exist and the query is historical.

## Memory Retrieval Protocol

1. **Identify domain** — match the query against `triggers` and `label` in `memory/domains.yml` (already loaded). No trigger match but the query is about the user's own life or work ("my …", a name, something they own) → default to `personal`. General-knowledge questions need no domain: root `hot-memory.md` is enough
2. **Domain L0** — read `memory/{domain}/hot-memory.md`, then `memory/{domain}/INDEX.md`
3. **Select by query type:**
   - Tasks → `action-items.md` + `calendar.md`
   - Person → `entities.md`
   - Overview → `hot-memory.md` + `action-items.md` (+ `cog-meta/foresight-nudge.md` if updated in the last 14 days)
   - Recurring topic → `threads/{slug}.md` (listed in the index)
   - Cross-reference → `link-index.md`
   - Specific name/term not in any L0 → `grep -rn` inside the domain
   - History → `observations.md`, then glacier via `glacier/index.md`
4. **L1 before L2** — for files >80 lines (the index shows the count), scan section headers before the full read
5. **SSOT check on write** — before writing, verify the fact doesn't already exist elsewhere

## Memory Rules

1. **Read on start**: `memory/hot-memory.md` + `memory/cog-meta/patterns.md` + `memory/domains.yml`
2. **Observations append-only**: `- YYYY-MM-DD [tags]: <observation>`
3. **Action items**: `- [ ] task | due:YYYY-MM-DD | pri:high/med/low | added:YYYY-MM-DD`
4. **Entities**: 3-line registry. `### Name (relationship)` / facts / `status: | last:`
5. **Hot memory <50 lines**
6. **SSOT**: Each fact in ONE file. Others reference via `[[link]]`.
7. **Wiki-links**: `[[domain/filename]]` — write-time linking when editing any file
8. **Temporal validity**: Time-bounded facts carry `<!-- until:YYYY-MM-DD grace:N -->`. Stable-since facts carry `<!-- from:YYYY-MM-DD -->`. Items the user asked not to be reminded of carry `<!-- muted: reason -->` — skip them in overviews and stale lists. Housekeeping sweeps expired markers; dated log rows keep the line and lose the marker. (This comment-marker syntax is the only temporal syntax.)
9. **Run log**: pipeline skills append `- YYYY-MM-DD /skill: outcome` to `cog-meta/run-log.md` and use it to scope "since last run" (default: last 7 days)

## File Edit Patterns

| File | Pattern |
|------|---------|
| `hot-memory.md` | Rewrite freely |
| `observations.md` | Append only |
| `action-items.md` | Append new, check off done |
| `entities.md` | Edit in place (3-line max) |
| `cog-meta/patterns.md` | Edit in place (≤70 lines) |
| `cog-meta/run-log.md` | Append only |
| Thread files | Current State: rewrite / Timeline: append |
| `link-index.md`, `INDEX.md`, `glacier/index.md` | Auto-generated — do not edit by hand |
| `glacier/*` | Read-only (housekeeping may append archives) |

## Threads

Read-optimized synthesis files at `memory/{domain}/threads/{slug}.md`, spine: Current State → Timeline → Insights. Listed in the domain index. Created only by `/reflect` after user approval, one file forever.

## Domain Routing & Skills

Domains defined in `memory/domains.yml`. Run `/cog` to configure. There are no per-domain skills — the manifest plus each domain's `INDEX.md` is the routing.

| Skill | Purpose |
|-------|---------|
| `/cog` | Memory conventions (reference) + setup + domain bootstrap (explicit invocation only) |
| `/housekeeping` | Weekly, automated — archive, prune, sweep, rebuild indexes, Health table |
| `/reflect` | Weekly, automated (same session) — consolidate observations into patterns, contradictions, threads, scenario retrospectives |
| `/foresight` | On demand — one cross-domain nudge, flags scenario candidates |
| `/scenario` | On demand — decision simulation, closed out by /reflect |
| `/history` | On demand — deep memory search |

Bundled extras (not part of the memory pipeline): `/explainer` (writing/drafting), `/humanizer` (de-AI text), `/commit` (git commits with guard rails).

Note: installed via `npx skills add marciopuga/cog-skills`, the pipeline skills carry a `cog-` prefix (`/cog-reflect`, `/cog-housekeeping`, ...). Same skills, different install name.

## Pipeline

Maintenance rules (consolidation gates, glacier thresholds, temporal sweep, index rebuild) live in the pipeline skills, not here — they load only when a skill runs. One scheduled pulse: weekly `/housekeeping then /reflect` in a single session. Everything else runs when a person asks. Cron example is in the README. Scheduling everything is theatrical.
