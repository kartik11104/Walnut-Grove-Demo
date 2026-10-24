# P2 Services page
Allowed files: `template.html` (inside `#v-services`, the drawer, and their CSS/JS), `data/content.json` (wording only, never images)
Goal: owners find a service fast. 20 services, 5 groups.
Do:
- Add a search box that filters the cards as you type (no network).
- Show a small "No match, call us" message when nothing matches.
- Keep the service drawer, Escape to close, and return focus to the card that opened it.
Do not: rewrite medical descriptions or add services.
Done when: typing "dental" shows only matching cards; Escape closes the drawer; tests pass.
