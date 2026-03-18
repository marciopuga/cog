Use this skill when the user discusses personal life topics. Trigger if the conversation involves:
- Family members, friends, or personal relationships
- Health, fitness, diet, sleep, or medical topics
- Personal calendar, appointments, errands, or day-to-day logistics
- Emotions, mood, or personal reflections
- Home, pets, hobbies (non-coding), travel plans
Do NOT trigger for work topics, coding projects, or career development.

## Domain

Personal life — family, friends, health, calendar, day-to-day logistics.

## Memory Files

Always read on activation:
- `memory/personal/hot-memory.md`

Then load additional files per the **Memory Retrieval Protocol** (see CLAUDE.md) based on the query:
- Status query → `memory/personal/calendar.md` or `memory/personal/action-items.md`
- Entity query → `memory/personal/entities.md`
- Health query → `memory/personal/health.md`
- Update/observation → target file only
- Complex query → hot-memory first, then drill into referenced files

Available warm files: `observations.md`, `calendar.md`, `health.md`, `entities.md`, `action-items.md`

Historical data: read `memory/glacier/index.md`, filter by domain=personal

## Behaviors

- When reading memory files, follow [[wiki-links]] if the linked topic is relevant
- Track family and friend updates in `entities.md`
- Log schedule changes to `calendar.md`
- Note health observations in `health.md`
- Add time-sensitive items to `hot-memory.md`
- Append notable events to `observations.md`

## Artifact Formats

**Observation**: `- YYYY-MM-DD: <what happened or was learned>`
**Action item**: `- [ ] <task> (added YYYY-MM-DD)`
**Entity entry**: `- **Name** — relationship (context: <details>)`

## Activation

Read hot-memory, classify the query per the Memory Retrieval Protocol, load the minimum files needed, and respond.
