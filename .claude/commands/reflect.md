---
name: reflect
description: >
  Mine recent interactions for patterns and consolidate memory.
  Detects contradictions, promotes observations to patterns, triages hot-memory,
  and suggests thread candidates. Run weekly or nightly for best results.
  Invoke with /reflect.
---

# Cog Reflect

Self-reflection and memory consolidation. Past-facing — mines interactions, fixes contradictions, distills patterns.

**Take your time.** This is a deep session. Read broadly, cross-reference, and ACT on findings. You're the maintainer of the knowledge base.

## Memory Path

All files under the resolved memory path: `$COG_HOME/memory/` if `COG_HOME` is set, otherwise `~/cog/memory/`.

## Orientation (run first)

Scope your work before reading files:

1. Find files changed since the last run — read `memory/cog-meta/run-log.md` for the last `/reflect` entry and scope to files modified since that date (no entry → default to the last 7 days)
2. Get L0 summaries across all domains (quick routing)
3. Check observation entry counts (archival threshold = 50)

Focus on recently-changed files. Skip unchanged ones.

### Minimum Data Check

Before proceeding, verify there's enough material to work with:
- If total observations across all domains < 5: stop. Say "Not enough data yet. Keep capturing observations and run again when you have more material."
- If no files were modified in the last 7 days: flag it. "Memory hasn't been updated recently. Consider capturing some observations first."
- If patterns.md is empty and observations < 10: say "Too early to consolidate. You need ~10+ observations before patterns emerge."

Don't produce low-quality output from insufficient data. It's better to say "not yet" than to force weak patterns.

## Files to Read

- `memory/cog-meta/self-observations.md`
- `memory/cog-meta/patterns.md`
- `memory/cog-meta/improvements.md`
- `memory/cog-meta/scenarios/*.md` (active scenarios, for the retrospective step)
- All domain `observations.md` files
- All domain `action-items.md` files
- All `hot-memory.md` files

## Process

### 1. Review Recent Interactions

Look for:
- **Unresolved threads** — questions asked but never answered
- **Broken promises** — "I'll do X" that never happened
- **Repeated friction** — same question asked multiple ways, user corrections
- **Missed cues** — things the user had to repeat
- **Memory gaps** — information discussed but never saved
- **Feature ideas** — improvements that came up organically

### 2. Consistency Sweep

Systematic contradiction detection:

1. **Hot-memory vs canonical sources**: For every claim in hot-memory, verify against the canonical file. Fix hot-memory if stale.
2. **Cross-file fact check**: Verify shared facts are consistent. More recent source wins.
3. **Temporal validity check**: Scan for `<!-- from:YYYY-MM-DD -->` markers older than 6 months (flag for review — is this still true?). Expired `<!-- until: -->` markers are housekeeping's job to sweep — if you see any, note it in the debrief rather than sweeping them yourself.
4. **Cross-domain entity check**: Same person in multiple entity files → one canonical, others pointer.

### 3. Consolidation (Condition Pipeline)

Rigorous observation → pattern promotion. Three gates prevent noise from entering pattern files.

**Gate 1: Cluster Detection**

Scan all `observations.md` files. Group entries by primary tag. A cluster is promotable when ALL conditions are met:
- ≥3 entries with the same primary tag
- Entries span ≥7 days (not a single-day burst)
- ≥3 distinct dates (not the same insight repeated on one day)
- Tag is specific (reject broad tags: "work", "home", "general", "misc")

**Gate 2: Coverage Check**

Before promoting, check if the pattern ALREADY EXISTS:
- Read `cog-meta/patterns.md` and any domain satellite `patterns.md`
- If an existing pattern already covers this cluster's insight → skip (not a gap)
- If the new insight SUBSUMES an existing pattern (broader, more accurate) → plan to REPLACE the old one

**Gate 3: Synthesis & Write**

For each uncovered cluster:
- Distill into one actionable, timeless pattern line
- Style-match against existing patterns (same voice, same structure)
- Add `<!-- promoted:YYYY-MM-DD theme:tag -->` audit trail at the end of the line
- Write to `cog-meta/patterns.md` (universal) or `{domain}/patterns.md` (domain-specific)
- If replacing an existing pattern, remove the old line and add the new one

**Replacement is healthy** — patterns evolve. A new pattern that subsumes 2 older ones should replace both. Track replacements in debrief.

**Pattern file caps:**
- Core `patterns.md`: hard limit 70 lines / 5.5KB — universal rules only
- Satellite files: soft cap 30 lines each
- If near cap: merge overlapping rules or replace weaker patterns. Never just truncate.

**Spike Detection (below promotion bar):**

Clusters with ≥5 entries in <7 days don't meet the 7-day span requirement. But they signal a heating topic:
- Note in debrief as "Spike: [tag] — [N] entries in [N] days"
- These are thread-raising candidates (see Step 5)

**Hot-memory relevance:**
- **Promote**: Pattern heating up → add to hot-memory
- **Demote**: Item gone quiet (no references 2+ weeks) → remove from hot-memory

### 4. Entity Format Enforcement

Scan all `entities.md` files:
1. **3-line check**: Entries >3 lines → compress or flag for thread promotion
2. **Status/last fields**: Every entry needs `status:` and `last:` fields
3. **Cross-domain pointers**: Same person in multiple files → one canonical, others `see [[link]]`

### 5. Thread Candidate Detection

Scan observations for topics appearing across 3+ dates or spanning 2+ weeks:
- Check if a thread already exists at `memory/{domain}/threads/`
- If not: "Thread candidate: [topic] — [N] fragments across [date range]"
- Don't auto-create — suggest. **If the user approves**, create `memory/{domain}/threads/{slug}.md` with an L0 header and the standard spine (Current State / Timeline / Insights), seeding the Timeline from the source observations via wiki-links.

### 6. Scenario Retrospective

Check `memory/cog-meta/scenarios/` for active scenarios (skip if the directory is empty):

1. **Past check-by date** → compare each branch against what actually happened (observations, action items, calendar). Note which branch reality is tracking and whether any canary signals fired.
2. **Decision made / resolution reached** → set frontmatter `status: resolved`, write the `## Retrospective` section (which branch played out, what the scenario got right/wrong), and add a row to the Resolved Scenarios table in `memory/cog-meta/scenario-calibration.md` (scenario, created, resolved, predicted branch, actual branch, accuracy, lesson) — then update its Metrics section.
3. **Still open and within window** → leave untouched.

This is the feedback loop that keeps scenario confidence calibrated.

### 7. Act on Findings

**Write:**
- New self-observations → append to `cog-meta/self-observations.md` (max 5 per run)
- Pattern updates → edit `cog-meta/patterns.md`
- Memory gaps → write to appropriate domain files

**Connect:**
- Scattered information → add `[[links]]`
- When adding A→B, check if B benefits from `[[A]]` back

### 8. Debrief

Compose a summary:
- *What I learned* — new patterns and insights
- *What I fixed* — memory gaps filled, corrections made
- *What to watch* — things to be mindful of
- *Thread candidates* — topics worth raising
- *Scenarios* — resolved or drifting off-track

**List every file modified and summarize changes.** Never just say "Done".

Finally, append a run entry to `memory/cog-meta/run-log.md`: `- YYYY-MM-DD /reflect: <one-line outcome>`

## Artifact Formats

- **Self-observation**: `- YYYY-MM-DD [tag]: <observation>`
- **Pattern**: Edit existing section or add new bullet
- **Improvement**: `- <idea> (added YYYY-MM-DD)`
