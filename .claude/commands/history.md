---
name: history
description: >
  Deep memory search and recall — recursive search across all memory files,
  piecing together a narrative from observations, entities, and action items.
  Invoke with /history or on "what did I say about..." queries.
---

Use this skill for deep memory search and recall. Trigger if the user says "what did I say about...", "when did we discuss...", "find that conversation about...", "history of...", or asks about past information that needs multi-file search. For simple date/keyword lookups, a quick Grep suffices — this skill is for when you need to piece together a narrative from multiple entries.

## Domain

Memory recall — recursive search across all memory files, cross-referencing observations, entities, and action items.

## Memory Path

All files under the resolved memory path: `$COG_HOME/memory/` if `COG_HOME` is set, otherwise `~/cog/memory/`. All `memory/...` references below are relative to this root.

## Memory Files

Read on activation:
- `memory/hot-memory.md` (for context on what's currently relevant)

Search across:
- All `observations.md` files (personal, work domains, cog-meta)
- All `entities.md` files
- All `action-items.md` files
- All `hot-memory.md` files
- `memory/glacier/` (via index.md for targeted retrieval)

## Process

### Pass 1: Locate

- Extract keywords from the user's query (names, topics, dates, phrases)
- If the query names a domain (or `memory/domains.yml` triggers match), grep inside that domain first; fall back to the whole memory root only when the domain is unknown
- Grep for each keyword
- Note which files matched and how many hits
- If >10 files match, narrow by domain or add query terms
- If 0 matches, try synonyms or related terms
- Check `memory/glacier/index.md` for archived data matching the query

### Pass 2: Extract

- Read the top 3-5 most relevant files (by hit density and recency)
- Extract the specific passages that match the query
- Track the timeline: when did the topic first come up? How did it evolve?

### Pass 3: Synthesize

- Combine extracted passages into a coherent answer
- Present findings chronologically with dates
- If something seems incomplete, flag it:
  > "Found references to X in observations but no entity entry — want me to create one?"

## Artifact Formats

**Search result**: `YYYY-MM-DD: <summary of what was found>`
**Memory gap**: `Gap: referenced but not in memory — <topic>`
**Timeline**: Chronological list of when a topic appeared and how it evolved

## Activation

Extract search terms from the user's query and begin Pass 1. Be thorough but concise in the synthesis — don't dump raw content.
