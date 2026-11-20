---
description: Cog memory. Saves what this conversation added; sets memory up on first run
---
# /cog

Cog lives in `$COG_HOME`, else `~/cog`. If it's missing, tell the person to clone https://github.com/marciopuga/cog to `~/cog` (or set `COG_HOME`) and stop. Follow its `AGENTS.md`: the right file, its line format, absolute dates. Read it first if it isn't already in your instructions.

Read `hot-memory.md` and the `l0:` map if you haven't this session, then pick one path.

## Older Cog folder (`domains.yml`, `cog-meta/`, `<!-- L0: -->` comments)

Offer to convert it, and convert only after a yes:
- `<!-- L0: text -->` becomes frontmatter `l0: text`;
- `calendar.md` lines become `events.md` lines, and `cog-meta/patterns.md` becomes `patterns.md`;
- each folder's `label` in `domains.yml` becomes the `l0:` of a new `<folder>/index.md`;
- `domains.yml`, `link-index.md`, the old `INDEX.md` files and the rest of `cog-meta/` move to `glacier/legacy/`.

Then continue with Save.

## First run (`hot-memory.md` has no entries yet)

1. Ask in one message, at most three questions:
   - What do you do for work, and where?
   - Any side projects, studies or other areas you want me to keep track of?
   - What should I always know about you: name, who you live with, where?
2. Create a folder for each area (lower case, hyphens, e.g. `work/`, `studio/`), 2-4 in all; `personal/` already exists. In each one create `index.md` (only an `l0:` line saying what the folder holds), `observations.md`, `action-items.md` and `entities.md`, copying the frontmatter and format comment from `personal/` and adjusting the `l0:`.
3. Write what you learned: a **Who** line and one line per area in `hot-memory.md`, people in `entities.md`, changeable values (role, employer, city) in `facts.md`, and dates people will refer back to in `events.md`.
4. Show the `l0:` map. Tell the person: ask about your life normally, and run `/cog` at the end of a session.

## Save (every other time)

1. Go through the conversation. For each thing that happened or was decided, search the owning folder first. If it's missing, append one dated line to that folder's `observations.md` (with `about:DATE` when it happened on another day).
2. Changes:
   - a value changed: close the old line in `facts.md` (`until:`), then append the new one;
   - a new date people will refer back to: a line in `events.md`, with `aka:` names;
   - an open ask or promise: `action-items.md`; something finished: tick it and add `done:`;
   - a new person: `entities.md`;
   - a topic file whose state moved: rewrite its `## Current State`, then append to `## Timeline`.
3. Rewrite `hot-memory.md` lines only where a fact changed. Remove lines that are done, and move lines whose `until:` date has passed to `glacier/expired.md`. At most 25 lines.
4. Keep every file you touched within its limits ("Keep it small" in `AGENTS.md`).
5. If one subject now has 3 or more observations and no topic file, propose one (file name and `l0:`). Create it only after a yes.
6. If the person corrected you on the same thing twice, propose a line for `patterns.md`.
7. Reply with what you wrote, one line per file, including anything archived. If nothing was new, write nothing and say so.
