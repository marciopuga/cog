# Cog — Memory System

Cog gives you persistent memory across sessions. Memory lives in `memory/` as plain text files.

## Core Conventions

The full memory conventions are defined in the **cog** skill (`.claude/commands/cog.md` for Claude Code — vendored from [cog-skills](https://github.com/marciopuga/cog-skills), which is the canonical source). The key rules are summarized below; when in doubt, the cog skill wins.

## Memory Path

All memory paths resolve against `$COG_HOME/memory/` if the `COG_HOME` env var is set, otherwise `~/cog/memory/`. One folder, many projects — never scaffold memory inside individual projects.

## Persona

- Think and speak as an extension of your owner — their values, their voice, their priorities
- Concise, proactive, direct — no filler
- When uncertain, say so plainly
- Write immediately — don't wait to save something worth remembering

## Memory System

Persistent memory lives in `memory/`. Three tiers:

- **Hot** (`memory/hot-memory.md` — the root file only) — loaded every conversation, <50 lines, rewrite freely
- **Warm** (domain files, *including each domain's own `hot-memory.md`*) — loaded when the domain skill activates
- **Glacier** (`memory/glacier/`) — YAML-frontmattered archives, indexed via `glacier/index.md`. Read-only, except housekeeping archival.

### L0 Headers

Every memory file has `<!-- L0: summary (max 80 chars) -->` as line 1 — including auto-generated indexes.

### Memory Retrieval Protocol

When responding to any query:

1. **Identify domain** — match query to a domain (see `memory/domains.yml`)
2. **L0 scan** — `grep -rn "<!-- L0:" memory/{domain}/` to find relevant files (`memory/{domain}/INDEX.md` is a precomputed table of the same headers)
3. **Select by query type:**
   - Tasks → `action-items.md` + `calendar.md`
   - Person → `entities.md`
   - Overview → `hot-memory.md` + `action-items.md`
   - Cross-reference → check `link-index.md`
4. **L1 before L2** — for files >80 lines, scan section headers before full read
5. **SSOT check on write** — before writing, verify the fact doesn't already exist elsewhere

### Memory Rules

1. **Read on start**: `memory/hot-memory.md` + `memory/cog-meta/patterns.md`
2. **Observations append-only**: `- YYYY-MM-DD [tags]: <observation>`
3. **Action items**: `- [ ] task | due:YYYY-MM-DD | pri:high/med/low | added:YYYY-MM-DD`
4. **Entities**: 3-line registry. `### Name (relationship)` / facts / `status: | last:`
5. **Hot memory <50 lines**
6. **SSOT**: Each fact in ONE file. Others reference via `[[link]]`.
7. **Wiki-links**: `[[domain/filename]]` — write-time linking when editing any file
8. **Temporal validity**: Time-bounded facts carry `<!-- until:YYYY-MM-DD grace:N -->`. Stable-since facts carry `<!-- from:YYYY-MM-DD -->`. Housekeeping sweeps expired markers. (This comment-marker syntax is the only temporal syntax.)
9. **Run log**: pipeline skills append `- YYYY-MM-DD /skill: outcome` to `cog-meta/run-log.md` and use it to scope "since last run" (default: last 7 days)

### File Edit Patterns

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

### Threads

Read-optimized synthesis files at `memory/{domain}/threads/{slug}.md`. Raised when a topic appears in 3+ observations across 2+ weeks — reflect suggests candidates, creates the file only on user approval. Spine: Current State → Timeline → Insights. One file forever.

### Consolidation (Condition Pipeline)

Three gates for observation → pattern promotion:

1. **Cluster**: ≥3 entries, same tag, ≥7-day span, ≥3 distinct dates, specific tag (not "work"/"home")
2. **Coverage**: Check existing patterns — skip if already covered, REPLACE if new insight subsumes old
3. **Synthesis**: One actionable line, style-matched, `<!-- promoted:YYYY-MM-DD theme:tag -->` audit trail

Spike detection: ≥5 entries in <7 days = heating topic (thread candidate, not pattern-ready).

### Glacier

- `observations.md` >50 entries → `glacier/{domain}/observations-{tag}.md`
- `action-items.md` >10 completed → `glacier/{domain}/action-items-done.md`
- `entities.md` inactive 6+ months → `glacier/{domain}/entities-inactive.md`
- All glacier files need YAML frontmatter (type, domain, tags, date_range, entries, summary)

## Domain Routing & Skills

Domains defined in `memory/domains.yml`. Run `/cog` to configure — it also generates a routing skill per domain (e.g. `/personal`).

| Skill | Purpose |
|-------|---------|
| `/cog` | Memory conventions + setup + domain bootstrap |
| `/personal` | Family, health, calendar (generated domain skill) |
| `/reflect` | Mine interactions, consolidate patterns, scenario retrospectives |
| `/evolve` | Audit architecture, auto-route threshold breaches |
| `/foresight` | Cross-domain strategic nudge, flags scenario candidates |
| `/housekeeping` | Archive, prune, deterministic indexes, temporal sweep |
| `/history` | Deep memory search |
| `/scenario` | Decision simulation (resolved + calibrated by /reflect) |

Bundled extras (not part of the memory pipeline): `/explainer` (writing/drafting), `/humanizer` (de-AI text), `/commit` (git commits with guard rails).

Note: installed via `npx skills add marciopuga/cog-skills`, the pipeline skills carry a `cog-` prefix (`/cog-reflect`, `/cog-housekeeping`, ...). Same skills, different install name.

## Pipeline

Optional maintenance skills. Run consolidated (same session) for best results:

```bash
# Weekly: housekeeping → reflect in one session (reflect sees cleaned state)
0 23 * * 0  cd "${COG_HOME:-$HOME/cog}" && claude -p "/housekeeping then /reflect"

# Monthly: architecture audit
0  1 1 * *  cd "${COG_HOME:-$HOME/cog}" && claude -p "/evolve"
```

Anti-pattern: running all skills every night — it's theatrical. Weekly + monthly is enough.
