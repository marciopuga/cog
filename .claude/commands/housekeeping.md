---
name: housekeeping
description: >
  Archive old observations, prune stale items, rebuild indexes,
  enforce entity format, and maintain memory health. Run weekly
  to prevent memory bloat. Invoke with /housekeeping.
---

# Cog Housekeeping

Memory maintenance — archive, prune, index, enforce format. The janitor.

## Memory Path

All files under `~/cog/memory/`.

## Orientation (run first)

Scope your work:
1. Find files changed since last run
2. Check observation entry counts (>50 = archive threshold)
3. Check completed action item counts (>10 = archive threshold)

Only read files that need work. Skip unchanged files.

### Minimum Data Check

Before proceeding, verify there's enough material to maintain:
- If no observations files exist or all are empty: stop. Say "Nothing to maintain yet. Start by capturing some observations and the system will grow."
- If all entry counts are well below thresholds (obs < 10, items < 3): say "Memory is still light. No maintenance needed yet — keep building."

Don't run a full pipeline over an empty system. Acknowledge and exit early.

## Process

### 1. Garbage Collect

Archive stale data per glacier rules. All glacier files need YAML frontmatter.

**Observations — archive by primary tag:**
- Any `observations.md` >50 entries → group oldest by primary tag → `glacier/{domain}/observations-{tag}.md`

**Other files:**
- `action-items.md` >10 completed → `glacier/{domain}/action-items-done.md`
- `entities.md` inactive 6+ months → `glacier/{domain}/entities-inactive.md`

### 2. Prune Hot Memory

Keep ALL `hot-memory.md` files under 50 lines.

**Pruning priority:**
1. Resolved items (strikethrough, "DONE", "RESOLVED")
2. Past events (dates already occurred)
3. SSOT violations (same fact in hot-memory AND canonical file)
4. Stale entries (not referenced 14+ days)
5. Low-signal entries (FYI with no action or deadline)

**Where trimmed entries go:**
- Lasting value → append to `observations.md`
- Purely historical → let them go
- Never silently delete — move or note in debrief

### 3. Surface Opportunities

Review all `action-items.md` across every domain:
- **Stale items** (open >2 weeks): list with age and suggested action
- **Dormant domains** (0 observations in >4 weeks): flag
- **Health escalation** (open >6 months): flag with urgency
- **Birthday prep** (<2 weeks away): pull interests, suggest ideas

### 4. Temporal Validity Sweep

Scan ALL memory files (hot-memory, action-items, entities, threads) for `<!-- until:YYYY-MM-DD -->` and `<!-- until:YYYY-MM-DD grace:N -->` markers:

1. **Compute expiry**: `until_date + grace_days` (grace defaults to 0)
2. **If expired**: remove the line from its current file
   - If the line has lasting value → append to `observations.md` with `[archived]` tag
   - If purely temporal (event countdown, temporary state) → discard
3. **If expiring within 7 days**: leave in place but add to debrief as "expiring soon"

This is deterministic — no judgment needed. Date math only.

**Do NOT touch `<!-- from:YYYY-MM-DD -->` markers** — those are stable-since markers and never expire.

### 5. Rebuild Indexes (Deterministic)

Rebuild ALL indexes from source of truth — no LLM judgment, pure data extraction.

**5a. Glacier Index**

Scan `memory/glacier/**/*.md`, extract YAML frontmatter, write `memory/glacier/index.md`:

```markdown
# Glacier Index
<!-- Auto-generated. Do not edit. -->
<!-- Last updated: YYYY-MM-DD -->

| File | Domain | Type | Tags | Date Range | Entries | Summary |
|------|--------|------|------|------------|---------|---------|
```

**5b. Domain INDEX.md files**

For each domain directory, read every `.md` file's `<!-- L0: ... -->` header and write `memory/{domain}/INDEX.md`:

```markdown
# {Domain} Index
<!-- Auto-generated from L0 headers. Do not edit. -->
<!-- Last updated: YYYY-MM-DD -->

| File | Summary |
|------|---------|
| hot-memory.md | Current state and priorities |
| observations.md | Timestamped events and learnings |
```

**Key principle**: These indexes are DETERMINISTIC — computed from L0 headers that already exist. If a file has no L0 header, list it with summary "(no L0 header — needs one)". Never invent summaries; just reflect what's there.

This prevents index drift — the failure mode where LLM-generated indexes silently go stale because the generation step was skipped or failed.

### 6. Link Audit

For each non-glacier memory file:
1. Entity mentions matching `### Name` headers → add `[[links]]` if missing
2. Cross-domain references → add cross-domain links
3. Action item references → link observations to tasks

### 7. Entity Format Enforcement

Scan all `entities.md`:
1. **3-line max**: Entries >3 lines → compress or flag for thread promotion
2. **Glacier candidates**: Inactive >6 months → move to glacier (leave stub)
3. **Missing metadata**: Flag entries without `status:` or `last:` fields

### 8. Rebuild Link Index

Scan all memory files (exclude glacier) for `[[wiki-links]]`. Write `memory/link-index.md`:

```markdown
# Memory Link Index
<!-- Auto-generated. Do not edit. -->
<!-- Last updated: YYYY-MM-DD -->

| Target | Linked from |
|--------|-------------|
```

### 9. L0 Header Maintenance

Check all files for missing `<!-- L0: ... -->` headers. Add where missing:
- Read file content
- Write one-line summary (max 80 chars)
- Place as first line

### 10. Debrief

Summarize:
- What was archived/pruned
- Upcoming events flagged
- Action items surfaced
- Links added
- Files modified (list each one)
