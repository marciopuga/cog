Use this skill for scenario simulation — modeling decision branches with timelines, dependencies, and contingencies grounded in real memory data. Trigger if the user says "scenario", "what if", "model this", "simulate", "play out", "what happens if", or similar branching/decision-modeling requests.

**This is NOT /foresight.** Foresight finds the question. Scenario models the answers.

## Domain

Cross-domain decision modeling — personal, work, projects, health, family.

## Memory Files

Read based on scenario topic:
- `memory/hot-memory.md`
- `memory/personal/calendar.md`
- `memory/personal/action-items.md`
- Work domain action-items (read `memory/domains.yml` for active work domains)
- Relevant domain hot-memory and entity files
- `memory/cog-meta/scenarios/` (check for duplicates)
- `memory/cog-meta/scenario-calibration.md` (past accuracy)

## Process

### 1. Decision Point Identification

A valid scenario requires:
- A **fork** — at least 2 meaningfully different paths
- **Stakes** — wrong choice has real cost
- **Uncertainty** — right choice isn't obvious
- **Time sensitivity** — decision window is closing

### 2. Dependency Mapping

**Upstream dependencies** (constraints): calendar, commitments, people's states, health/financial constraints.
**Downstream consequences** (cascading effects): action items, calendar events, people affected.

Every dependency must cite its source file.

### 3. Branch Generation

Generate 2-3 branches. For each:

```
### Branch N: <name>

**Path**: <what happens, step by step>
**Timeline**: <mapped to real calendar>
**Assumptions**: <what must be true>
**Dependencies**: <what else changes>
**Risk**: <canary signal — earliest indicator it's going wrong>
**Confidence**: <calibrated against past accuracy>
```

Include at least one branch the user probably isn't considering.

### 4. Timeline Overlay

Map each branch against the actual calendar. Show where branches collide with reality.

### 5. Contingency Mapping

For each branch: `If [assumption] breaks → watch for [signal] → pivot to [contingency]`

### 6. Write Scenario File

Write to `memory/cog-meta/scenarios/{slug}.md` with YAML frontmatter:

```yaml
---
type: scenario
domain: <primary domain(s)>
created: YYYY-MM-DD
status: active
check-by: YYYY-MM-DD
resolution-by: YYYY-MM-DD
decision: <one-line>
source: user|foresight
---
```

## Rules

1. **Read-only except for output** — writes ONLY to `memory/cog-meta/scenarios/{slug}.md`
2. **2-3 branches, not more**
3. **Evidence-based** — every dependency cites a source file
4. **Calendar-grounded** — every branch overlays against real calendar
5. **Confidence-calibrated** — read calibration before assigning confidence

## Activation

Read scenario-calibration.md first. Then read relevant memory files. Model the futures. Be honest about uncertainty.
