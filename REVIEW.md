# Claude's review checklist (applied to every Codex pull request)

Pass = all seven. Any fail = send back with the exact line and the fix needed. Two fails on the same task = Claude builds that piece.

1. SCOPE     Only the allowed files changed. `git diff --stat` matches the task.
2. FACTS     No new claims or numbers. Name, address, phone, hours exactly as in AGENTS.md. Every [CONFIRM] listed.
3. SAFETY    Emergency wording intact. No medical advice added. Booking still sends nothing. No external calls.
4. TESTS     `python3 tests/test.py` prints ERRORS: [] and the booking checks are all True.
5. LOOK      Screenshots checked by eye: desktop and phone, light and dark. Nothing cut off, overlapping, or hard to read.
6. ACCESS    Keyboard works, focus visible, alt text, contrast, tap targets, headings in order.
7. VOICE     Plain, warm, accurate. No hype. Spelling and punctuation checked.

Scorecard (kept in tasks/SCORECARD.md): task, pass/fail on first try, fails by check number, minutes of owner time.
Rule: 3 first-try passes in a row, give Codex bigger tasks. 2 fails in a row, give smaller tasks.
