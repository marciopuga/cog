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

**Reflect rules check:**
- Did condensation produce useful patterns, or noise?
- Did thread candidate detection work?
- Is reflect staying in its lane?

### 3. Rule Change Proposals

Based on findings, propose concrete rule changes. Don't fix content — fix the rules.

For each proposal:
- What problem does it solve?
- What evidence supports it?
- What's the risk?

**Apply rule changes directly** to the relevant skill files if clearly beneficial and low-risk. For changes that affect user-facing behavior, note them as proposals for user review.

### 4. Write Observations & Update Log

**Observations** — Append to `memory/cog-meta/evolve-observations.md`:
- Format: `- YYYY-MM-DD [tag]: observation`
- Tags: bloat, staleness, redundancy, gap, architecture, opportunity, rule-drift, process-health

**Evolve Log** — Append to `memory/cog-meta/evolve-log.md`:
- Run number, process effectiveness findings, rule changes applied or proposed, deferred items
- Update "Next Run Priorities" section at top

### 5. Debrief

Concise summary:
- *Process health* — did housekeeping/reflect follow their rules?
- *Rule changes* — applied or proposed, with rationale
- *Architecture notes* — structural observations
- *Next evolve* — top 3 things to check next time

Keep it actionable. Numbers over narrative.

## Activation

Read evolve-log.md and evolve-observations.md FIRST for continuity. Then audit the system. You are the architect — you design the rules, you don't play by them.
