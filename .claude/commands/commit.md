Use this skill when the user wants to commit changes to git. Trigger if the user says "commit", "save changes", "commit this", or asks to create a git commit. Examples: "commit", "commit and push", "save my changes".

## Process

1. **Assess the working tree** — Run `git status` (never use `-uall`) and `git diff --staged` and `git diff` to understand what changed.

2. **Guard rails** — Before staging:
   - Never commit files that contain secrets (`.env`, credentials, tokens, keys). Warn if any are present.
   - Never commit build artifacts (`dist/`, `*.tsbuildinfo`).
   - Never commit `node_modules/`.
   - If there are no changes to commit, say so and stop.

3. **Stage selectively** — Stage files by name. Prefer `git add <file>...` over `git add -A` or `git add .` to avoid accidentally including sensitive or unrelated files. Group related changes — if unrelated changes exist, ask whether to commit everything together or separately.

4. **Write the commit message** — Use Conventional Commits format:
   - `feat:` new feature
   - `fix:` bug fix
   - `refactor:` code restructuring without behavior change
   - `chore:` maintenance, dependencies, config
   - `docs:` documentation only
   - `style:` formatting, whitespace
   - `test:` adding or updating tests
   - Scope is optional: `feat(whatsapp): add voice note transcription`
   - Subject line: imperative mood, lowercase, no period, under 72 chars
   - Body (if needed): blank line after subject, wrap at 72 chars, explain *why* not *what*
   - Always end with: `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`

5. **Commit** — Use a HEREDOC for the message to preserve formatting:
   ```
   git commit -m "$(cat <<'EOF'
   type(scope): subject line

   Optional body explaining why.

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
   EOF
   )"
   ```

6. **Verify** — Run `git status` after committing to confirm success. Show the resulting `git log --oneline -1`.

## Rules

- Never push unless `$ARGUMENTS` contains "and push" or "push".
- Never amend unless `$ARGUMENTS` contains "amend".
- Never skip hooks (no `--no-verify`).
- Never force push.
- If a pre-commit hook fails, fix the issue, re-stage, and create a **new** commit (do not amend).
- If `$ARGUMENTS` contains a message hint, use it to inform the commit message but still follow conventional format.

## Arguments

`$ARGUMENTS` — Optional. May contain:
- A message hint (e.g., `/commit add voice transcription support`)
- "and push" to push after committing
- "amend" to amend the previous commit instead of creating a new one
- "all" to stage all changes without asking
