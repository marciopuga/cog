# Cog

Persistent memory, self-reflection, and foresight for Claude Code — the first layer of continuous awareness for AI agents.

**[Documentation](https://lab.puga.com.br/cog)** | **[Why Text](https://lab.puga.com.br/cog/#/why-text)** | **[Credits & Inspiration](https://lab.puga.com.br/cog/#/credits)**

## What is Cog?

Cog is a set of instructions that teach Claude how to build and maintain a scalable memory architecture — from scratch, through conversation alone.

There is no server, no runtime, no application code. `CLAUDE.md` contains the conventions — how to tier memory, when to condense, how to route queries, when to archive. The skill files (`.claude/commands/*.md`) are more instructions that teach Claude specific workflows: reflection, foresight, housekeeping, self-evolution. Claude reads these instructions and follows them to organize, maintain, and grow a persistent knowledge base across sessions.

The architecture isn't implemented in code. It's described in plain text, and Claude executes it. This means you can read exactly how every decision gets made, modify any rule by editing a markdown file, and watch the model organize its own knowledge in real time. Everything is [plain text by design](https://lab.puga.com.br/cog/#/why-text).

The real experiment is what happens when you give an AI clear conventions for memory management and let it self-evolve — reflecting on its own behavior, auditing its own rules, and improving how it operates over time.

## Quick Start

Requires [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview).

```bash
git clone https://github.com/marciopuga/cog
cd cog
```

Open the project in Claude Code, then:

```
/setup
```

Cog will ask about your life and work — company, side projects, what you want to track. From that conversation, it generates everything: domain manifest, memory directories, skill files, and routing table.

That's it. Start talking.

### Permissions

Cog ships with `.claude/settings.json` that pre-approves the tools it needs — file reads, writes, edits, search, and git operations. When you first open the project, Claude Code will ask you to accept these project-level permissions. Say yes once and you won't be interrupted again.

If you'd rather review everything manually, delete `.claude/settings.json` and Claude Code will prompt for each operation individually.

## How It Works

`CLAUDE.md` defines the conventions below. Claude reads them at the start of every session and follows them to decide where to store facts, when to condense, how to route queries, and when to archive. The `memory/` directory is the state that emerges from following these rules over time.

### Three-Tier Memory

```
memory/
├── hot-memory.md           ← Always loaded. <50 lines. What matters right now.
├── personal/               ← Warm. Loaded when relevant.
│   ├── hot-memory.md
│   ├── observations.md     ← Append-only event log
│   ├── action-items.md     ← Tasks with due dates
│   ├── entities.md         ← People, places, things
│   └── ...
├── work/acme/              ← Your work domain (created by /setup)
│   └── ...
└── glacier/                ← Cold. Archived, indexed, retrieved on demand.
    └── index.md
```

- **Hot**: Loaded every conversation. Current state, top priorities.
- **Warm**: Domain-specific files loaded when a skill activates.
- **Glacier**: YAML-frontmattered archives. Searched via `glacier/index.md`.

### What Memory Looks Like

Here's what builds up over time. None of this is pre-filled — it emerges from your conversations.

**`memory/hot-memory.md`** — the 30,000-foot view:

```markdown
# Hot Memory
<!-- L0: Current priorities, active situations, system notes -->

## Identity
- Software engineer at Acme Corp, 2 kids, based in Melbourne
- Side project: open-source CLI tools

## Watch
- Performance review cycle opens next week — prep doc started [[work/acme/action-items]]
- Kid's speech therapy showing progress — 3 new words this month [[personal/health]]

## System
- /reflect found 3 observation clusters ready to promote to patterns
```

**`memory/personal/observations.md`** — raw events, append-only:

```markdown
- 2026-03-10 [family]: School called — Sam had a great day, shared toys unprompted for the first time
- 2026-03-11 [health]: Ran 5k in 28min. Knee felt fine. Third run this week without pain.
- 2026-03-12 [insight]: Realized I've been avoiding the budget conversation. Not about money — about control.
```

**`memory/work/acme/entities.md`** — people and context:

```markdown
### Sarah Chen
- Role: Engineering Manager (direct report to VP Eng)
- Context: Joined Jan 2025. Runs platform team. Prefers async updates over meetings.
- Notes: Advocated for my promotion. Values shipping over polish.
```

### Progressive Condensation

Two processes:

**Condensation:** observations → patterns → hot-memory. Each layer is smaller and more actionable than the one below.

**Archival:** old observations → glacier. Indexed, retrievable, out of the way.

Nothing is deleted — it moves to the right place.

### Threads — The Zettelkasten Layer

When a topic keeps coming up across observations, Cog raises it into a **thread** — a read-optimized synthesis file that pulls scattered fragments into a coherent narrative.

Every thread has the same spine:

- **Current State** — what's true right now (rewrite freely)
- **Timeline** — dated entries, append-only, full detail preserved
- **Insights** — patterns, learnings, what's different this time

A thread gets raised when a topic appears in 3+ observations across 2+ weeks, or when you say "raise X" or "thread X". Threads grow long — that's the point. The texture is the value. One file forever, never condensed.

Fragments (observations) never move. Threads reference them via wiki-links.

See the full [Thread Framework documentation](https://lab.puga.com.br/cog/#/memory) for details.

### L0 / L1 / L2 Tiered Loading

Every memory file has a one-line summary: `<!-- L0: what's in this file -->`. This is the first tier of a three-level retrieval protocol:

- **L0** — one-line summary. Decides whether to open a file at all.
- **L1** — section header scan. Identifies which part of a long file to read.
- **L2** — full file read. Used when the full context is needed.

Scan L0s first, confirm relevance, use L1 for long files, read only what's needed.

### Single Source of Truth

Each fact lives in one canonical file. `entities.md` owns people. `action-items.md` owns tasks. `hot-memory.md` holds pointers — not the authoritative version of any fact. Other files reference with `[[wiki-links]]` instead of copying.

### Wiki-Links

Files cross-reference each other with `[[domain/filename]]` links. A link index is auto-generated by `/housekeeping` so you can discover what connects to what.

### Domain Registry

Domains are areas of your life — personal, work, side projects. Each domain gets its own memory directory and slash command.

```
/setup → conversational → domains.yml → directories + skills + routing
```

| Type | Purpose | Examples |
|------|---------|---------|
| `personal` | Personal life | Always created |
| `work` | Day job | `/acme`, `/google` |
| `side-project` | Ventures, hobbies | `/myapp`, `/substack` |
| `system` | Cog internals | Auto-created (`cog-meta`) |

## Skills

Built-in skills in `.claude/commands/`:

| Skill | What it does |
|-------|-------------|
| `/setup` | Conversational domain setup |
| `/personal` | Family, health, calendar, day-to-day |
| `/reflect` | Mine conversations, extract patterns, condense |
| `/evolve` | Audit memory architecture, propose rule changes |
| `/foresight` | Cross-domain strategic nudge |
| `/scenario` | Decision simulation with timeline overlay |
| `/housekeeping` | Archive, prune, link audit, glacier index |
| `/history` | Deep search across memory files |
| `/explainer` | Writing and explanation (Atkins + Montaigne method) |
| `/humanizer` | Remove AI patterns from text |

Domain skills (`/work`, `/sideproject`, etc.) are auto-generated by `/setup`.

## Pipeline

Cog includes pipeline skills that maintain memory health over time. Run them manually:

```
/housekeeping    # Archive stale data, prune hot-memory, rebuild indexes
/reflect         # Mine recent work, condense patterns, detect threads
/evolve          # Audit architecture, check rule effectiveness
/foresight       # Cross-domain scan, surface one strategic nudge
```

Or automate with scheduling:

**Claude Code** has built-in task scheduling — use `/loop` or cron to run pipeline skills on a recurring basis:

```bash
# Example: nightly housekeeping + reflect via cron
0 23 * * * cd /path/to/cog && claude -p "$(cat .claude/commands/housekeeping.md)"
0 0  * * * cd /path/to/cog && claude -p "$(cat .claude/commands/reflect.md)"
```

**[Cowork](https://claude.com/product/cowork)** sessions can also run pipeline skills. Open Cog in Cowork and ask it to run `/housekeeping` or `/reflect` — it has full file access and can maintain memory as part of a longer autonomous session.

The pipeline is optional. Cog works without it — but running it regularly keeps memory clean and surfaces insights you'd miss.

## Architecture

Cog's architecture lives entirely in instructions — `CLAUDE.md` for conventions and `.claude/commands/*.md` for workflows. There is no application code. The instructions define how memory is structured, how queries are routed, and how the system maintains itself. Claude reads these files and acts on them. The `memory/` directory is just the state that accumulates.

This makes Cog interface-agnostic. It works with:

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)** (terminal) — native. Just open the project.
- **[Cowork](https://claude.com/product/cowork)** — Claude Desktop's agentic mode. Point it at `memory/` and it inherits everything. Great for heavy document generation and long autonomous workflows.
- **Any Claude-powered tool** that reads `CLAUDE.md` and has file access.

The memory system is the same everywhere — markdown files with conventions. The interface just determines how context is loaded.

## Connecting Tools

Cog becomes significantly more powerful when connected to external tools via MCP (Model Context Protocol). In Claude Code or Cowork, you can connect services like:

- **Google Calendar** — schedule awareness, meeting prep, time-blocking
- **Gmail** — email drafting, inbox triage, follow-up tracking
- **Slack** — team context, message drafting, channel monitoring
- **GitHub** — PR reviews, issue tracking, codebase awareness
- **Linear/Jira** — project tracking, sprint context
- **Notion/Obsidian** — extended knowledge base, note sync

When tools are connected, Cog's skills can use them automatically. `/foresight` checks your calendar before surfacing nudges. `/reflect` can reference Slack threads. `/personal` can draft emails. The memory layer gives these tools something they don't have alone: context that persists and compounds.

**To connect tools in Cowork**, add MCP servers in your Cowork settings. Each tool appears as a set of functions Cog can call alongside its memory operations — no code changes needed.

The combination of persistent memory + connected tools is where Cog stops being a note-taking system and starts being a cognitive layer. Memory without action is a diary. Memory with tools is an agent.

## Credits

Cog is a synthesis of ideas from research, open-source systems, and knowledge management traditions.

**Research**: [RLM](https://arxiv.org/abs/2512.24601) (recursive memory hierarchy) | [A-MEM](https://arxiv.org/abs/2502.12110) (bi-directional back-linking) | [OpenViking](https://github.com/volcengine/OpenViking) (L0/L1/L2 tiered context loading)

**Systems**: [Zep/Graphiti](https://github.com/getzep/graphiti) (temporal validity) | [Mem0](https://github.com/mem0ai/mem0) (contradiction detection) | [Claude Memory](https://docs.anthropic.com/en/docs/claude-code/memory) (file-based architecture validation)

**Traditions**: [Zettelkasten](https://en.wikipedia.org/wiki/Zettelkasten) (thread framework) | [SSOT](https://en.wikipedia.org/wiki/Single_source_of_truth) (canonical fact storage)

**Platform**: [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) (Anthropic)

See the [full credits page](https://lab.puga.com.br/cog/#/credits) for how each idea shaped Cog's design.

## Citation

If Cog influences your work — whether you fork it, adapt the patterns, or reference the architecture — a mention goes a long way:

```
Cog: Cognitive Architecture for Claude Code
https://github.com/marciopuga/cog
Marcio Puga, 2026
```

BibTeX for academic use:

```bibtex
@software{puga2026cog,
  author = {Puga, Marcio},
  title = {Cog: Cognitive Architecture for Claude Code},
  year = {2026},
  url = {https://github.com/marciopuga/cog},
  note = {Persistent memory, self-reflection, and foresight for AI agents}
}
```

## License

MIT
