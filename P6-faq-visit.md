# P6 FAQ and Visit pages
Allowed files: `template.html` (inside `#v-faq` and `#v-visit`), `build.py` (the FAQ list and schema only)
Goal: answers a stressed owner needs.
Do:
- FAQ: keep items marked `confirm=True` visibly tagged for the owner and out of the search-engine schema.
- Visit: map link, directions text, hours table with today highlighted (America/Vancouver time), `[CONFIRM: parking]` and `[CONFIRM: holiday hours]`.
Do not: state an after-hours clinic name; use `[CONFIRM: nearest 24-hour emergency clinic]`.
Done when: schema still validates as JSON; tests pass.
