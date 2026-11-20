"""Tests for bin/cog, run against a temp copy of examples/memory. Standard library only.

    python3 -m unittest discover tests
"""
import collections
import hashlib
import importlib.machinery
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COG = os.path.join(REPO, "bin", "cog")
FIXTURE = os.path.join(REPO, "examples", "memory")
TODAY = "2026-11-20"

loader = importlib.machinery.SourceFileLoader("cog", COG)
cog = importlib.util.module_from_spec(importlib.util.spec_from_loader("cog", loader))
loader.exec_module(cog)


def tree_hash(root):
    h = hashlib.sha256()
    for dirpath, dirs, files in os.walk(root):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            h.update(os.path.relpath(p, root).encode() + text(p).encode())
    return h.hexdigest()


def run(root, *args):
    env = dict(os.environ, COG_TODAY=TODAY)
    env.pop("COG_HOME", None)
    r = subprocess.run([sys.executable, COG, "--root", root, *args], capture_output=True, text=True, env=env)
    if r.returncode:
        raise AssertionError(r.stderr)
    return r.stdout


def text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def lines(path):
    return text(path).split("\n")


def entries_in(path):
    return [s for s in lines(path) if s.startswith("- ")]


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture_hash = tree_hash(FIXTURE)

    @classmethod
    def tearDownClass(cls):
        assert tree_hash(FIXTURE) == cls.fixture_hash, "a test changed the committed fixture"

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, "memory")
        shutil.copytree(FIXTURE, self.root)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def p(self, *parts):
        return os.path.join(self.root, *parts)


class Formats(unittest.TestCase):
    def ok(self, fmt, line):
        self.assertTrue(cog.FORMATS[fmt].match(line), f"{fmt} should accept: {line}")

    def bad(self, fmt, line):
        self.assertFalse(cog.FORMATS[fmt].match(line), f"{fmt} should reject: {line}")

    def test_observation(self):
        self.ok("observation", "- 2026-11-20 [garden, home]: Planted garlic [[personal/garden]]")
        self.ok("observation", "- 2026-11-20 [running] about:2026-11-18: Ran 10 km")
        self.ok("observation", "- 2026-11-20 [trip] about:2026-11-01..2026-11-05: Away")
        self.bad("observation", "- 2026-11-20: no tags")
        self.bad("observation", "- 20 Nov [tag]: wrong date")
        self.bad("observation", "- 2026-11-20 [tag] about:18 Nov: about needs an ISO date")

    def test_action(self):
        self.ok("action", "- [ ] Book the vet | due:2026-12-03 | pri:high | added:2026-11-05")
        self.ok("action", "- [x] Done thing | due:2026-03-01 | pri:high | added:2026-02-27 | done:2026-03-02")
        self.ok("action", "- [ ] Return the door | due:2026-11-15 | pri:low | added:2026-07-02 <!-- until:2026-11-15 -->")
        self.ok("action", "- [ ] No fields yet")
        self.bad("action", "- [ ] Task | due 2026-12-01")
        self.bad("action", "- task without a box")

    def test_fact_event_entity(self):
        self.ok("fact", "- car: Electric estate | from:2026-09-12 | until: | src:[[personal/car]] | kind:home")
        self.ok("fact", "- role: Designer | from: | until:2026-04-01")
        self.bad("fact", "- car: Electric estate | since 2026")
        self.ok("event", "- summer-holiday | 2026-07-11..2026-07-25 | at the coast | aka: Coast, holiday")
        self.ok("event", "- new-job | 2026-04-01.. | open-ended")
        self.bad("event", "- Summer Holiday | 11 Jul")
        self.ok("entity", "### Teo Marsh (partner)")
        self.bad("entity", "### Teo Marsh")

    def test_frontmatter(self):
        self.assertEqual(cog.frontmatter(["---", "l0: A file", "---", "x"]), ("A file", 3))
        self.assertEqual(cog.frontmatter(["---", 'l0: "Quoted: yes"', "---"]), ("Quoted: yes", 3))
        self.assertEqual(cog.frontmatter(["# no frontmatter"]), (None, 0))

    def test_entries_keep_continuation_lines(self):
        got = cog.entries(["---", "l0: x", "---", "- a", "  more", "- b", "", "  not mine"], 3)
        self.assertEqual(got, [[3, 4], [5, 5]])


class Tidy(Base):
    def test_fixture_has_no_format_problems(self):
        out = run(FIXTURE, "tidy", "--dry-run")
        self.assertIn("0 format problems", out)

    def test_dry_run_writes_nothing(self):
        before = tree_hash(self.root)
        out = run(self.root, "tidy", "--dry-run")
        self.assertIn("would move 22 observations, 12 action-items-done, 4 expired", out)
        self.assertEqual(tree_hash(self.root), before)

    def test_observations_archive_oldest_down_to_40(self):
        src = self.p("personal", "observations.md")
        before = entries_in(src)
        run(self.root, "tidy")
        after = entries_in(src)
        self.assertEqual(len(after), 40)
        self.assertEqual(after, before[22:])  # the fixture is in date order, so the oldest 22 left
        glacier = self.p("personal", "glacier")
        archived = [s for f in os.listdir(glacier) if f.startswith("observations-") for s in entries_in(os.path.join(glacier, f))]
        self.assertEqual(collections.Counter(archived) - collections.Counter(before[:22]),
                         collections.Counter(entries_in(os.path.join(FIXTURE, "personal", "glacier", "observations-garden.md"))))
        kids = entries_in(os.path.join(glacier, "observations-kids.md"))
        self.assertTrue(all("[kids" in s for s in kids) and len(kids) == 4)
        self.assertEqual(len(entries_in(self.p("work", "observations.md"))), 30)  # under the cap: untouched

    def test_done_items_move_only_over_ten(self):
        run(self.root, "tidy")
        personal = entries_in(self.p("personal", "action-items.md"))
        self.assertFalse(any(s.startswith("- [x]") for s in personal))
        self.assertEqual(len(entries_in(self.p("personal", "glacier", "action-items-done.md"))), 12)
        self.assertEqual(sum(s.startswith("- [x]") for s in entries_in(self.p("work", "action-items.md"))), 2)

    def test_expired_lines_move_with_their_date(self):
        run(self.root, "tidy")
        hot = "\n".join(lines(self.p("hot-memory.md")))
        self.assertNotIn("no sink", hot)
        self.assertNotIn("recovery block", hot)
        self.assertIn("Fieldcraft talk", hot)  # until:2026-12-10 is still live
        expired = entries_in(self.p("glacier", "expired.md"))
        self.assertEqual(len(expired), 2)
        self.assertTrue(expired[0].startswith("- 2026-11-12 [expired]: **Kitchen**"))
        self.assertTrue(all(cog.FORMATS["observation"].match(s) for s in expired))
        self.assertTrue(any("Return the spare cabinet door" in s for s in entries_in(self.p("personal", "glacier", "expired.md"))))

    def test_nothing_is_lost(self):
        def all_entries(root):
            return collections.Counter(s.split(" (from ")[0] for dp, _, fs in os.walk(root) for f in fs
                                       if f.endswith(".md") and f != "index.md" for s in entries_in(os.path.join(dp, f)))
        before = all_entries(self.root)
        run(self.root, "tidy")
        after = all_entries(self.root)
        self.assertEqual(sum(before.values()), sum(after.values()))
        self.assertEqual(before - after, collections.Counter({  # expired lines are rewritten, not dropped
            s: 1 for s in before if "until:2026-11-1" in s}))

    def test_idempotent(self):
        run(self.root, "tidy")
        once = tree_hash(self.root)
        out = run(self.root, "tidy", "--quiet")
        self.assertEqual(out, "")
        self.assertEqual(tree_hash(self.root), once)

    def test_glacier_is_written_before_the_source(self):
        cog.ROOT, cog.TODAY = self.root, date.fromisoformat(TODAY)
        src = self.p("personal", "observations.md")
        before, real = lines(src), cog.write

        def failing_write(path, new):
            if path == src:
                raise OSError("disk full")
            real(path, new)
        cog.write = failing_write
        try:
            with self.assertRaises(OSError), redirect_stdout(io.StringIO()):
                cog.tidy()
        finally:
            cog.write = real
        self.assertEqual(lines(src), before)
        archived = entries_in(self.p("personal", "glacier", "observations-kids.md"))
        self.assertEqual(len(archived), 4)

    def test_index_folds_big_folders(self):
        run(self.root, "tidy")
        index = "\n".join(lines(self.p("index.md")))
        self.assertIn("## personal/ — Family, home, health and everything outside work", index)
        self.assertIn("15 files, folded: read personal/index.md", index)
        self.assertIn("| work/heron-launch.md | 19 | Heron, the field-survey app", index)
        self.assertIn("| hot-memory.md |", index)
        self.assertIn("- personal/glacier/: 11 files", index)
        own = lines(self.p("personal", "index.md"))
        self.assertEqual(own[1], "l0: Family, home, health and everything outside work")
        self.assertEqual(sum(s.startswith("| personal/") for s in own), 15)

    def test_check_reports_location_and_never_writes(self):
        obs = self.p("work", "observations.md")
        with open(obs, "a", encoding="utf-8") as f:
            f.write("- 21 Nov: written without the format\n")
        with open(self.p("work", "notes.md"), "w") as f:
            f.write("# no frontmatter\n")
        before = text(obs)
        out = run(self.root, "tidy", "--quiet")
        self.assertIn("2 format problems", out)
        self.assertIn("work/observations.md:36: not a observation line: - 21 Nov", out)
        self.assertIn("work/notes.md:1: no l0:", out)
        self.assertEqual(text(obs), before)

    def test_hot_memory_cap(self):
        with open(self.p("hot-memory.md"), "a") as f:
            f.write("".join(f"- **x{i}** — filler\n" for i in range(20)))
        self.assertIn("hot-memory.md: 28 lines, cap is 25", run(self.root, "tidy", "--dry-run"))


class When(Base):
    def test_asof_and_timeline(self):
        self.assertIn("heron-team-size: 6", run(self.root, "when", "asof", "2026-07-01", "heron-team-size"))
        out = run(self.root, "when", "asof", "offsite", "role")  # an event name resolves to its start
        self.assertIn("role: Senior product designer", out)
        self.assertNotIn("Head of", out)
        tl = run(self.root, "when", "timeline", "mortgage-rate").splitlines()
        self.assertTrue(tl[0].startswith("2024-03-01..2026-09-01") and "5.1%" in tl[0])
        self.assertTrue(tl[1].startswith("2026-09-01..…") and "4.3%" in tl[1])
        self.assertIn("resting-heart-rate: 54 bpm", run(self.root, "when", "facts"))

    def test_event_windows_and_aka(self):
        out = run(self.root, "when", "during:Saltmarsh", "armbands")
        self.assertIn("personal/observations.md:40", out)
        out = run(self.root, "when", "before:the-race", "after:2026-09-25", "running")
        self.assertIn("Left calf strain", out)
        self.assertNotIn("1:52:40", out)
        out = run(self.root, "when", "after:launch", "before:2026-10-16", "--clock", "said")
        self.assertIn("rolled back background sync", out)

    def test_about_dates_count(self):
        out = run(self.root, "when", "2026-10-25", "--clock", "about", "mile")
        self.assertIn("Teo and the kids were at mile 10", out)

    def test_last_and_glacier(self):
        out = run(self.root, "when", "last:7d")
        self.assertIn("Kofi", out)
        self.assertNotIn("2026-11-12 [reading]", out)
        run(self.root, "tidy")
        self.assertNotIn("heart murmur", run(self.root, "when", "2026-02"))
        self.assertIn("heart murmur", run(self.root, "when", "2026-02", "--glacier"))

    def test_dates_written_in_prose(self):
        ctx = date(2026, 11, 20)
        spans = cog.date_line("- 2026-11-18 [car]: first service due by 5 Dec, trip 29 Sep–6 Oct", None, ctx)
        self.assertIn(("about", date(2026, 12, 5), date(2026, 12, 5)), spans)
        self.assertIn(("about", date(2026, 9, 29), date(2026, 10, 6)), spans)
        self.assertEqual(cog.date_line("- [ ] x | due:2026-12-01 | added:2026-11-01", None)[1:], [("due", date(2026, 12, 1), date(2026, 12, 1))])
        self.assertEqual(cog.date_line("see [[work/2026-01-05-notes]]", None), [])

    def test_awareness(self):
        out = run(self.root, "when")
        self.assertIn("in 9d    mabel-birthday", out)
        self.assertIn("## Overdue open items (3)", out)
        self.assertIn("Send the Heron accessibility audit", out)


OLD = {
    "domains.yml": "# L0: Domain manifest\ndomains:\n  - id: personal\n    path: personal\n    type: personal\n"
                   "    label: \"Family and home\"\n    triggers: [family]\n  - id: cog-meta\n    path: cog-meta\n"
                   "    label: \"System\"\n",
    "hot-memory.md": "<!-- L0: Cross-domain state -->\n# Hot Memory\n\n- Dentist Tue <!-- until:2026-11-10 grace:5 -->\n"
                     "- Talk prep <!-- until:2026-12-01 -->\n",
    "link-index.md": "<!-- L0: Backlinks -->\n",
    "glacier/index.md": "<!-- L0: Glacier catalog -->\n",
    "cog-meta/patterns.md": "<!-- L0: Rules -->\n# Patterns\n\n- Be brief.\n",
    "cog-meta/run-log.md": "<!-- L0: Run log -->\n",
    "personal/INDEX.md": "<!-- L0: index -->\n| File |\n",
    "personal/observations.md": "<!-- L0: Personal log -->\n# Obs\n\n- 2026-11-01 [home]: Moved the shed\n",
    "personal/calendar.md": "<!-- L0: Calendar -->\n# Calendar\n\n## Upcoming\n- 2026-12-09: the talk\n",
    "personal/threads/garden.md": "---\ntype: thread\n---\n<!-- L0: Garden thread -->\n## Current State\n",
}


class Migrate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, "memory")
        for path, body in OLD.items():
            os.makedirs(os.path.dirname(os.path.join(self.root, path)), exist_ok=True)
            with open(os.path.join(self.root, path), "w") as f:
                f.write(body)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def read(self, path):
        return text(os.path.join(self.root, path))

    def test_dry_run_by_default(self):
        before = tree_hash(self.root)
        out = run(self.root, "migrate")
        self.assertIn("dry run", out)
        self.assertIn("merge personal/calendar.md into events.md", out)
        self.assertEqual(tree_hash(self.root), before)

    def test_apply(self):
        run(self.root, "migrate", "--apply")
        exists = lambda p: os.path.exists(os.path.join(self.root, p))  # noqa: E731
        self.assertTrue(self.read("personal/observations.md").startswith("---\nl0: Personal log\n---\n# Obs"))
        self.assertEqual(self.read("personal/threads/garden.md").split("\n")[:4], ["---", "l0: Garden thread", "type: thread", "---"])
        self.assertIn("l0: Family and home", self.read("personal/index.md"))
        self.assertFalse(exists("personal/INDEX.md"))
        self.assertIn("- Be brief.", self.read("patterns.md"))
        for old in ("cog-meta/run-log.md", "link-index.md", "domains.yml", "index.md", "personal-calendar.md"):
            self.assertTrue(exists("glacier/legacy/" + old), old)
        self.assertFalse(exists("cog-meta") or exists("link-index.md") or exists("personal/calendar.md"))
        self.assertIn("- 2026-12-09: the talk", self.read("events.md"))
        self.assertIn("Talk prep <!-- until:2026-12-01 -->", self.read("hot-memory.md"))
        self.assertIn("- 2026-11-15 [expired]: Dentist Tue", self.read("glacier/expired.md"))  # grace folded, then expired
        self.assertIn("## personal/ — Family and home", self.read("index.md"))
        out = run(self.root, "migrate")
        self.assertIn("0 steps", out)


if __name__ == "__main__":
    unittest.main()
