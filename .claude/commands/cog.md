---
description: Set up Cog memory, folders for the areas of your life and work
---
# /cog: set up memory

1. Find memory (`$COG_HOME/memory`, else `~/cog/memory`). If it's missing, tell the person to clone Cog to `~/cog` (or set `COG_HOME`) and stop.
2. If memory comes from an older Cog (`domains.yml`, `cog-meta/`, `<!-- L0: -->` comments), offer to convert it first, then convert only after a yes:
   - `<!-- L0: text -->` becomes frontmatter `l0: text`;
   - `calendar.md` lines become `events.md` lines, and `cog-meta/patterns.md` becomes `patterns.md`;
   - `domains.yml`, `link-index.md`, `INDEX.md` files and the rest of `cog-meta/` move to `glacier/legacy/`.
3. Read `hot-memory.md` and the `l0:` map. If memory already holds content, ask what to add or change instead of starting over.
4. Ask in one message, at most three questions:
   - What do you do for work, and where?
   - Any side projects, studies or other areas you want me to keep track of?
   - What should I always know about you: name, who you live with, where?
5. For each area, create a folder (lower case, hyphens, e.g. `work/`, `studio/`). Keep it to 2-4 folders; `personal/` already exists. In each one create `observations.md`, `action-items.md` and `entities.md`, copying the frontmatter and format comment from the files in `personal/` and adjusting the `l0:`.
6. Write what you learned:
   - `hot-memory.md`: a **Who** line, then one line per active area;
   - `entities.md`: the people named;
   - `facts.md`: values that will change (role, employer, city), with `from:` dates when known;
   - `events.md`: any dates mentioned that people will refer back to.
7. Show the `l0:` map of what now exists.
8. Tell the person the two habits that matter: ask questions about their life normally, and run `/save` at the end of a session.
