# Cog

One memory, not one per tool. A centralised, plain-text memory layer shared across all your AI agents and projects.

**[Documentation](https://lab.puga.com.br/cog/)** | **[Skills](https://github.com/marciopuga/cog-skills)** | **[Why Text](https://lab.puga.com.br/cog/#/why-text)**

## What is Cog?

AI agents have memory now — but it's siloed. Each tool remembers things its own way, locked inside its own project. Switch tools or start a new project, and you're re-explaining yourself. Cog gives you one shared memory — structured plain-text files that any agent can read, search, and maintain.

Three primitives:
- **L0 headers** — progressive context loading (scan before you read)
- **Three tiers** — hot (always loaded), warm (on demand), glacier (archived)
- **Single source of truth** — each fact in one place, cross-referenced via wiki-links

No server, no database, no application code. Just markdown files with conventions.

## Quick Start

```bash
git clone https://github.com/marciopuga/cog ~/cog
cd ~/cog
npx skills add marciopuga/cog-skills
```

Start your agent and run `/cog` to bootstrap your domains. Your agent now has persistent memory at `~/cog/memory/`.

**Claude Code users:** the clone already ships the skills at `.claude/commands/` (vendored from [cog-skills](https://github.com/marciopuga/cog-skills), the canonical source, under their unprefixed names — `/reflect`, `/housekeeping`, ...). The `npx skills add` step is what installs them for other agents, where they carry a `cog-` prefix (`/cog-reflect`, ...).

**One folder, many projects.** `~/cog` is your agent's single brain — it works across every project and session. Don't scaffold memory inside each project. That fragments your context. One place where everything connects.

### Custom install location

If you cloned somewhere other than `~/cog`, set the `COG_HOME` env var:

```bash
export COG_HOME=~/projects/cog  # add to ~/.zshrc or ~/.bashrc
```

## Supported Agents

`npx skills add` auto-detects your agent and installs skills into its native format via [skills.sh](https://skills.sh):

- Claude Code
- Codex (OpenAI)
- Cursor
- Windsurf
- Gemini CLI
- GitHub Copilot
- Opencode
- Cowork (Claude Desktop)

All agents read the same memory folder (`$COG_HOME/memory/`, defaults to `~/cog/memory/`).

## Use with Obsidian

The `memory/` folder is a valid Obsidian vault. Wiki-links (`[[domain/file]]`) work natively in Obsidian's graph view and link resolution.

You can:
- Clone `~/cog` and open `memory/` as a vault in Obsidian
- Or clone directly into an existing vault as a subfolder
- Edit files manually in Obsidian — your agent picks up changes next session
- Use Obsidian's graph view to visualize connections between memory files

The folder works as both an AI memory system and a human knowledge base. No conflict — they're the same markdown files.

## Memory Structure

```
~/cog/memory/
├── hot-memory.md           ← Always loaded. <50 lines. Current state.
├── domains.yml             ← Domain manifest (SSOT)
├── link-index.md           ← Backlink index (auto-generated)
├── personal/               ← Warm. Loaded when relevant.
│   ├── hot-memory.md
│   ├── observations.md     ← Append-only event log
│   ├── action-items.md     ← Tasks
│   ├── entities.md         ← People, places, things
│   ├── threads/            ← Synthesis files for recurring topics
│   ├── INDEX.md            ← Domain L0 index: file, line count, summary; subfolders inline or folded (auto-generated)
│   └── ...
├── work/                   ← Your work domains (created by /cog)
├── cog-meta/               ← System self-knowledge
│   ├── patterns.md         ← Distilled rules
│   ├── self-observations.md
│   ├── action-items.md     ← System tasks (over-cap metrics, ideas)
│   ├── run-log.md          ← Pipeline run log
│   ├── foresight-nudge.md  ← Latest on-demand nudge
│   ├── scenarios/          ← Active decision simulations
│   └── INDEX.md
└── glacier/                ← Cold archive. Indexed.
    └── index.md
```

## Skills

Installed via `npx skills add marciopuga/cog-skills` (names carry a `cog-` prefix) or bundled with this repo for Claude Code (unprefixed):

| Skill | Purpose |
|-------|---------|
| `/cog` | Memory conventions + setup — bootstraps domains, folders, and their indexes (no per-domain skills; routing is `domains.yml` → `INDEX.md`) |
| `/housekeeping` | Weekly, automated — archive, prune, rebuild indexes, sweep expired facts, report a Health table |
| `/reflect` | Weekly, automated (same session) — consolidate observations into patterns, fix contradictions, raise threads, close scenarios |
| `/foresight` | On demand — one cross-domain strategic nudge, flags decisions worth simulating |
| `/scenario` | On demand — branch a decision into 2-3 modeled paths |
| `/history` | On demand — deep memory search, piece together a narrative across files |

The Claude Code bundle also includes writing extras (`/explainer`, `/humanizer`) and a `/commit` utility.

## Optional: Automated Maintenance

One scheduled pulse. **Run housekeeping → reflect in the same session** so reflect sees freshly-pruned state:

```bash
# Weekly maintenance pulse
0 23 * * 0  cd "${COG_HOME:-$HOME/cog}" && claude -p "/housekeeping then /reflect"
```

Foresight, scenario, and history run when you ask for them. Housekeeping's Health table is the system audit.

(Skill names carry a `cog-` prefix when installed via skills.sh: `/cog-housekeeping then /cog-reflect`.)

The pipeline is optional. Cog works without it — but running it regularly keeps memory clean and surfaces insights you'd miss.

## How It Works

`npx skills add` installs SKILL.md files that teach your agent the conventions: how to tier memory, when to consolidate, how to route queries, where to write facts. The `memory/` directory is the state that emerges from following these rules over time.

Everything is observable. The agent never loads the whole tree — it climbs a ladder of small reads, each one saying what to open next:

```
memory/hot-memory.md          always          → what's going on
memory/domains.yml            always          → which folders exist, what wakes them
memory/{domain}/INDEX.md      domain matched  → which file (L0 + line count, subfolders, threads, glacier pointer)
grep -n "^#" file             files >80 lines → which section
the file, or one section      L2              → the content
```

Large subfolders fold into one index row of file names plus their own `INDEX.md`, so a domain index stays one read however many files it grows. A query about your own life with no trigger match defaults to `personal`; a name no L0 mentions is found with one grep inside that domain, never across the tree.

Run `grep -rn "<!-- L0:" ~/cog/memory/` yourself to see every summary the agent can reach. No black box.

## Verified on Real Memory

The conventions were tested against a copy of a real personal memory — 53 files, ~8,600 lines, eight nested subfolders, 23 glacier archives — with headless runs tracing every tool call, then one full weekly pulse.

| What was measured | Result |
|-------------------|--------|
| Retrieval queries (overview, person, history, nested folder, glacier, proper noun, off-topic) | 10/10 answered correctly |
| Memory loaded per query | 5–10k tokens of a ~100k-token corpus; off-topic queries load nothing |
| Domain index after subfolder support | 39 rows, one read, every file reachable in ≤2 reads |
| Housekeeping's rebuilt indexes vs a deterministic reference | byte-identical |
| Weekly pulse (housekeeping → reflect) | hot-memory 59→49 lines, 26 expired markers swept, 22 archive L0s added, 12 patterns seeded, Health table with nothing over cap |

What it found became rules: subfolder-aware indexes, default-to-personal, the one sanctioned grep, headers-before-cat, L0 after frontmatter. The remaining risk is model discipline on files over 80 lines — text rules steer, they don't enforce — which is why the pipeline keeps files small and splits recurring topics into threads.

## Credits

Built on research: [RLM](https://arxiv.org/abs/2512.24601) (recursive memory) | [A-MEM](https://arxiv.org/abs/2502.12110) (back-linking) | [OpenViking](https://github.com/volcengine/OpenViking) (L0 tiered loading) | [Zettelkasten](https://en.wikipedia.org/wiki/Zettelkasten) (threads) | [SSOT](https://en.wikipedia.org/wiki/Single_source_of_truth) (canonical facts)

## Citation

```
Cog: Plain-Text Memory System for AI Agents
https://github.com/marciopuga/cog
Marcio Puga, 2026
```

## License

MIT
