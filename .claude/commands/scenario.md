Use this skill for scenario simulation — modeling decision branches with timelines, dependencies, and contingencies grounded in real memory data. Trigger if the user says "scenario", "what if", "model this", "simulate", "play out", "what happens if", or similar branching/decision-modeling requests. Also triggered when foresight flags a scenario candidate.

**This is NOT /foresight.** Foresight = scan broadly, write one nudge. Scenario = take a specific decision point, branch it into 2-3 paths, map dependencies and timelines for each. **Foresight finds the question. Scenario models the answers.**

**This is NOT /reflect.** Reflect = past-facing, mines interactions, improves memory. Scenario = future-facing, models possible futures from a decision point. Reflect checks old scenarios against reality (the feedback loop), but scenario creates them.

## Domain

Cross-domain decision modeling — personal, work, projects, health, family. Scenarios are most valuable when a decision in one domain has cascading effects across others.

## Memory Files

Read based on scenario topic — this is focused, not a broad scan:
- `memory/hot-memory.md` (cross-domain strategic context)
- `memory/personal/calendar.md` (upcoming timeline for overlay)
- `memory/personal/action-items.md` (existing commitments, constraints)
- Work domain action-items (read `memory/domains.yml` for active work domains)
- Relevant domain hot-memory and entity files based on the scenario topic
- `memory/cog-meta/scenarios/` (existing scenarios — check for duplicates or related active scenarios)
- `memory/cog-meta/scenario-calibration.md` (past accuracy — calibrate confidence accordingly)

## Process

### 1. Decision Point Identification

From user input or foresight seed, identify the specific decision point. A valid scenario requires:
- A **fork** — at least 2 meaningfully different paths forward
- **Stakes** — the outcome matters enough that choosing wrong has real cost (time, money, relationships, health)
- **Uncertainty** — the right choice isn't obvious from current information
- **Time sensitivity** — the decision window is closing or the consequences unfold on a timeline

If the input doesn't meet these criteria, say so and suggest what would make it scenario-worthy. Don't force-fit.

Format the decision point:
```
Decision: <one-line framing>
Context: <why this matters now — cite memory files>
Window: <when must this be decided by>
Domains affected: <which life/work domains>
```

### 2. Dependency Mapping

Read across memory files to identify what this decision depends on and what depends on it.

**Upstream dependencies** (things that constrain the decision):
- Calendar events, deadlines, commitments from action-items
- Other people's states/decisions from entities
- Health, financial, or logistical constraints
- Active scenarios that overlap

**Downstream consequences** (things that change based on which path is chosen):
- Action items that would need to change
- Calendar events that would need to move
- People who would be affected
- Other decisions that cascade from this one

Every dependency must cite its source file: `[[personal/calendar]]`, `[[work/acme/action-items]]`, etc.

### 3. Branch Generation

Generate 2-3 branches. Not more — forced prioritization.

For each branch:

```
### Branch N: <name>

**Path**: <what happens, step by step>
**Timeline**: <when each step occurs, mapped to real calendar>
**Assumptions**: <what must be true for this path to work>
**Dependencies**: <what else changes if this path is taken>
**Risk**: <what could go wrong, and what would you see first — the canary signal>
**Confidence**: <how likely is this path to play out as described — calibrated against past scenario accuracy>
```

Branch quality rules:
- Each branch must be **genuinely different** — not "do it" vs "do it but slightly differently"
- Include at least one branch the user probably isn't considering (the non-obvious path)
- Every claim in a branch must trace to a memory file or be explicitly marked as an assumption

### 4. Timeline Overlay

Map each branch's key events against the actual calendar. Cross-reference `calendar.md` for recurring routines.

Output a simple timeline per branch:
```
Branch 1 Timeline:
- Week of Mar 17: <action>
- Week of Mar 24: <action> (note: conflict with X)
- Week of Apr 1: <action>
...
```

The overlay is what makes scenarios useful — it shows where branches collide with reality.

### 5. Contingency Mapping

For each branch, identify the **canary signal** — the earliest observable indicator that this branch is going off-track.

```
If [assumption] breaks → watch for [signal] → pivot to [contingency]
```

This turns the scenario from a static prediction into a monitoring framework.

### 6. Write Scenario File

Write to `memory/cog-meta/scenarios/{slug}.md`:

```yaml
---
type: scenario
domain: <primary domain(s)>
created: YYYY-MM-DD
status: active
check-by: YYYY-MM-DD
resolution-by: YYYY-MM-DD
decision: <one-line>
related-threads: [thread1, thread2]
source: user|foresight
---
```

Body format:
```markdown
# Scenario: <decision>
<!-- Auto-generated by /scenario. Checked by /reflect. -->

## Decision Point
<from step 1>

## Dependencies
### Upstream
<constraints — each with [[source]] link>

### Downstream
<consequences — each with [[source]] link>

## Branches

### Branch 1: <name>
<from step 3>

### Branch 2: <name>
<from step 3>

### Branch 3: <name> (optional)
<from step 3>

## Timeline Overlay
<from step 4>

## Contingency Map
<from step 5>

## Retrospective
<!-- Added by /reflect when status changes to resolved -->
```

## Rules

1. **Read-only except for output** — Scenario NEVER edits existing memory files. Writes ONLY to `memory/cog-meta/scenarios/{slug}.md`. If you spot a memory error, note it in the dependencies section and route to reflect.
2. **2-3 branches, not more** — force prioritization. If you can't distinguish 2 branches, it's not a scenario.
3. **Evidence-based** — every dependency and assumption cites a source file. No hunches.
4. **Calendar-grounded** — every branch must overlay against the real calendar. No timelines in a vacuum.
5. **Confidence-calibrated** — read `scenario-calibration.md` before assigning confidence. If past scenarios have been overconfident, adjust.
6. **One scenario per decision** — don't combine multiple decisions. If they're linked, note the dependency and create separate scenarios.

## Anti-Patterns

- Don't scenario obvious decisions — if one path is clearly better, just say so
- Don't scenario things already decided — check action-items for existing commitments
- Don't produce "analysis paralysis" — the goal is clarity, not exhaustive enumeration
- Don't scenario recurring/routine decisions — this is for inflection points, not daily choices
- Don't ignore the non-obvious path — if all branches are variations of what the user already thinks, you're not adding value
- Don't invent facts — if you don't have data for a dependency, mark it as an assumption

## Trigger Threshold

A scenario is worth running when:
1. **Foresight flags it** — foresight's pattern projection identified a fork with stakes
2. **User explicitly asks** — `/scenario what if...`
3. **Action item conflict** — two critical/high-priority action items have incompatible timelines
4. **Calendar crunch** — upcoming 2-week window has more commitments than capacity
5. **Cross-domain cascade** — a decision in one domain visibly affects 2+ others

NOT worth running for: hypotheticals with no deadline, decisions where all paths lead to the same outcome, things already decided.

## Activation

Read scenario-calibration.md first (if it exists) for past accuracy. Then read the relevant memory files for the scenario topic. Model the futures. Be honest about uncertainty.
