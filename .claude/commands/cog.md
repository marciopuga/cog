---
description: Set up Cog memory, folders for the areas of your life and work
---
# /cog: set up memory

1. Find memory (`$COG_HOME/memory`, else `~/cog/memory`). If it's missing, tell the person to clone Cog to `~/cog` (or set `COG_HOME`) and stop.
2. Read `hot-memory.md` and `index.md`. If memory already holds content, ask what to add or change instead of starting over.
3. Ask in one message, at most three questions:
   - What do you do for work, and where?
   - Any side projects, studies or other areas you want me to keep track of?
   - What should I always know about you: name, who you live with, where?
4. For each area, create a folder (lower case, hyphens, e.g. `work/`, `studio/`). Keep it to 2-4 folders; `personal/` already exists. In each one:
   - `index.md`: frontmatter with one `l0:` line describing the folder;
   - `observations.md`, `action-items.md`, `entities.md`: copy the frontmatter and format comment from the files in `personal/`, adjusting the `l0:`.
5. Write what you learned:
   - `hot-memory.md`: a **Who** line, then one line per active area;
   - `entities.md`: the people named;
   - `facts.md`: values that will change (role, employer, city), with `from:` dates when known;
   - `events.md`: any dates mentioned that people will refer back to.
6. Run `bin/cog tidy` and show the resulting `index.md`.
7. Tell the person the two habits that matter: ask questions about their life normally, and run `/save` at the end of a session.
