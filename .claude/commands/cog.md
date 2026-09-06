---
name: cog
description: >
  Plain-text persistent memory system for AI agents. Conventions for L0 progressive
  loading, three-tier storage (hot/warm/glacier), single-source-of-truth, temporal
  validity, and wiki-links. Run /cog to bootstrap or reconfigure domains.
---

# Cog

A plain-text memory system that gives any AI agent persistent memory across sessions. Memory lives in a local folder as markdown files — observable, editable, git-trackable.

**One folder, many projects.** All reads and writes target a single global memory path. Don't create separate memory in each project — that fragments your context. One brain, used everywhere.

## Memory Path

Resolved in this order:

1. `$COG_HOME/memory/` — if the `COG_HOME` environment variable is set
2. `~/cog/memory/` — default fallback

If the resolved path doesn't exist, run `/cog` to bootstrap it.

## Three Tiers

| Tier | Where | Loaded | Size limit | Edit mode |
|------|-------|--------|-----------|-----------|
| **Hot** | `memory/hot-memory.md` | Every conversation | <50 lines | Rewrite freely |
| **Warm** | Domain files (incl. domain `hot-memory.md`) | When a domain matches the query | Per-file caps | File-specific |
| **Glacier** | `memory/glacier/` | On-demand (indexed) | Unlimited | Read-only (housekeeping archives) |

**Hot** = your desk. The root `memory/hot-memory.md` only — cross-domain current state, loaded every turn.
**Warm** = your filing cabinet. Domain files — *including each domain's own `hot-memory.md`* — loaded when a domain matches the query, not every turn. That's what keeps loading progressive.
**Glacier** = deep archive. Old observations, completed items. Indexed, searchable, never auto-loaded. Read-only, except when housekeeping appends archives and rebuilds `glacier/index.md`.

## L0 Headers (Progressive Context Loading)

Every memory file has a one-line L0 summary — a quick answer to "what would I find if I read this file?"

**Format:**
```
<!-- L0: summary here (max 80 chars) -->
```

**Placement:**
- Markdown files: line 1.
- Files with YAML frontmatter (glacier archives, scenarios, imported files that carry metadata): the first line after the closing `---`. Frontmatter can be long — locate an L0 with `grep -m1 "<!-- L0:"`, never `head -1`.
- YAML files (`domains.yml`): `# L0: summary` on line 1.

### The Loading Ladder

Context is disclosed one level at a time. Each level is one small read that tells you what to open next — never load a whole folder, or the whole tree, to find out what's in it.

| Level | Read | Answers | When |
|-------|------|---------|------|
| Always | `memory/hot-memory.md` + `memory/cog-meta/patterns.md` + `memory/domains.yml` | What's going on, how to behave, which folders exist | Every conversation |
| Folder | Match the query against each domain's `triggers` / `label` in `domains.yml` | Which domain folder (≤2) | Every query that touches memory |
| Domain | `memory/{domain}/INDEX.md` | Which file — L0 + line count per file; small subfolders inline, large ones as one row (file names) with their own `INDEX.md`; `threads/`, `scenarios/`, glacier pointer | A domain matched |
| File L0 | `<!-- L0: -->` of one file | Is this file relevant? | `INDEX.md` missing or stale (>14 days): `grep -n "<!-- L0:" memory/{domain}/*.md` |
| File L1 | `grep -n "^#" file` — headers of one file | Which section | File >80 lines (the index shows the count) |
| File L2 | Full file, or one section via `sed -n 'a,bp'` | The content | Relevance confirmed |

**Decision rules:**
1. Route by index, not by skill. There are no per-domain skills: `domains.yml` (always loaded, ~20 lines) says which folders exist and what wakes them; the matched folder's `INDEX.md` says which file. At most 2 domains per query, never a tree-wide scan.
2. `INDEX.md` is the L0 view of a domain: one read replaces N header reads. A folded subfolder row (`| career/ | 8 files | …names… |`) means: open the named file directly if the name is enough, else read that folder's own `INDEX.md` — one more small read, never `ls`/`grep` the folder. Grep L0 headers only when the index is missing or stale, and only inside that domain.
3. If L0 confirms relevance but the file is >80 lines, scan section headers (L1) before the full read. Never `cat` a file the index shows >80 lines — headers, then `sed -n` the section you need.
4. For files <80 lines, go straight to L2.
5. Hot-memory files are always L2 — they're small by design.
6. `grep -rn "<!-- L0:" memory/` is a human observability command. It is not a retrieval step — dumping every L0 in the tree defeats the ladder.
7. Glacier is never scanned. Read `glacier/index.md` only when the domain index shows archives exist and the query is historical.
8. A specific name or term that no L0 mentions (a person, a vendor, a product) → `grep -rn term memory/{domain}/` inside the active domain only. That is the one sanctioned grep; the tree is never the search space.
9. When a folded folder row is the likely target, open that folder's `INDEX.md` — not every sub-index in the domain.

## Directory Structure

Domains are defined in `memory/domains.yml` — the single source of truth for all memory domains.

```
memory/
  domains.yml                      # Domain manifest
  hot-memory.md                    # Cross-domain (loaded every turn)
  link-index.md                    # Backlink index (auto-generated)
  cog-meta/                        # System self-knowledge
    self-observations.md           # What worked/didn't — append-only
    patterns.md                    # Distilled interaction rules — edit in place
    action-items.md                # System tasks (housekeeping routes over-cap metrics, reflect routes ideas)
    run-log.md                     # Pipeline run log — append-only
    foresight-nudge.md             # Strategic nudge (foresight overwrites, on demand)
    scenarios/                     # Active decision scenarios
    INDEX.md                       # Per-domain L0 index (auto-generated)
  personal/                        # Default domain
    hot-memory.md
    observations.md
    action-items.md
    entities.md
    calendar.md
    health.md
    habits.md
    threads/                       # Synthesis files (created on promotion)
    INDEX.md                       # Per-domain L0 index (auto-generated)
  glacier/                         # Archived data by domain
    index.md                       # Glacier catalog (auto-generated)
```

## Memory Rules

1. **Read on start**: Always read `memory/hot-memory.md`, `memory/cog-meta/patterns.md`, and `memory/domains.yml` (the folder index — routing depends on it)
2. **Write immediately**: Don't wait to save something worth remembering
3. **Observations are append-only**: `- YYYY-MM-DD [tags]: <observation>` — never edit past entries
4. **Action items**: `- [ ] task | due:YYYY-MM-DD | pri:high/med/low | added:YYYY-MM-DD`
5. **Entities**: 3-line compact registry. `### Name (relationship)` / pipe-separated facts / `status: active | last: YYYY-MM-DD`
6. **Hot memory <50 lines**: Prune aggressively, detail goes in observations
7. **Single Source of Truth (SSOT)**: Each fact in ONE canonical file. Others reference via `[[link]]`.
8. **Temporal validity**: Time-bounded facts SHOULD carry an expiry marker (see below).

## Temporal Validity Markers

Facts with a natural expiry (upcoming events, temporary states, countdowns) should carry an inline marker:

```markdown
- HydroTap repair — chiller removed, reinstall in 1-2 weeks <!-- until:2026-06-20 grace:5 -->
- Leflunomide 3-month review Thu 18 Jun <!-- until:2026-06-18 grace:14 -->
- New job started at Acme <!-- from:2026-03-01 -->
```

**Marker types:**
- `<!-- until:YYYY-MM-DD -->` — expires on this date. Housekeeping archives after expiry.
- `<!-- until:YYYY-MM-DD grace:N -->` — expires N days after the `until` date (buffer for follow-up).
- `<!-- from:YYYY-MM-DD -->` — stable since this date. Never expires, documents when something became true.
- `<!-- muted: reason -->` — still open, but the user asked not to be reminded. Stale-item lists and overview briefings skip it; it never expires. Remove the marker when the user raises the item again.

**Rules:**
- Stable facts (DOB, role, relationships) need no marker
- Only mark facts that will become irrelevant after a date
- Housekeeping sweeps expired markers → moves to glacier or deletes. In append-only sections (observations, History, Timeline) it strips the marker and keeps the line.
- Only live-state files carry `until:` markers (hot-memory, action-items, entities, calendar, Current State sections). A dated log row is already scoped by its date — don't mark it.
- Use absolute dates, never computed counts ("since Jan 27" not "Day 42")
- Grace period = buffer for the fact to still matter after the event (e.g., a medical review result may take 2 weeks to act on)

## File Edit Patterns

| File | Edit mode |
|------|-----------|
| `hot-memory.md` | Rewrite freely |
| `observations.md` | Append only |
| `action-items.md` | Append new, check off done |
| `entities.md` | Edit in place (3-line max per entry) |
| `calendar.md` | Edit in place |
| `health.md` | Current State: rewrite / History: append |
| `habits.md` | Current State: rewrite / Patterns: append |
| Thread files | Current State: rewrite / Timeline: append |
| `cog-meta/patterns.md` | Edit in place (distill from observations) |
| `cog-meta/run-log.md` | Append only (pipeline skills log runs here) |
| `link-index.md`, `INDEX.md`, `glacier/index.md` | Auto-generated — do not edit by hand |
| `glacier/*` | Read-only (housekeeping may append archives) |

## Wiki-Links

Cross-reference files using `[[domain/filename]]` or `[[domain/filename#Section]]`.

- Path relative to `memory/`, no `.md` extension
- **Write-time linking**: When editing ANY file, add `[[links]]` to related files
- **Write-time back-linking**: When adding A→B, check if B benefits from pointing back to A
- Follow links when the linked topic is relevant — don't chase every link mechanically

## SSOT (Single Source of Truth)

Each fact lives in exactly ONE canonical file:

- People → `entities.md`
- Tasks → `action-items.md`
- Health → `health.md`
- Events → `calendar.md`
- Current state → `hot-memory.md` (pointers only, not source facts)
- Raw events → `observations.md`

When the same fact appears in two files: keep it in the canonical file, replace the duplicate with a `[[link]]`.

## Threads (Zettelkasten Layer)

Threads are read-optimized synthesis files for topics that appear across 3+ observations over 2+ weeks. One file per topic, consistent spine:

1. **Current State** — what's true now (rewrite freely)
2. **Timeline** — dated entries, append-only, full detail preserved
3. **Insights** — learnings, patterns, what's different this time

**Rules:**
- Threads live at `memory/{domain}/threads/{slug}.md` — kebab-case slug, L0 header on line 1
- Created by the reflect skill after the user approves a thread candidate — never auto-created
- One file forever — threads grow long, don't split
- Texture is the value — keep full detail, quotes, dates
- Fragments never move — threads reference them via wiki-links

## Memory Retrieval Protocol

When responding to any query, walk the loading ladder:

1. **Identify domain** — match the query against `triggers` and `label` in `memory/domains.yml` (already loaded). At most 2 domains. No trigger match but the query is about the user's own life or work ("my …", a name, something they own) → default to `personal`. General-knowledge questions need no domain: root `hot-memory.md` is all you need.
2. **Domain L0** — read `memory/{domain}/hot-memory.md`, then `memory/{domain}/INDEX.md`. Grep `<!-- L0:` headers inside the domain only if the index is missing or >14 days stale.
3. **Select by query type:**
   - Tasks → `action-items.md` + `calendar.md`
   - Person → `entities.md`
   - Overview → `hot-memory.md` + `action-items.md` (+ `cog-meta/foresight-nudge.md` if updated in the last 14 days)
   - Recurring topic → `threads/{slug}.md` (listed in the index)
   - Cross-reference → `link-index.md`
   - Specific name/term not in any L0 → `grep -rn` inside the domain (never the tree)
   - History → `observations.md`, then glacier via `glacier/index.md` if the index shows archives
4. **L1 before L2** — for files >80 lines (the index shows the count), scan headers first
5. **SSOT check on write** — before writing, verify the fact doesn't already exist elsewhere

## Run Log (Pipeline Bookkeeping)

`memory/cog-meta/run-log.md` records when each pipeline skill last ran. Append-only, one line per run:

```
- YYYY-MM-DD /skill-name: <one-line outcome>
```

- Every pipeline skill (housekeeping, reflect, foresight) appends a line at the end of its run
- "Since last run" scoping reads this file: find the last entry for the skill, scope work to files modified since that date. **If no entry exists, default to the last 7 days.**
- Housekeeping may trim entries older than 90 days

## Consolidation

Memory flows upward through the tiers:

```
observations (raw events, append-only)
    ↓ cluster 3+ on same theme
patterns (distilled rules, edit in place)
    ↓ most urgent/active
hot-memory (current state, rewrite freely)
```

Each layer up is smaller and more distilled. Nothing is deleted — abstracted and relocated.

## Glacier Archival

When files exceed limits, old data moves to `memory/glacier/{domain}/`:

- `observations.md` >50 entries → `glacier/{domain}/observations-{tag}.md`
- `action-items.md` >10 completed → `glacier/{domain}/action-items-done.md`
- Inactive entities (6+ months) → `glacier/{domain}/entities-inactive.md`

All glacier files have YAML frontmatter, followed by the L0 line:
```yaml
---
type: observations
domain: personal
tags: [health, habits]
date_range: 2024-01 to 2024-06
entries: 47
summary: Health and habit observations from early 2024
---
<!-- L0: Archived health and habit observations, Jan–Jun 2024 -->
```

## Domain Registry

`memory/domains.yml` is the single source of truth — and the folder-level L0: its `label` says what each folder holds, its `triggers` say when to open it. Line 1 is `# L0: ...` (YAML can't hold an HTML comment).

```yaml
# L0: Domain manifest — which memory folders exist and what activates them
domains:
  - id: personal
    path: personal
    type: personal
    label: "Family, health, calendar, day-to-day"
    triggers: [family, health, kids, calendar]
    files: [hot-memory, action-items, entities, observations, habits, health, calendar]
```

Domain types: `personal` (always one), `work`, `side-project`, `system` (cog-meta, auto-created).

## Patterns

Distilled rules from 3+ observations on the same theme. Timeless, actionable, no examples or dates.

- **Core** (`cog-meta/patterns.md`): universal rules, ≤70 lines. Loaded every turn.
- **Satellite** (`{domain}/patterns.md`): domain-specific, soft cap 30 lines. Loaded when that domain matches the query.

## Scheduling: Consolidated Pulses

When automating memory maintenance (cron, scheduled tasks, or manual batch runs), **run skills in the same session** rather than as separate isolated invocations.

### Why

Separate runs re-read all context from scratch and can't see what the prior skill modified. Hand-off files between runs drift and add complexity. Running housekeeping → reflect in one session means reflect sees what housekeeping just cleaned — no handoff needed.

### The Only Scheduled Pulse

| Pulse | Skills (in order) | Cadence | Rationale |
|-------|-------------------|---------|-----------|
| **Maintenance** | housekeeping → reflect | Weekly | Reflect sees cleaned state; promotions land in freshly-pruned files. Housekeeping's Health table is the system audit — no separate audit skill. |

Everything else is on demand: `foresight` when you want a read on where things are heading, `scenario` when a real decision is on the table, `history` when you need to reconstruct something.

### Anti-Pattern: Scheduled Everything

Running every skill on a timer is theatrical — it generates reports nobody reads and logs the same issues repeatedly without resolving them. One weekly pulse keeps memory clean; the judgment skills earn their context only when a person asks.

### Hand-Off Principle

Within a consolidated pulse, phases share context naturally (same conversation). Between runs (e.g., foresight reading reflect's patterns), the contract is through FILES — `patterns.md`, `action-items.md`, `self-observations.md`. No separate state files needed.

---

# Setup

This section runs **only** when the user explicitly invokes `/cog` or asks to set up, add, or reconfigure domains. If this skill was opened for reference — by the retrieval protocol or a pipeline skill — stop here. The conventions above are the whole payload; nothing below should execute.

## Phase 0: Verify Environment

1. **Resolve path** — check `$COG_HOME`. Cog home is `$COG_HOME` if set, otherwise `~/cog`. The memory root is `{cog_home}/memory/`.
2. **Check existence** — does the memory root exist?
   - **Yes** → skip to Phase 1 (or ask "Want to add more domains?")
   - **No** → create it: `mkdir -p "${COG_HOME:-$HOME/cog}/memory"`
3. **Set COG_HOME if non-default** — if the path is not `~/cog`, tell the user to add `export COG_HOME=/their/path` to their shell profile. Offer to do it for them.

## Phase 1: Discovery (Conversational)

Have a natural conversation to understand the user's domains. Ask about:

1. **Work** — "What do you do for work? Company name, role?" → becomes a `work` domain
2. **Side projects** — "Any side projects or ventures?" → each becomes a `side-project` domain
3. **Personal** — The `personal` domain is always created. Ask: "Anything specific you want to track? Health, hobbies, habits, kids?"
4. **Anything else** — "Any other areas you want persistent memory for?"

Keep it natural. 3-4 questions max. Use their answers to build the manifest.

### Domain Types

| Type | Meaning | Files |
|------|---------|-------|
| `personal` | Personal life (always one) | hot-memory, action-items, entities, observations, habits, health, calendar |
| `work` | Day job | hot-memory, action-items, entities, projects, observations |
| `side-project` | Ventures, hobbies | hot-memory, action-items, projects, observations |
| `system` | Cog internals (auto-created) | self-observations, patterns, action-items, run-log, foresight-nudge |

## Phase 2: Confirm

Before writing, show the user a summary:

```
Here's what I'll set up:

Domains:
- personal — Family, health, day-to-day
- acme — Work at Acme Corp (Designer)
- myapp — Side project

This will create:
- memory/domains.yml (domain manifest)
- Memory directories + starter files for each domain
- A domain INDEX.md per domain (the L0 table your agent routes through)

Good to go?
```

Wait for confirmation.

## Phase 3: Generate

### 3a. Write `memory/domains.yml`

Always include `cog-meta` as a system domain automatically.

```yaml
# Cog Domain Manifest — generated by /cog
# Single source of truth for all memory domains.
# To modify: run /cog again.

domains:
  - id: personal
    path: personal
    type: personal
    label: "<from conversation>"
    triggers: [<inferred keywords>]
    files: [hot-memory, action-items, entities, observations, habits, health, calendar]

  - id: cog-meta
    path: cog-meta
    type: system
    label: "Cog self-knowledge and patterns"
    triggers: [cog, meta, memory system, patterns]
    files: [self-observations, patterns, action-items, run-log, foresight-nudge]
```

### 3b. Create Directories and Starter Files

For each domain, create `memory/{path}/` and starter files:

**hot-memory.md:**
```markdown
<!-- L0: Current state and top-of-mind for {label} -->
# {Label} — Hot Memory

<!-- Rewrite freely. Keep under 50 lines. -->
```

**observations.md:**
```markdown
<!-- L0: Timestamped observations and events -->
# {Label} — Observations

<!-- Append-only. Format: - YYYY-MM-DD [tags]: observation -->
```

**action-items.md:**
```markdown
<!-- L0: Open and completed tasks -->
# {Label} — Action Items

## Open

## Completed
```

**entities.md:**
```markdown
<!-- L0: People, places, and things -->
# {Label} — Entities

<!-- 3-line max per entry. Format: ### Name (relationship) / facts / status|last -->
```

**Other files** (calendar, health, habits, projects, etc.):
```markdown
<!-- L0: {file name} for {label} -->
# {Label} — {File Name}
```

**cog-meta files** (system domain) each get an L0 header plus a format comment:

| File | Format comment |
|------|----------------|
| `self-observations.md` | `<!-- Append-only. Format: - YYYY-MM-DD [tag]: observation -->` |
| `patterns.md` | `<!-- Edit in place. Timeless rules only. HARD LIMIT: 70 lines / 5.5KB. -->` |
| `action-items.md` | `<!-- Format: - [ ] task \| due:YYYY-MM-DD \| pri:high/med/low \| added:YYYY-MM-DD. [housekeeping] = routed over-cap metric; pri:low = system idea. -->` |
| `run-log.md` | `<!-- Append-only. Format: - YYYY-MM-DD /skill-name: outcome -->` |
| `foresight-nudge.md` | `<!-- Overwritten by the foresight skill each run. -->` |

Also create the empty `cog-meta/scenarios/` directory.

### 3c. Create Cross-Domain Files and Indexes

If they don't exist:
- `memory/hot-memory.md` — cross-domain strategic context
- `memory/link-index.md` — backlink index (auto-generated)
- `memory/glacier/index.md` — glacier catalog

Then bootstrap `memory/{domain}/INDEX.md` for each domain using the housekeeping skill's index format (step 6b): `| File | Lines | Summary |` rows built from the L0 headers just written (line count from `wc -l`), subfolders inline when ≤5 files or as one folder row plus their own `INDEX.md` when larger, one `(empty)` row for each of `threads/` / `scenarios/` where present, with header `<!-- L0: L0 index of {domain} files -->` and `<!-- Auto-generated from L0 headers. Do not edit. -->` / `<!-- Last updated: YYYY-MM-DD -->` comments. Housekeeping regenerates these on every run — this bootstrap just prevents "stale index" flags before the first housekeeping.

### 3d. No per-domain skills

Cog deliberately installs **no** per-domain skills or shims. Routing is data, not code: `domains.yml` (always loaded) carries each domain's `label` and `triggers`, and each domain's `INDEX.md` carries its file-level L0s. The agent matches a query against the manifest, opens the matched index, then opens only the files it points to. Adding a domain is therefore just a manifest entry plus a folder — nothing to install, nothing to drift.

## Phase 4: Summary

Output:
- Domains created
- Files generated
- Indexes bootstrapped
- Next steps: "Just talk naturally. Your memory system is ready."

## Setup Rules

1. **Never delete** — setup only creates and updates
2. **Idempotent** — running again is safe, skips existing files
3. **cog-meta is automatic** — always included, never ask about it
4. **Conversational first** — no one edits YAML manually
5. **Re-runs are additive** — "Want to add more domains or reconfigure?"
