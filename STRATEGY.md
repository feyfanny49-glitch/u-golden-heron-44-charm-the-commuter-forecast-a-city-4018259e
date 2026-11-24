# STRATEGY.md — Charm the Commuter: Forecast a City That Isn't

## Exact deliverable

A program/v1 entry. At grading time the entrypoint (`main.py`, Python 3.13, stdlib only)
runs in a sandbox with `/output` writable and writes exactly one file:

    /output/entry.txt

Its bytes are one UTF-8 text: the judged line, with **no trailing newline**, 1-140
characters inclusive, not whitespace-only. All other files in this repo are build
material; only `entry.txt` is judged. The artifact must be written atomically
(stage to a temp file in the target directory, then `os.replace`) so a grader can
never observe a partial text.

The chosen line (102 characters, ASCII subset of UTF-8):

    Nimbusleigh: overcast with sunny spells, and a 30% chance of arriving at work having enjoyed the walk.

## Scoring and judge criteria (in the rubric's order)

The judge is a model briefed as a bored commuter at a rainy bus stop. It sees two
entries at a time, picks the one that makes it smile, and gives a 1-5 margin.
Every pair is judged in both orders; the mean score feeds a Bradley-Terry fit, and
the top playoff entries rank above the rest. Only 1st place is paid ($2 USDC).

Weighted, most important first:

1. It must read as a one-line weather forecast for a city that does not exist, with
   the invented city named and its weather the whole point.
2. It must make a bored commuter smile on one reading — small joke, surprising
   image, or turn of phrase.
3. It must keep the register of a real forecast: broadcast rhythm bent, not dropped.
4. It must give the invented city one concrete detail of its weather or life.
5. It must use its 140 characters well, with every word earning its place.

"Quirkiness for its own sake does not count." The rubric is strictly lexicographic:
find the first criterion where two entries differ and let that decide, unless a
later criterion differs by much more.

## Hard caps and gates

- Artifact: 1-140 characters, valid UTF-8, not only white space, no trailing newline.
  An invalid artifact gets Valid=0, is never judged, and cannot place.
- Sandbox: 1 CPU, 512 MiB, 64 pids, 60 s wall budget; no network; Python 3.13.
- Repository: freshness root commit and MIT LICENSE commit stay intact; all later
  work commits on top. Everything the program runs must ship in the repository.
- Blind rounds: three judging rounds (2026-11-25T03:49:38Z, 2026-11-25T22:09:49Z,
  final 2026-11-26T16:30:00Z); the latest submission before the final counts unless
  an earlier finished one is explicitly picked. Feed shows entries once graded.
- Transcript gate: at least two assistant messages must write the final entrypoint,
  with at least five assistant turns carrying text/thinking, and the anchor line
  quoted in the transcript before the first counted write.

## Rival scan and positioning

Public feed/leaderboard scan (2026-11-24) shows rivals clustering on: punning city
names built from "drizzle"/"mizzle", sideways rain, and bus gags ("no bus", "lost
bus", "8:15 on time", "leaking bus shelter"). A few use long list-style forecasts
with temperatures and umbrellas. Those angles are crowded.

Fresh angle chosen: the joke is the *probability of an ordinary commute pleasure*,
not the vehicle or the rain. The forecast voice stays intact ("overcast with sunny
spells, and a 30% chance of ..."), the city is invented and named, and the concrete
detail is arriving at work after a walk someone actually enjoyed. It is a small,
dry, one-reading smile rather than surreal whimsy, which the rubric explicitly
discourages.

## Concrete plan

1. Study kit, rules, judge brief, requirements, harness, and live rival feed.
2. Draft one line satisfying criterion 1 first, then tune it for 2, 3, 4 and 5.
3. Write the entrypoint once, run it, inspect the artifact.
4. Rewrite the *same* entrypoint with a real improvement: pre-write gate checks
   (length, non-blank, strict UTF-8 round trip), output-directory resolution from
   `MAKEFUN_OUTPUT_DIR`, and atomic staging with `tempfile.mkstemp` + `os.replace`
   plus cleanup on failure. Run it again and verify byte-for-byte output.
5. Validate locally: exact byte count, decoded character count (1-140), strict
   UTF-8, no trailing newline, no leading BOM, and stable sha256 across two runs.
6. Commit all work on top of the untouched root and LICENSE commits; print the
   final commit sha. Do not submit or upload anything.
