<!-- Auto-generated from domains.yml by /setup. Re-run /setup to regenerate. -->
<!-- Template variables: {{ID}}, {{LABEL}}, {{PATH}}, {{TRIGGERS}}, {{FILES}} -->

Use this skill when the user discusses {{LABEL}} topics. Trigger if the conversation involves:
{{TRIGGERS}}
Do NOT trigger for topics belonging to other domains.

## Domain

{{LABEL}}

## Memory Files

Always read on activation:
- `memory/{{PATH}}/hot-memory.md`

Then load additional files per the **Memory Retrieval Protocol** (see CLAUDE.md) based on the query:
- Status/task query → `memory/{{PATH}}/action-items.md`
- Entity/people query → `memory/{{PATH}}/entities.md`
- Project query → `memory/{{PATH}}/projects.md` (if exists)
- Technical query → `memory/{{PATH}}/dev-log.md` (if exists)
- Update/observation → target file only
- Complex query → hot-memory first, then drill into referenced files

Available warm files: {{FILES}}

Historical data: read `memory/glacier/index.md`, filter by domain={{ID}}

## Routing

When the user shares information or asks to save something:
- Task/todo → `memory/{{PATH}}/action-items.md`
- Person/entity → `memory/{{PATH}}/entities.md`
- Project/technical → `memory/{{PATH}}/projects.md`
- Update/log → `memory/{{PATH}}/observations.md`
- Status/overview → `memory/{{PATH}}/hot-memory.md`

## Activation

Read the hot-memory file, then respond to the user's query using the retrieval protocol above.
