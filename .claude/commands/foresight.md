---
name: foresight
description: >
  Cross-domain strategic scan. Detects convergence between life areas,
  velocity changes, and upcoming timing windows. Writes one actionable
  nudge per run. Invoke with /foresight.
---

# Cog Foresight

Strategic foresight — connecting dots across domains. Future-facing.

**This is NOT /cog-reflect** (past-facing) or **/cog-evolve** (system architecture). Foresight scans broadly and projects trajectories.

## Memory Path

All files under `~/cog/memory/`.

## Minimum Data Check

Before scanning, verify there's enough material for meaningful foresight:
- If total observations across all domains < 10: stop. Say "Not enough history for strategic foresight. Keep capturing for a few more weeks."
- If only 1 domain has data: say "Foresight works best with 2+ active domains (it connects dots between them). Consider adding more domains or building out existing ones."
- If no action items exist: say "No active items to assess velocity on. Capture some tasks first."

Don't force a nudge from thin data. One honest "not yet" is better than a weak insight.

## Files to Read

Read broadly — this is a scan:

1. Read `memory/domains.yml` to discover all active domains
2. For each domain: `hot-memory.md` + `action-items.md`
3. Also read:
   - `memory/hot-memory.md` (cross-domain context)
   - `memory/personal/entities.md` (birthdays, relationships)
   - `memory/personal/calendar.md` (upcoming events)
   - `memory/personal/health.md` (health trajectory)
   - Recent observations across all domains (last 7 days)
   - Thread current-state sections

## Process

### 1. Cross-Domain Convergence

Look for topics, people, or themes appearing in 2+ domains simultaneously. These are convergence points — where effort in one area compounds into another.

### 2. Velocity & Stall Detection

Classify active items:
- **Accelerating** — multiple updates last week. Signal: ride the wave.
- **Cruising** — steady progress. Signal: nothing to flag.
- **Stalling** — no movement 2+ weeks. Signal: blocked or lost priority?
- **Dormant** — domain silence 4+ weeks. Signal: conscious or drift?

### 3. Timing Awareness

Read calendar and entities for events in next 2-4 weeks. Things that should start NOW to be ready later.

### 4. Pattern Projection

Read patterns and recent observations. Project: "If this continues 2 more weeks, what happens?"

### 5. Write One Strategic Nudge

Synthesize into **one nudge**. Not a list. One thing.

The nudge must:
- Cite at least 2 source files
- Be something the user hasn't explicitly asked about
- Be actionable — "do Y because of X and Z" (not "think about X")
- Connect dots across domains

Write to `memory/cog-meta/foresight-nudge.md`:

```markdown
# Foresight Nudge
<!-- Last updated: YYYY-MM-DD -->

## Signal
<What you noticed — raw observation from 2+ domains>

## Insight
<Why it matters — the connection or trajectory>

## Suggested Action
<One concrete thing to do>

---
Sources: [[file1]], [[file2]]
```

Overwrite each run. One nudge per run.

## Rules

1. **Read-only** — foresight NEVER edits memory files. Only writes `foresight-nudge.md`.
2. **One nudge** — force prioritization.
3. **Evidence-based** — cite 2+ source files.
4. **Non-obvious** — should surprise. If the user already knows, pick something else.
5. **Forward-looking** — project into next week/month.
6. **Cross-domain preferred** — connections between domains are highest value.

## Anti-Patterns

- Don't repeat what housekeeping already flagged (stale items, birthdays)
- Don't recommend "reflect on X" — be specific about what to DO
- Don't flag explicitly deferred items
- Don't flag things that are cruising
- Don't write a mini-briefing — one insight, one action
