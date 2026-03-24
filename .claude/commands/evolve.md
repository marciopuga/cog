Use this skill for systems-level self-improvement. Trigger if the user says "evolve", "system audit", "audit yourself", "check your architecture", or similar structural introspection requests.

**This is NOT /reflect.** Reflect = "what did I learn from interactions?" Evolve = "are the rules and architecture working?" **Evolve never touches memory content — it changes the rules that govern how content moves.**

## Domain

Systems architecture — process rules, skill design, tier effectiveness, pipeline health.

## Memory Files

Read FIRST — this is your continuity:
- `memory/cog-meta/evolve-log.md` — your run log
- `memory/cog-meta/evolve-observations.md` — architectural issues spotted

Architecture reference:
- `CLAUDE.md` — project instructions
- `.claude/commands/housekeeping.md` — housekeeping rules
- `.claude/commands/reflect.md` — reflect rules

Measure (don't edit content):
- `memory/hot-memory.md`
- `memory/cog-meta/patterns.md`
- Any domain satellite pattern files (e.g. `work/*/patterns.md`)

## Orientation (run FIRST, before any file reads)

Use these shell commands to see exactly what changed since last run:

```bash
# What did housekeeping and reflect change recently?
git diff HEAD~1 --stat memory/

# Detailed diff of architectural files (what you care about)
git diff HEAD~1 memory/cog-meta/patterns.md memory/hot-memory.md CLAUDE.md

# What changed in the last 24h?
find memory/ -type f -name "*.md" -mtime -1 | sort

# Current prompt weight components (quick file sizes)
wc -c memory/hot-memory.md memory/cog-meta/patterns.md memory/cog-meta/briefing-bridge.md 2>/dev/null
```

Use git diffs to understand what housekeeping/reflect actually did, instead of re-reading entire files.

## Process

### 1. Architecture Review

Evaluate the structural design:

- **Tier design** — are the tiers (hot-memory → patterns → observations → glacier) well-defined?
- **Condensation pipeline** — is the flow working? Where does it leak or stall?
- **File naming and organization** — any files in wrong domains? Orphaned files?
- **Skill boundaries** — are housekeeping/reflect/evolve boundaries clean? Any drift?

### 2. Process Effectiveness Audit

Review the output of recent housekeeping and reflect runs:

**Housekeeping rules check:**
- Did pruning priority order work? Or did it trim wrong things?
- Are glacier thresholds (50 obs, 10 action items) right?
- Is the 50-line hot-memory cap appropriate?
- Is entity format enforcement catching violations?

**Reflect rules check:**
- Did condensation produce useful patterns, or noise?
- Did thread candidate detection work?
- Is reflect staying in its lane?
- Are patterns routing to the right file (core vs satellite)?

**Scorecard metrics** — measure and record in evolve-log:
- Core `patterns.md`: line count / 70, byte size / 5.5KB (target: ≤1.0)
- Satellite pattern files: list each with line count (soft cap: 30)
- Entity compression ratio: `(total entity lines across all files) / (total ### entries)` (target: ≤3.0)
- Hot-memory line counts vs caps

### 3. Rule Change Proposals

Based on findings, propose concrete rule changes. Don't fix content — fix the rules.

For each proposal:
- What problem does it solve?
- What evidence supports it?
- What's the risk?
- Is this a rule change (apply directly) or architecture change (propose for user review)?

**Apply low-risk rule changes directly** to the relevant skill files. Propose architecture changes for user review.

### 4. Route Content Issues

When you spot content problems during your audit, **don't fix them and don't defer them for yourself**. Route them explicitly:

Format in debrief:
```
→ housekeeping: entities.md at 290 lines, needs glacier pass
→ reflect: hot-memory missing thread link for X
→ reflect: patterns.md has stale snapshot data from Feb
```

If the same content issue keeps appearing across runs, that's a **rule problem** — propose a rule change so housekeeping/reflect catch it themselves.

### 5. Generate Scorecard

Overwrite `memory/cog-meta/scorecard.md` with current metrics:
- Core patterns.md: line count / 70, byte size / 5.5KB (target: ≤1.0)
- Satellite pattern files: list each with line count (soft cap: 30)
- Entity compression ratio: `(total entity lines across all files) / (total ### entries)` — target ≤3.0
- Hot-memory line counts vs caps
- Briefing bridge SSOT compliance (% of lines with [[source]] links)

### 6. Write Observations & Update Log

**Observations** — Append to `memory/cog-meta/evolve-observations.md`:
- Format: `- YYYY-MM-DD [tag]: observation`
- Tags: bloat, staleness, redundancy, gap, architecture, opportunity, rule-drift, process-health

**Evolve Log** — Append to `memory/cog-meta/evolve-log.md`:
- Run number, process effectiveness findings, rule changes applied or proposed, deferred items
- Content issues routed (→ housekeeping / → reflect)
- Update "Next Run Priorities" section at top. **Only architecture/design items — never content work.**

### 7. Debrief

Concise summary:
- *Process health* — did housekeeping/reflect follow their rules?
- *Rule changes* — applied or proposed, with rationale
- *Routed issues* — content problems sent to housekeeping/reflect
- *Architecture notes* — structural observations
- *Next evolve* — top 3 architecture priorities

Keep it actionable. Numbers over narrative.

## Activation

Read evolve-log.md and evolve-observations.md FIRST for continuity. Then audit the system. You are the architect — you design the rules, you don't play by them.
