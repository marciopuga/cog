# Cog

A plain-text memory system for AI agents. Clone it, point your agent at it, start remembering.

**[Documentation](https://lab.puga.com.br/cog/)** | **[Skills](https://github.com/marciopuga/cog-skills)** | **[Why Text](https://lab.puga.com.br/cog/#/why-text)**

## What is Cog?

Every new AI chat starts from scratch. Cog fixes that — persistent memory using plain text files that any agent can read and write.

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

Start your agent and run `/setup` to bootstrap your domains. Your agent now has persistent memory at `~/cog/memory/`.

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
├── personal/               ← Warm. Loaded when relevant.
│   ├── hot-memory.md
│   ├── observations.md     ← Append-only event log
│   ├── action-items.md     ← Tasks
│   ├── entities.md         ← People, places, things
│   └── ...
├── work/                   ← Your work domains
├── cog-meta/               ← System self-knowledge
│   ├── patterns.md         ← Distilled rules
│   └── self-observations.md
└── glacier/                ← Cold archive. Indexed.
    └── index.md
```

## Optional: Automated Maintenance

Schedule pipeline skills with cron. **Run housekeeping → reflect in the same session** so reflect sees freshly-pruned state:

```bash
# Weekly maintenance pulse
0 23 * * 0  cd ~/cog && claude -p "/housekeeping then /reflect"

# Monthly architecture audit
0  1 1 * *  cd ~/cog && claude -p "/evolve"
```

The pipeline is optional. Cog works without it — but running it regularly keeps memory clean and surfaces insights you'd miss.

## How It Works

`npx skills add` installs SKILL.md files that teach your agent the conventions: how to tier memory, when to consolidate, how to route queries, where to write facts. The `memory/` directory is the state that emerges from following these rules over time.

Everything is observable — run `grep -rn "<!-- L0:" ~/cog/memory/` and you see exactly what your agent sees. No black box.

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
