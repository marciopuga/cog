# Cog

One memory for every agent and project: a folder of plain-text files, a short instruction file, and one small script. No server, no database and no embeddings, just files and grep.

**[Skills](https://github.com/marciopuga/cog-skills)** for agents that load skills rather than `AGENTS.md`.

## Quick start

```bash
git clone https://github.com/marciopuga/cog ~/cog
cd ~/cog
claude            # or any agent that reads AGENTS.md
> /cog            # a few questions, then it creates your folders
```

From then on, ask about your life and work as you normally would. The agent reads memory before it answers and writes new facts as it learns them. Run `/save` at the end of a session to catch anything it missed.

If you cloned somewhere else, set `COG_HOME` (for example `export COG_HOME=~/projects/cog`).

### Use it from every project

Memory lives in one place, `~/cog/memory/`. Keep it there and don't scaffold memory inside each project.

- **Claude Code, everywhere:** add `@~/cog/AGENTS.md` to `~/.claude/CLAUDE.md`, and the tidy hook to `~/.claude/settings.json`:
  ```json
  { "hooks": { "SessionStart": [ { "hooks": [ { "type": "command",
      "command": "python3 \"${COG_HOME:-$HOME/cog}/bin/cog\" tidy --quiet" } ] } ] } }
  ```
- **Codex, Cursor, Gemini CLI and others:** point the agent's own instruction file at `~/cog/AGENTS.md`, or install the skill with `npx skills add marciopuga/cog-skills`. Run tidy from cron: `0 * * * * python3 ~/cog/bin/cog tidy --quiet`.

## How it works

At the start of every session the agent reads three small files:

| File | What it says |
|---|---|
| `memory/hot-memory.md` | What's going on now (at most 25 lines) |
| `memory/patterns.md` | How you want it to work (at most 40 lines, written by hand) |
| `memory/index.md` | Every folder and file, each with a one-line summary and a line count (generated) |

The index tells it which file to open. A file over 80 lines gets `grep -n '^#'` first, then only the section it needs. A name no summary mentions gets one grep inside the likely folder. Questions about time ("what was X in March", "what happened before the trip") go to `bin/cog when`.

That is the whole retrieval model. It works because the agent navigates rather than searches, so the design keeps every file small and every summary current. Keyword search over a large tree is a weak retriever, and the archiving and the generated index exist so the agent rarely has to use it.

```
~/cog/
  AGENTS.md              the instructions (CLAUDE.md just imports it)
  bin/cog                tidy, when, migrate: one Python file, standard library only
  memory/
    index.md             generated: never edit
    hot-memory.md        read every session
    patterns.md          read every session
    facts.md             values that change over time
    events.md            named dated anchors: trips, launches, appointments
    personal/            a folder per area of life or work
      index.md           its l0: line is the folder's summary
      observations.md
      action-items.md
      entities.md
      kitchen-renovation.md    topic files, as they appear
      glacier/           archives written by bin/cog tidy
    work/
      ...
```

A folder is a domain, and nothing else acts as a manifest.

## Line formats

Every file starts with a one-key frontmatter (`l0:`, a one-line summary), then a comment that states its line format. The rule travels with the file, so any agent, or you in an editor, can follow it without loading anything else.

```markdown
---
l0: Who's who at home: family, friends, the people who help
---
<!-- Edit in place. Format: ### Name (relationship), then 1-3 lines of facts, last line last: YYYY-MM-DD -->
```

| File | Line | Edit |
|---|---|---|
| `observations.md` | `- 2026-11-20 [tag, tag]: text [[folder/file]]`, optionally `about:2026-11-18` after the tags (when it happened, not when it was written) | Append only |
| `action-items.md` | `- [ ] task \| due:2026-12-01 \| pri:high \| added:2026-11-20` | Append; tick when done |
| `entities.md` | `### Name (relationship)`, then 1-3 lines | Edit in place |
| `facts.md` | `- key: value \| from:2026-11-08 \| until: \| src:[[folder/file]] \| kind:health` | Fill `until:` on the old line, append the new one |
| `events.md` | `- beach-trip \| 2026-09-30..2026-10-06 \| note \| aka: Beach, the trip` | Append; edit in place |
| `hot-memory.md` | `- **topic** — state [[folder/file]] <!-- until:2026-11-30 -->` | Rewrite freely |
| topic file | `## Current State` (rewritten), then `## Timeline` (`- 2026-11-20: ...`, appended) | As shown |

The four rules are: absolute dates only; each fact lives in one place and is linked from elsewhere; links point to whole files (`[[folder/file]]`), because section links break when headings change; and a correction rewrites the wrong line rather than adding a contradicting one.

All of these formats are defined once, in `bin/cog`. Every subcommand uses the same definitions, so the checker and the tools can't drift apart.

## The tools

**`bin/cog tidy`** is deterministic, needs no model, and is safe to run any time. It finishes in well under a second.

1. Observations: when a file has more than 50 entries, it moves the oldest out until 40 remain, into `glacier/observations-<first tag>.md`. It writes the glacier file first and removes lines from the source after.
2. Action items: once more than 10 are ticked, it moves them to `glacier/action-items-done.md`.
3. Expiry: lines in `hot-memory.md` and `action-items.md` whose `until:` date has passed move to `glacier/expired.md`, dated with the day they expired.
4. Index: it rebuilds `memory/index.md`. A folder of more than 12 files folds into one row plus its own `index.md`.
5. Check: it reports every line that breaks its file's format, with its location. It never writes markers into your files.

`--dry-run` prints the plan without writing anything. `--quiet` prints only when something moved or needs fixing, which is what the session-start hook uses.

**`bin/cog when`** answers questions about dates from the files:

```
bin/cog when asof 2026-07-01 heron-team-size      # a fact on a date
bin/cog when asof offsite role                    # ...or on an event's date
bin/cog when timeline mortgage-rate               # every value a fact has had
bin/cog when before:the-race after:2026-09-25 running
bin/cog when during:Saltmarsh                     # an event's name or any aka:
bin/cog when last:7d                              # dated lines in a window
bin/cog when                                      # upcoming events, due soon, overdue
```

It reads the line's own date, `about:`, `due:`, `from:`/`until:`, and dates written in the text ("5 Dec", "29 Sep–6 Oct", "July 2026"). Add `--glacier` to include archives.

**`/save`** is the one prompt routine. Run it at the end of a session. It writes what the conversation added (a dated observation, a changed fact, a new event, an action item), updates hot memory only where a fact changed, and proposes a topic file when one subject has come up three times.

**`/cog`** sets up folders from a few questions.

## Try it on the example

`examples/memory/` is a made-up person across two folders: about 35 files, an over-full observations file, expired lines and a fact history.

```bash
bin/cog --root examples/memory tidy --dry-run
bin/cog --root examples/memory when asof offsite role
bin/cog --root examples/memory when during:Saltmarsh
```

Tests run against a temporary copy of it: `python3 -m unittest discover tests`.

## Evaluation

Twenty questions about the example person (`eval/questions.json`, answer key included), each asked in a fresh headless Claude Code session (Sonnet, `claude -p`) against two copies of the same memory: the v1 layout and instructions (`<!-- L0 -->` comments, `domains.yml`, per-folder hot memory and `INDEX.md`, `threads/`, `calendar.md`, values kept as History lines) and v2. Both copies hold the same facts. `python3 eval/run.py` rebuilds both and reruns everything; per-question answers and tool calls are in `eval/results-*.jsonl`.

| | Cog v1 | Cog v2 |
|---|---|---|
| Correct | 20/20 | 20/20 |
| Tool calls, total | 45 | 32 |
| Input tokens per question (incl. cache) | 64.8k | 47.1k |
| Cost for all 20 | $1.09 | $0.88 |

| Question type | v1 tool calls | v2 tool calls | v1 tokens | v2 tokens |
|---|---|---|---|---|
| Who (4) | 10 | 7 | 69k | 51k |
| What's due (4) | 9 | 7 | 67k | 49k |
| Value on a date (4) | 10 | 5 | 70k | 40k |
| Before / during / after an event (4) | 7 | 6 | 54k | 46k |
| Current state of a topic (3) | 7 | 6 | 66k | 54k |
| Archived history (1) | 2 | 1 | 59k | 36k |

Both versions answered everything correctly. This example memory is small enough that v1 finds every answer too, so accuracy here only shows that v2 loses nothing. The difference is in the work: v2 reached the same answers with fewer reads and about a quarter fewer input tokens. The gain is largest on questions about values on a date, where `bin/cog when asof` replaces searching through History sections. Each question ran once, so expect a few calls of noise either way.

## What was left out, and why

Earlier versions of Cog shipped about 1,700 lines of prompts: weekly housekeeping and reflection passes, a backlink index, self-observation logs, foresight and scenario skills, a domain manifest with keyword triggers, and a hot-memory file per folder. v2 keeps about 130 lines of prompt text and a 500-line script. The rule behind the cut is that a routine has to change files. One that writes a report for another routine to read doesn't make the cut.

- **Backlink index:** `grep -rn '[[folder/file'` gives backlinks on demand.
- **Self-observations, run logs, foresight, scenarios:** you can just ask the agent. When the same correction comes up twice, write it in `patterns.md`.
- **Automated pattern promotion and weekly reflection:** `/save` works from the conversation, which is where new facts actually come from.
- **Domain manifest and keyword triggers:** an agent reading one-line folder summaries routes just as well.
- **Per-folder hot memory, rich frontmatter, `last_updated`:** one hot memory is enough, and a file's modification time doesn't go stale.
- **`from:`, `grace:` and `muted:` markers:** `from:` lives in `facts.md`, and instead of `grace:` you set a later `until:`.

## Upgrading from Cog v1

```bash
bin/cog migrate          # dry run: prints every step
bin/cog migrate --apply
```

The script converts `<!-- L0: -->` comments to `l0:` frontmatter, folds `grace:N` into `until:`, and turns `domains.yml` labels into each folder's `index.md`. It merges `calendar.md` into `events.md`, where `tidy` flags the lines to rewrite as events, and moves `cog-meta/patterns.md` to `patterns.md`. `cog-meta/`, `link-index.md` and `domains.yml` go to `glacier/legacy/`. Afterwards it runs `tidy`.

## Use with Obsidian

`memory/` is a valid Obsidian vault. `l0:` shows as a property, wiki-links resolve, and edits you make by hand are picked up next session.

## Credits

[OpenViking](https://github.com/volcengine/OpenViking) (L0 summaries and tiered loading) | [Zettelkasten](https://en.wikipedia.org/wiki/Zettelkasten) (topic files) | [SSOT](https://en.wikipedia.org/wiki/Single_source_of_truth) (one fact, one place)

## License

MIT
