#!/usr/bin/env python3
"""Ask the 20 questions in eval/questions.json against two copies of examples/memory:

  old  the layout and instructions of Cog before v2 (CLAUDE.md + /cog skill from git ref OLD_REF,
       <!-- L0 --> comments, domains.yml, per-folder hot-memory.md and INDEX.md, threads/,
       calendar.md, facts kept as History lines in the files they came from, link-index.md)
  v2   this repo: AGENTS.md and its commands (prompt only), the fixture as it is

Each question runs in a fresh headless Claude Code session. Grading is by keywords from the
answer key (eval/questions.json); read eval/results-*.jsonl to check them by eye.

  python3 eval/run.py [--model sonnet] [--only old|v2] [--ids 1,2,3]
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE = os.path.join(REPO, "examples", "memory")
OLD_REF = "33a621c"  # last commit before v2
TODAY = "2026-11-20"
PROMPT = ("{q}\n\nToday is " + TODAY + ". Answer from my memory in one or two sentences. "
          "Do not change any files.")


def fm(text):
    """(l0, body) of a v2 file."""
    m = re.match(r"---\nl0: (.*)\n---\n", text)
    return (m.group(1).strip('"'), text[m.end():]) if m else ("", text)


def build_old(dst):
    """The fixture in the pre-v2 layout, holding the same information."""
    subprocess.run(f"git -C {REPO} archive {OLD_REF} CLAUDE.md .claude | tar -x -C {dst}", shell=True, check=True)
    mem = os.path.join(dst, "memory")
    topics = {}
    for folder in ("personal", "work"):
        for f in os.listdir(os.path.join(FIXTURE, folder)):
            if f.endswith(".md") and f not in ("index.md", "observations.md", "action-items.md", "entities.md"):
                topics[f"{folder}/{f[:-3]}"] = f"{folder}/threads/{f[:-3]}"
    relink = lambda s: re.sub(r"\[\[([^\]]+)\]\]", lambda m: f"[[{topics.get(m.group(1), m.group(1))}]]", s)  # noqa: E731
    files = {}
    for dp, _, fs in os.walk(FIXTURE):
        for f in fs:
            r = os.path.relpath(os.path.join(dp, f), FIXTURE)
            if f == "index.md" or r in ("facts.md", "events.md", "patterns.md"):
                continue
            l0, body = fm(open(os.path.join(dp, f), encoding="utf-8").read())
            if "/glacier/" in "/" + r:
                folder, name = r.split("/glacier/")
                r = f"glacier/{folder}/{name}"
            r = topics.get(r[:-3], r[:-3]) + ".md"
            body = re.sub(r"\[\[facts\]\] \(key [a-z-]+\)", "the History section below", body)
            files[r] = f"<!-- L0: {l0} -->\n" + relink(body)
    text = lambda p: open(os.path.join(FIXTURE, p), encoding="utf-8").read()  # noqa: E731
    for line in fm(text("facts.md"))[1].splitlines():
        m = re.match(r"- ([a-z0-9-]+): (.*?) \| from:(\S*) \| until:(\S*) \| src:\[\[([^\]]+)\]\]", line)
        if m:
            key, val, frm, until, src = m.groups()
            path = topics.get(src, src) + ".md"
            row = f"- {frm}: {key.replace('-', ' ')} = {val} (until {until or 'now'})"
            if path.endswith("observations.md"):
                row = f"- {frm} [{key}]: {key.replace('-', ' ')} = {val} (until {until or 'now'})"
            elif "## History" not in files[path]:
                files[path] = files[path].rstrip("\n") + "\n\n## History\n\n"
            files[path] = files[path].rstrip("\n") + "\n" + row + "\n"
    cal = ["<!-- L0: Upcoming events, appointments, and named dates -->", "# Personal — Calendar", "",
           "<!-- Edit in place. Time-bounded entries carry until:YYYY-MM-DD comment markers. -->", ""]
    for line in fm(text("events.md"))[1].splitlines():
        m = re.match(r"- ([a-z0-9-]+) \| (\S+) \| ([^|]*)(?:\| aka: (.*))?", line)
        if m:
            cal.append(f"- {m.group(2)} — {m.group(3).strip()} ({m.group(1)}" + (f"; also called {m.group(4)})" if m.group(4) else ")"))
    files["personal/calendar.md"] = "\n".join(cal) + "\n"
    l0, body = fm(text("hot-memory.md"))
    files["hot-memory.md"] = f"<!-- L0: {l0} -->\n# Hot Memory\n" + relink(body)
    l0, body = fm(text("patterns.md"))
    files["cog-meta/patterns.md"] = f"<!-- L0: {l0} -->\n# Learned Patterns\n" + body
    for folder, label in (("personal", "Family, home, health, day-to-day"), ("work", "Work at Quillmoor: Heron, design team, design system")):
        files[f"{folder}/hot-memory.md"] = f"<!-- L0: Current state for {folder} -->\n# Hot Memory\n\n<!-- Rewrite freely. Keep under 50 lines. -->\n"
    links = {}
    for p, t in files.items():
        for target in set(re.findall(r"\[\[([^\]]+)\]\]", t)):
            links.setdefault(target, []).append(p[:-3])
    files["link-index.md"] = "<!-- L0: Backlink index — which files link to which -->\n# Memory Link Index\n\n| Target | Linked from |\n|--------|-------------|\n" + \
        "".join(f"| {t} | {', '.join(sorted(s))} |\n" for t, s in sorted(links.items()))
    files["domains.yml"] = ("# L0: Domain manifest — which memory folders exist and what activates them\ndomains:\n"
                            "  - id: personal\n    path: personal\n    type: personal\n    label: \"Family, home, health, kids, dog, running, money\"\n"
                            "    triggers: [family, kids, health, home, kitchen, car, dog, running, money, holiday]\n"
                            "  - id: work\n    path: work\n    type: work\n    label: \"Quillmoor: Heron, design team, hiring, design system, talks\"\n"
                            "    triggers: [work, quillmoor, heron, design, hiring, team, offsite, talk, conference]\n"
                            "  - id: cog-meta\n    path: cog-meta\n    type: system\n    label: \"Cog self-knowledge\"\n    triggers: [cog, meta]\n")
    for p, t in files.items():
        os.makedirs(os.path.dirname(os.path.join(mem, p)), exist_ok=True)
        open(os.path.join(mem, p), "w", encoding="utf-8").write(t)
    for folder in ("personal", "work", "cog-meta", "glacier"):  # INDEX.md as old housekeeping generated it
        rows = []
        for dp, _, fs in sorted(os.walk(os.path.join(mem, folder))):
            for f in sorted(fs):
                t = open(os.path.join(dp, f), encoding="utf-8").read()
                m = re.search(r"<!-- L0: (.*?) -->", t)
                rows.append(f"| {os.path.relpath(os.path.join(dp, f), os.path.join(mem, folder))} | {t.count(chr(10))} | {m.group(1) if m else ''} |")
        name = "index.md" if folder == "glacier" else "INDEX.md"
        open(os.path.join(mem, folder, name), "w").write(f"<!-- L0: L0 index of {folder} files -->\n# {folder} Index\n\n| File | Lines | Summary |\n|------|-------|---------|\n" + "\n".join(rows) + "\n")


def build_v2(dst):
    for p in ("AGENTS.md", "CLAUDE.md", ".claude"):
        (shutil.copytree if os.path.isdir(os.path.join(REPO, p)) else shutil.copy)(os.path.join(REPO, p), os.path.join(dst, p))
    shutil.copytree(FIXTURE, os.path.join(dst, "memory"))


def ask(cwd, q, model):
    cmd = ["claude", "-p", PROMPT.format(q=q["q"]), "--model", model, "--output-format", "stream-json", "--verbose",
           "--max-turns", "20", "--setting-sources", "project", "--strict-mcp-config", "--no-session-persistence",
           "--permission-mode", "bypassPermissions", "--disallowedTools", "Edit", "Write", "NotebookEdit", "Task", "Agent", "WebSearch", "WebFetch"]
    env = {k: v for k, v in os.environ.items() if not k.startswith(("CLAUDECODE", "CLAUDE_CODE_"))}  # not a nested session
    env.update(COG_HOME=cwd)
    out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env, timeout=600).stdout
    events = [json.loads(s) for s in out.splitlines() if s.startswith("{")]
    tools = [b for e in events if e.get("type") == "assistant" for b in e["message"]["content"] if b.get("type") == "tool_use"]
    res = next((e for e in events if e.get("type") == "result"), {})
    u = res.get("usage", {})
    answer = res.get("result", "")
    ok = all(any(re.search(rf"\b{re.escape(k)}" if k[0].isdigit() else re.escape(k), answer, re.I) for k in group) for group in q["keys"])
    return {"id": q["id"], "kind": q["kind"], "correct": ok, "answer": answer, "key": q["answer"],
            "tool_calls": len(tools), "tools": [t["name"] + ":" + json.dumps(t["input"])[:120] for t in tools],
            "turns": res.get("num_turns"), "cost_usd": res.get("total_cost_usd"),
            "input_tokens": u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0),
            "output_tokens": u.get("output_tokens", 0)}


def main(argv):
    model = argv[argv.index("--model") + 1] if "--model" in argv else "sonnet"
    arms = [argv[argv.index("--only") + 1]] if "--only" in argv else ["old", "v2"]
    qs = json.load(open(os.path.join(REPO, "eval", "questions.json")))
    if "--ids" in argv:
        ids = {int(x) for x in argv[argv.index("--ids") + 1].split(",")}
        qs = [q for q in qs if q["id"] in ids]
    tmp = tempfile.mkdtemp(prefix="cog-eval-")
    for arm in arms:
        rows = []

        def one(q, arm=arm):  # every question gets its own fresh copy, so no run sees another's tidy or edits
            cwd = os.path.join(tmp, f"{arm}-{q['id']}")
            os.makedirs(cwd)
            (build_old if arm == "old" else build_v2)(cwd)
            return ask(cwd, q, model)
        with ThreadPoolExecutor(4) as pool:
            rows = sorted(pool.map(one, qs), key=lambda r: r["id"])
        with open(os.path.join(REPO, "eval", f"results-{arm}.jsonl"), "w") as f:
            f.writelines(json.dumps(r) + "\n" for r in rows)
        n = len(rows)
        print(f"{arm}: {sum(r['correct'] for r in rows)}/{n} correct, "
              f"{sum(r['tool_calls'] for r in rows) / n:.1f} tool calls, "
              f"{sum(r['input_tokens'] for r in rows) / n / 1000:.1f}k input tokens, "
              f"${sum(r['cost_usd'] or 0 for r in rows):.2f} total")
    shutil.rmtree(tmp)


if __name__ == "__main__":
    main(sys.argv[1:])
