# Cog: your memory

You have a persistent memory: one folder of plain-text files, shared by every agent and project. Read it before you answer anything about the person's life or work. Write to it as soon as you learn something worth keeping.

## Where

Memory is `$COG_HOME/memory/` if `COG_HOME` is set, else `~/cog/memory/`. Never create memory anywhere else. Paths below are relative to `memory/`.

## Read at the start of every session

1. `hot-memory.md`: what is going on now.
2. `patterns.md`: how the person wants you to work.
3. The map: search the memory for lines starting `l0:`, skipping `glacier/` (`grep -r '^l0:' --include='*.md' --exclude-dir=glacier ~/cog/memory`). That's one line per file, giving its path and a one-line summary.

These three are small, and together they tell you which file to open next.

## Find

- Pick at most two folders from the map, then the file whose summary fits. Over 80 lines: list its headings (`grep -n '^#'`) and read only the section you need.
- People: the folder's `entities.md`. Tasks and deadlines: its `action-items.md`. A subject's current state: its topic file (`## Current State`).
- A name or word that no summary mentions: search for it inside the likely folder, not across the whole tree.
- History: the folder's `observations.md`, then its `glacier/`.
- If memory doesn't have the answer, say so. Don't guess. Mention the file you used.

Questions about time. Every dated line starts with its date, so a date prefix is a search:

- **A value on a date** ("what was X in March"): find the key in `facts.md`. The answer is the line where `from:` ≤ date and `until:` is empty or later than the date.
- **Every value something has had:** all `facts.md` lines with that key, in order.
- **Before, after or during an event:** find the event in `events.md` by its name or an `aka:` to get its dates. Then read observation lines in that window, matching on the line date or on `about:` when present.
- **A window** ("last week", "in October"): search observations for the date prefix (`^- 2026-10`). Include `glacier/` for older periods.
- **Upcoming, due soon, overdue:** compare `due:` in `action-items.md` and the dates in `events.md` with today's date.

## Files

Every file starts with frontmatter that holds one key, `l0:` (a one-line summary of at most 100 characters), followed by a comment that states its line format. Follow that comment.

```
memory/
  hot-memory.md     current state, at most 25 lines
  patterns.md       rules for working with the person, at most 40 lines
  facts.md          values that change over time
  events.md         named dated anchors: trips, launches, appointments
  <folder>/         one per area of life or work (personal/, work/, ...)
    observations.md  action-items.md  entities.md  <topic>.md
    glacier/        archives: read when the question is about the past
```

| File | Line format | Edit |
|---|---|---|
| `observations.md` | `- 2026-11-20 [tag, tag]: text [[folder/file]]`. Add `about:2026-11-18` after the tags when it happened on another day | Append only |
| `action-items.md` | `- [ ] task \| due:2026-12-01 \| pri:high \| added:2026-11-20`. Done: `- [x] ... \| done:2026-11-22` | Append; tick when done |
| `entities.md` | `### Name (relationship)`, then 1-3 lines, the last being `last: 2026-11-20` | Edit in place |
| `facts.md` | `- key: value \| from:2026-11-08 \| until: \| src:[[folder/file]] \| kind:health` | Fill `until:` on the old line, append the new line |
| `events.md` | `- beach-trip \| 2026-09-30..2026-10-06 \| note \| aka: Beach, the trip` | Append; edit in place |
| `hot-memory.md` | `- **topic** — state [[folder/file]]`. Time-bound lines end with `<!-- until:2026-11-30 -->` | Rewrite freely |
| `<topic>.md` | `## Current State` (prose), then `## Timeline` (`- 2026-11-20: text`) | Rewrite the state; append to the timeline |

## Write

Write immediately, into the file that owns the fact, in that file's format.

- Something happened or was decided: a dated line in that folder's `observations.md`.
- A value changed (a role, a dose, a rate, a size, an address): add it to `facts.md`. Set `until:` on the old line to the change date, then append the new line with `from:` set to the same date. Keys are lower-case-hyphenated and reused across values.
- A date people will refer back to ("before the trip", "since the launch"): `events.md`, with `aka:` for the names they use.
- An ask or a promise: `action-items.md`. Done: tick it and add `done:`.
- A new person: `entities.md`.
- A subject that keeps coming back: propose a topic file `<folder>/<topic>.md` and create it only after a yes.
- Current state that matters now: `hot-memory.md`. Remove lines that are no longer true.
- The same correction twice: a rule in `patterns.md`.
- A new file always gets its `l0:` line and format comment, or it won't show on the map.

Rules:
- Absolute dates only (`2026-11-20`, never "yesterday" or "in 3 days").
- One fact lives in one place. Elsewhere, link to it with `[[folder/file]]` (whole files, never `#sections`).
- A correction rewrites the wrong line rather than adding a contradicting one (observations: append the correction).
- Never edit anything in `glacier/` except to append archives.

## Keep it small

Do this whenever you write to one of these files. There is no separate cleanup step.

- `observations.md` past 50 entries: move the oldest until 40 remain into `<folder>/glacier/observations-<year>.md`, by each line's year. Append them to the glacier file first, then remove them from the source.
- More than 10 ticked items in `action-items.md`: move the ticked ones to `<folder>/glacier/action-items-done.md`.
- A line in `hot-memory.md` or `action-items.md` whose `until:` date has passed: ignore it when reading. Move it to `expired.md` in the `glacier/` beside that file the next time you edit it.
- A glacier file you create gets an `l0:` line too, such as "Personal observations from 2025".

`/save` at the end of a session writes down what the conversation added and does this upkeep.
