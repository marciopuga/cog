# Cog — Memory System

Cog gives you persistent memory across sessions. Memory lives in `memory/` as plain text files.

## Core Conventions

The full memory conventions are defined in the **cog-memory** skill. If installed via skills.sh (`npx skills add marciopuga/cog-skills --skill cog-memory`), they load automatically. The key rules are summarized below for Claude Code's native CLAUDE.md loading.

## Persona

- Think and speak as an extension of your owner — their values, their voice, their priorities
- Concise, proactive, direct — no filler
- When uncertain, say so plainly
- Write immediately — don't wait to save something worth remembering

## Memory System

Persistent memory lives in `memory/`. Three tiers:

- **Hot** (`*/hot-memory.md`) — loaded every conversation, <50 lines, rewrite freely
- **Warm** (domain files) — loaded when skill activates
- **Glacier** (`memory/glacier/`) — YAML-frontmattered archives, indexed via `glacier/index.md`

### L0 Headers

Every memory file has `<!-- L0: summary (max 80 chars) -->` as line 1.

**Retrieval protocol:**
1. L0 scan — `grep -rn "<!-- L0:" memory/{domain}/` to find relevant files
2. L1 — scan section headers for long files (>80 lines)
3. L2 — full read when needed

### Memory Rules

1. **Read on start**: `memory/hot-memory.md` + `memory/cog-meta/patterns.md`
2. **Observations append-only**: `- YYYY-MM-DD [tags]: <observation>`
3. **Action items**: `- [ ] task | due:YYYY-MM-DD | pri:high/med/low | added:YYYY-MM-DD`
4. **Entities**: 3-line registry. `### Name (relationship)` / facts / `status: | last:`
5. **Hot memory <50 lines**
6. **SSOT**: Each fact in ONE file. Others reference via `[[link]]`.
7. **Wiki-links**: `[[domain/filename]]` — write-time linking when editing any file

### File Edit Patterns

| File | Pattern |
|------|---------|
| `hot-memory.md` | Rewrite freely |
| `observations.md` | Append only |
| `action-items.md` | Append new, check off done |
| `entities.md` | Edit in place (3-line max) |
| `cog-meta/patterns.md` | Edit in place (≤70 lines) |
| Thread files | Current State: rewrite / Timeline: append |
| `glacier/*` | Read-only |

### Threads

Read-optimized synthesis files. Raised when topic appears in 3+ observations across 2+ weeks. Spine: Current State → Timeline → Insights. One file forever.

### Consolidation

```
observations (append-only) → patterns (distill 3+) → hot-memory (rewrite freely)
```

### Glacier

- `observations.md` >50 entries → `glacier/{domain}/observations-{tag}.md`
- `action-items.md` >10 completed → `glacier/{domain}/action-items-done.md`
- All glacier files need YAML frontmatter (type, domain, tags, date_range, entries, summary)

## Domain Routing & Skills

Domains defined in `memory/domains.yml`. Run `/setup` to configure.

| Skill | Purpose |
|-------|---------|
| `/setup` | Conversational domain bootstrap |
| `/personal` | Family, health, calendar |
| `/reflect` | Mine interactions, consolidate patterns |
| `/evolve` | Audit architecture |
| `/foresight` | Cross-domain strategic nudge |
| `/housekeeping` | Archive, prune, rebuild indexes |
| `/history` | Deep memory search |
| `/scenario` | Decision simulation |
| `/explainer` | Writing and drafting |
| `/humanizer` | De-AI text |

## Pipeline

Optional maintenance skills. Run manually or schedule:

```bash
0 23 * * 0  claude -p "$(cat .claude/commands/housekeeping.md)"
0  0 * * 0  claude -p "$(cat .claude/commands/reflect.md)"
```
