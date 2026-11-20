---
description: Save what this conversation added to memory
---
# /save

Write down what this conversation taught you that memory doesn't have yet. Follow `AGENTS.md`: the right file, its line format, absolute dates.

1. If you haven't this session, read `hot-memory.md` and the `l0:` map.
2. Go through the conversation. For each thing that happened or was decided, search the owning folder first. If it's missing, append one dated line to that folder's `observations.md` (with `about:DATE` when it happened on another day).
3. Changes:
   - a value changed: close the old line in `facts.md` (`until:`), then append the new one;
   - a new date people will refer back to: a line in `events.md`, with `aka:` names;
   - an open ask or promise: `action-items.md`; something finished: tick it and add `done:`;
   - a new person: `entities.md`;
   - a topic file whose state moved: rewrite its `## Current State`, then append to `## Timeline`.
4. Rewrite `hot-memory.md` lines only where a fact changed. Remove lines that are done, and move lines whose `until:` date has passed to `glacier/expired.md`. At most 25 lines.
5. Keep every file you touched within its limits ("Keep it small" in `AGENTS.md`): observations past 50, more than 10 ticked items, expired `until:` lines.
6. If one subject now has 3 or more observations and no topic file, propose one (file name and `l0:`). Create it only after a yes.
7. If the person corrected you on the same thing twice, propose a line for `patterns.md`.
8. Reply with what you wrote, one line per file, including anything archived. If nothing was new, write nothing and say so.
