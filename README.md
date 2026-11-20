# Cog

One memory for every agent and project: a folder of plain-text files and one short instruction file. There's nothing to install, and no server, database, embeddings or scripts: just markdown and the file tools your agent already has.

**[Skills](https://github.com/marciopuga/cog-skills)** for agents that load skills rather than `AGENTS.md`.

## Quick start

```bash
git clone https://github.com/marciopuga/cog ~/cog
cd ~/cog
claude            # or any agent that reads AGENTS.md
> /cog            # first run: a few questions, then it creates your folders
```

From then on, ask about your life and work as you normally would. The agent reads memory before it answers and writes new facts as it learns them. Run `/cog` at the end of a session to catch anything it missed.

If you cloned somewhere else, set `COG_HOME` (for example `export COG_HOME=~/projects/cog`).

### Use it from every project

Memory lives in one place, `~/cog/memory/`. Keep it there and don't scaffold memory inside each project.

- **Claude Code, everywhere:** add `@~/cog/AGENTS.md` to `~/.claude/CLAUDE.md`, and copy `.claude/commands/cog.md` to `~/.claude/commands/`.
- **Codex, Cursor, Gemini CLI and others:** point the agent's own instruction file at `~/cog/AGENTS.md`, or install the skill with `npx skills add marciopuga/cog-skills`.

## How it works

At the start of every session the agent reads three small things:

| Read | What it says |
|---|---|
| `memory/hot-memory.md` | What's going on now (at most 25 lines) |
| `memory/patterns.md` | How you want it to work (at most 40 lines, written by hand) |
| Every `l0:` line | The map: one line per file, giving its path and a one-line summary. It's a single search, so there's no index to keep up to date. |

The map tells it which file to open. A file over 80 lines gets its headings listed first, then only the section it needs. A name no summary mentions gets one search inside the likely folder.

Time questions need no tool, because every dated line starts with its date:
- **A value on a date:** the `facts.md` line whose `from:`/`until:` window covers that date.
- **"Before the trip":** the trip's dates from `events.md`, then the observation lines in that window.
- **"Last October":** a search for `^- 2026-10`.

That is the whole retrieval model. It works because the agent navigates rather than searches, so the design keeps every file small and every summary honest.

```
~/cog/
  AGENTS.md              the instructions (CLAUDE.md just imports it)
  memory/
    hot-memory.md        read every session
    patterns.md          read every session
    facts.md             values that change over time
    events.md            named dated anchors: trips, launches, appointments
    personal/            a folder per area of life or work
      observations.md
      action-items.md
      entities.md
      kitchen-renovation.md    topic files, as they appear
      glacier/           archives
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

The four rules:
- Absolute dates only.
- Each fact lives in one place and is linked from elsewhere.
- Links point to whole files (`[[folder/file]]`), because section links break when headings change.
- A correction rewrites the wrong line rather than adding a contradicting one.

## Staying small

There's no cleanup job. The agent keeps files within their limits whenever it writes to them:
- **Observations:** once a file passes 50 entries, the oldest move into `glacier/observations-<year>.md` until 40 remain.
- **Action items:** once more than 10 are ticked, they move to `glacier/action-items-done.md`.
- **Expired lines:** a line in `hot-memory.md` or `action-items.md` whose `until:` date has passed is ignored when read and moved to `glacier/expired.md` at the next edit.

**`/cog`** is the only command. Run it at the end of a session.
- It writes what the conversation added: a dated observation, a changed fact, a new event, an action item.
- It updates hot memory only where a fact changed, and does the upkeep above.
- It proposes a topic file when one subject has come up three times.

On first run it sets up folders from a few questions instead, and when it finds a Cog v1 folder it offers to convert it.

## Try it on the example

`examples/memory/` is a made-up person across two folders: about 35 files, archives, expired lines and a fact history. Point `COG_HOME` at a copy of it and ask questions.

## Evaluation

Twenty questions about the example person (`eval/questions.json`, answer key included). Each was asked in a fresh headless Claude Code session (Sonnet, `claude -p`) against two copies of the same memory.
- **Cog v1:** the old layout and instructions (`<!-- L0 -->` comments, `domains.yml`, per-folder hot memory and `INDEX.md`, `threads/`, `calendar.md`, values kept as History lines).
- **Cog v2:** this repo.

Both copies hold the same facts. `eval/run.py` is a development tool, not part of Cog: it rebuilds both copies and reruns everything. Per-question answers and tool calls are in `eval/results-*.jsonl`.

| | Cog v1 | Cog v2 |
|---|---|---|
| Correct | 20/20 | 20/20 |
| Tool calls, total | 42 | 37 |
| Input tokens per question (incl. cache) | 61.5k | 53.0k |
| Cost for all 20 | $1.07 | $0.95 |

| Question type | v1 tool calls | v2 tool calls | v1 tokens | v2 tokens |
|---|---|---|---|---|
| Who (4) | 8 | 9 | 59k | 61k |
| What's due (4) | 9 | 8 | 64k | 55k |
| Value on a date (4) | 10 | 6 | 71k | 46k |
| Before / during / after an event (4) | 7 | 7 | 54k | 52k |
| Current state of a topic (3) | 6 | 6 | 59k | 56k |
| Archived history (1) | 2 | 1 | 59k | 37k |

Both versions answered everything correctly. The example memory is small enough that v1 finds every answer too, so accuracy here only shows that v2 loses nothing. The difference is in the work. v2 reached the same answers with fewer reads and about 14% fewer input tokens, mostly on questions about a value on a date, where one `facts.md` line replaces searching through History sections. Each question ran once, so expect a few calls of noise either way.

During development, v2 briefly shipped a helper script for archiving and date queries. It used 32 tool calls and 47.1k tokens per question on the same questions (`eval/results-v2-script.jsonl`). That was a little cheaper, but it cost a Python dependency, and the prompt-only version keeps the accuracy.

## What was left out, and why

Earlier versions of Cog shipped about 1,700 lines of prompts. They included weekly housekeeping and reflection passes, a backlink index, self-observation logs, foresight and scenario skills, a domain manifest with keyword triggers, and a hot-memory file per folder. v2 keeps about 130 lines of prompt text and nothing else.

The rule behind the cut: a routine has to change files. One that writes a report for another routine to read doesn't make the cut.

- **Backlink index:** searching for `[[folder/file` gives backlinks on demand.
- **Generated indexes:** the `l0:` lines are the index, read with one search.
- **Self-observations, run logs, foresight, scenarios:** you can just ask the agent. When the same correction comes up twice, write it in `patterns.md`.
- **Automated pattern promotion and weekly reflection:** `/cog` works from the conversation, which is where new facts actually come from.
- **Domain manifest and keyword triggers:** an agent reading one-line summaries routes just as well.
- **Per-folder hot memory, rich frontmatter, `last_updated`:** one hot memory is enough, and a file's modification time doesn't go stale.
- **`from:`, `grace:` and `muted:` markers:** `from:` lives in `facts.md`, and instead of `grace:` you set a later `until:`.

## Upgrading from Cog v1

Run `/cog`. When it finds a v1 folder it offers to convert it:
- `<!-- L0: -->` comments become `l0:` frontmatter.
- `calendar.md` becomes `events.md`.
- `cog-meta/patterns.md` becomes `patterns.md`.
- `domains.yml`, `link-index.md`, the `INDEX.md` files and the rest of `cog-meta/` move to `glacier/legacy/`.

## Use with Obsidian

`memory/` is a valid Obsidian vault. `l0:` shows as a property, wiki-links resolve, and edits you make by hand are picked up next session.

## Credits

[OpenViking](https://github.com/volcengine/OpenViking) (L0 summaries and tiered loading) | [Zettelkasten](https://en.wikipedia.org/wiki/Zettelkasten) (topic files) | [SSOT](https://en.wikipedia.org/wiki/Single_source_of_truth) (one fact, one place)

## License

MIT
