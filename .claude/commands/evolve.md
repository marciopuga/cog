---
name: evolve
description: >
  Audit memory architecture, review rule effectiveness, measure metrics,
  and propose system improvements. Run monthly to keep the system healthy.
  Invoke with /evolve.
---

# Cog Evolve

Systems-level self-improvement. The architect.

**This is NOT /cog-reflect.** Reflect = "what did I learn?" Evolve = "are the rules working?" Evolve never touches memory content — it changes the rules that govern how content moves.

## Memory Path

All files under `~/cog/memory/`.

## Minimum Data Check

Before auditing, verify the system has enough history:
- If reflect has never run (no self-observations, no patterns): stop. Say "Nothing to audit yet. Run /cog-reflect a few times first to build patterns, then evolve can assess whether they're working."
- If patterns.md has < 3 entries: say "Too few patterns to evaluate effectiveness. Let the system run for a few more cycles."

Evolve audits rules — there need to be rules to audit.

## Files to Read

Continuity (read first):
- `memory/cog-meta/self-observations.md` (what's been noticed)
- `memory/cog-meta/patterns.md` (current rules)

Measure (don't edit content):
- `memory/hot-memory.md`
- Any domain satellite pattern files

## Process

### 1. Architecture Review

Evaluate structural design:
- **Tier design** — are hot/warm/glacier boundaries well-defined?
- **Consolidation pipeline** — is the flow working? Where does it stall?
- **File organization** — any files in wrong domains? Orphaned files?
- **Skill boundaries** — are housekeeping/reflect/evolve lanes clean?

### 2. Process Effectiveness Audit

Review output of recent housekeeping and reflect runs:

**Housekeeping check:**
- Did pruning priority order work?
- Are glacier thresholds (50 obs, 10 items) right?
- Is the 50-line hot-memory cap appropriate?

**Reflect check:**
- Did consolidation produce useful patterns or noise?
- Did thread detection work?
- Is reflect staying in its lane?

**Scorecard metrics:**
- Core `patterns.md`: line count / 70 (target: ≤1.0)
- Satellite pattern files: list each with line count (cap: 30)
- Entity compression ratio: total entity lines / total entries (target: ≤3.0)
- Hot-memory line counts vs 50-line cap
- Domain INDEX.md freshness: last-updated date vs today (target: <7 days)
- Temporal markers: count of expired-but-not-swept markers (target: 0)

### 3. Auto-Route on Threshold Breach

This is the critical difference between theatrical evolve (reporting problems) and effective evolve (resolving them). When scorecard metrics breach thresholds, **create concrete action items** — not observations.

**Threshold → Action routing:**

| Metric | Threshold | Action |
|--------|-----------|--------|
| `patterns.md` line ratio > 1.0 | Exceeds 70 lines | → `cog-meta/action-items.md`: "Merge or replace patterns to bring below 70 lines" |
| Satellite pattern file > 30 lines | Exceeds soft cap | → domain `action-items.md`: "Compress {domain} patterns" |
| Entity compression > 3.0 | Entries too verbose | → domain `action-items.md`: "Compress entities or promote to threads" |
| Hot-memory > 50 lines | Exceeds cap | → `action-items.md`: "Prune hot-memory (run /cog-housekeeping)" |
| INDEX.md > 14 days stale | Drift risk | → `cog-meta/action-items.md`: "Rebuild domain indexes (run /cog-housekeeping)" |
| Expired temporal markers > 0 | Stale facts | → `cog-meta/action-items.md`: "Sweep expired temporal markers (run /cog-housekeeping)" |
| Same issue logged 3+ times in self-observations | Recurring unresolved | → Escalate: propose rule change that prevents recurrence |

**Format for auto-routed items:**
```
- [ ] [evolve] {description} | due:YYYY-MM-DD | pri:med | added:YYYY-MM-DD
```

The `[evolve]` tag identifies items created by this skill. If an `[evolve]` item already exists for the same metric, update it — don't duplicate.

**Key principle:** If you're logging an observation about a problem for the third time, that's a rule failure. Stop observing and start fixing.

### 4. Rule Change Proposals

Based on findings, propose concrete rule changes:
- What problem does it solve?
- What evidence supports it?
- What's the risk?
- Rule change (apply directly) vs architecture change (propose for review)?

**Apply low-risk changes directly.** Propose architecture changes for user review.

### 5. Route Content Issues

When you spot content problems that aren't threshold breaches, route them:

```
→ housekeeping: entities.md at 290 lines, needs glacier pass
→ reflect: hot-memory missing link for X
→ reflect: patterns.md has stale data
```

If the same issue keeps appearing → that's a rule problem. Propose a fix (Step 4), don't just route it again.

### 6. Write Observations

Append to `memory/cog-meta/self-observations.md`:
- Format: `- YYYY-MM-DD [tag]: observation`
- Tags: bloat, staleness, redundancy, gap, architecture, opportunity, rule-drift
- Max 3 per run — quality over quantity

### 7. Debrief

Concise summary:
- *Scorecard* — metrics table with current values vs targets
- *Actions created* — items routed to action-items (list each)
- *Rule changes* — applied or proposed
- *Process health* — did housekeeping/reflect follow their rules?
- *Architecture notes* — structural observations

Numbers over narrative. If nothing breaches thresholds, say so and stop — don't invent work.
