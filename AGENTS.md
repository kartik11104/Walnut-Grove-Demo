# Rules for Codex (read this first, every task)

You are building a demo website for Walnut Grove Animal Hospital, a real veterinary clinic in Langley, BC.
A reviewer (Claude) checks every change you make before the owner sees it. Work in small steps and follow these rules exactly.

## Project layout
- `template.html`  the whole site (HTML, CSS, JS). Pages are `<div class="view" id="v-NAME">` blocks. Edit this file.
- `data/content.json`  services text and images. `data/plants.json`  pet-safety lists. FAQ and schema live in `build.py`.
- `build.py`  fills the template and writes `dist/index.html`. Run: `python3 build.py dist/index.html`
- `tests/test.py`  Playwright checks. Run after every change: `python3 tests/test.py`  (must print ERRORS: [])
- `baseline-approved-demo.html`  the approved version. Never edit it. Use it to compare.

## Hard rules (a change that breaks one is rejected)
1. Change only the files named in the task's "Allowed files". Touch nothing else.
2. Never invent facts: no new years in practice, case counts, prices, staff names, awards, reviews, certifications, or services. Use only text already in the repo or in the task. If you need a fact, write `[CONFIRM: what is needed]` in the page and list it in your report.
3. Clinic facts are fixed: Walnut Grove Animal Hospital, 101A-20995 88 Ave, Langley BC V1M 2C9, (604) 888-2628, Mon-Fri 8:30am-7pm, Sat-Sun 9am-5pm.
4. No medical advice beyond what is already on the page. Anything about an emergency says: call the clinic, or the nearest 24-hour emergency clinic after hours.
5. The booking form is a demo and must send nothing. Do not add network calls, trackers, analytics, forms posting anywhere, or external scripts/fonts.
6. Keep: the Demo banner, `noindex` meta, light and dark mode, phone layout (390px wide, no sideways scroll), keyboard use, visible focus, alt text, 44px tap targets.
7. Never add secrets, passwords, emails of real people, or API keys. Never read or write outside this folder.
8. No new dependencies. Plain HTML, CSS and JS only.
9. Plain, kind wording for pet owners. No hype words ("best", "leading", "state-of-the-art") and no unprovable claims.

## How to finish a task
1. Run `python3 build.py dist/index.html` then `python3 tests/test.py`.
2. Commit on a branch named `task/<task-id>` and open a pull request. Do not merge.
3. In the pull request, fill in this report (the reviewer reads it first):
   - What I changed (files and what)
   - What I did NOT change
   - Facts I was unsure about ([CONFIRM] items)
   - Test output (paste the last lines)
   - Screenshots path (desktop and phone, light and dark) if the look changed
