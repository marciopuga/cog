# Cog

A plain-text memory system for AI agents. Clone it, point your agent at it, start remembering.

**[Documentation](https://cog.puga.com.br)** | **[Skills](https://github.com/marciopuga/cog-skills)** | **[Why Text](https://cog.puga.com.br/#/why-text)**

## What is Cog?

Every new AI chat starts from scratch. Cog fixes that — persistent memory using plain text files that any agent can read and write.

Three primitives:
- **L0 headers** — progressive context loading (scan before you read)
- **Three tiers** — hot (always loaded), warm (on demand), glacier (archived)
- **Single source of truth** — each fact in one place, cross-referenced via wiki-links

No server, no database, no application code. Just markdown files with conventions.

## Quick Start

```bash
# 1. Clone the memory folder
git clone https://github.com/marciopuga/cog ~/cog

# 2. Install the memory skill (any agent)
npx skills add marciopuga/cog-skills --skill cog-memory

# 3. Bootstrap your domains interactively
npx skills add marciopuga/cog-skills --skill cog-setup
```

Then start a conversation. Your agent now has persistent memory at `~/cog/memory/`.

### Custom install location

If you cloned somewhere other than `~/cog`, set the `COG_HOME` env var:

```bash
export COG_HOME=~/projects/cog  # add to ~/.zshrc or ~/.bashrc
```

The `cog-setup` skill will detect this and guide you through it.

## Supported Agents

Cog uses the [SKILL.md](https://agentskills.io/specification) standard via [skills.sh](https://skills.sh):

| Agent | How it loads |
|-------|-------------|
| **Claude Code** | Reads `CLAUDE.md` natively + skills via `npx skills add` |
| **Cowork** | Open `~/cog` folder — reads `CLAUDE.md` natively |
| **Codex** | Skills install to agent, or use `AGENTS.md` |
| **Cursor** | Skills install, or reference in `.cursorrules` |
| **Windsurf** | Skills install, or reference in `.windsurfrules` |
| **Gemini CLI** | Skills install to agent |
| **GitHub Copilot** | Skills install to agent |
| **Opencode** | Skills install to `.opencode/skills/` |

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

Install pipeline skills to keep memory clean:

```bash
npx skills add marciopuga/cog-skills --skill cog-housekeeping
npx skills add marciopuga/cog-skills --skill cog-reflect
npx skills add marciopuga/cog-skills --skill cog-evolve
npx skills add marciopuga/cog-skills --skill cog-foresight
```

Schedule with cron using any agent's headless mode:

```bash
# Weekly maintenance
0 23 * * 0  claude -p "/cog-housekeeping"    # or: codex exec "/cog-housekeeping"
0  0 * * 0  claude -p "/cog-reflect"         # or: codex exec "/cog-reflect"
```

The pipeline is optional. Cog works without it — but running it regularly keeps memory clean and surfaces insights you'd miss.

## How It Works

Your agent reads the cog-memory skill (installed via skills.sh) which teaches it the conventions: how to tier memory, when to consolidate, how to route queries, where to write facts. The `memory/` directory is the state that emerges from following these rules over time.

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
