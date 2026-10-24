# V2 build report

Branch: `v2-build`, created from main `ce2e2c7`. V1 templates and design files were not reused. Each page was committed separately; the branch was pushed throughout the work.

## Files changed

- `build_v2.py`, `requirements-v2.txt`: fresh Python/Jinja build, source extraction, metadata, schemas, sitemap, robots, vCard and intrinsic photo sizes.
- `templates/`: fresh shared shell/components, CSS/JS, Home, Services, service detail, Team, Visit, Pet care, FAQ, Blog, article, Book, Privacy and 404 templates.
- `data/clinic.json`, `services.json`, `faq.json`, `posts.json`, `plants.json`, `reviews.json`. Hours have one runtime source, clinic.json; `bookingLive` is false; reviews are empty.
- `assets/fonts/`: the specified Google Fonts in WOFF2 with their licences.
- `site/`: committed deployable output, 35 pages and local assets. No V1 output is reused by the V2 build.
- `tests/test_v2.py`: static HTTP checks plus the required Playwright checks and screenshot capture at both requested sizes. Real Google Form requests are intercepted and aborted during browser tests.
- `.gitignore`: excludes the local build dependency directory. Existing review/ exclusion retained.
- This report. Source text, original photos, V1 template/design files and Vercel noindex configuration were not edited.

Build with `python3 -m pip install -r requirements-v2.txt` then `python3 build_v2.py`. Local dependencies in this instance were installed under ignored `.build-deps/`. Set `SITE_URL` to the approved site origin before the final deployment build. This does not enable booking.

## Test output

```
V2 build: 35 pages; 20 services; 5 posts; bookingLive=False; SHOW_CONFIRM=True
CSS: 11379 bytes; JS: 11285 bytes
Canonical origin: https://example.invalid
```

`node --check site/assets/site.js`, Python compilation and `git diff --check` passed. Non-browser today-line checks passed at the three requested mocked Vancouver times.

`python3 tests/test_v2.py` exited 2:

```
Static checks: 35 pages, 0 errors
BLOCKED: Chromium unavailable. Browser tests and screenshots were not run.
BrowserType.launch: Executable doesn't exist at /home/agent/.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell
```

The static checks actually served all pages locally and checked internal links and fragments, unique titles, H1s, language, canonical/description metadata, image attributes and the false booking switch. Browser console, native keyboard behavior, visual layout/no overflow, image display sizes, screen reader behavior, clipboard, drafts and browser booking completion remain unverified. No real Google Form submission was attempted.

## Screenshots

Unavailable because Chromium cannot launch. `tests/test_v2.py` captures all 35 pages at 390×844 and 1280×800 into ignored `review/` once the reviewer runs it with Chromium. No screenshots are claimed or committed.

## Unspecified

1. **Service count conflict:** the brief says 19 pages, but there are 20 service source files and 20 named offerings. Included all 20 with the exact source slugs.
2. **Canonical origin:** no approved domain or deployment hostname is supplied. `SITE_URL` controls canonical, Open Graph and sitemap origins; the safe default is `https://example.invalid`. These must be rebuilt with the approved origin before publication. Existing robots/noindex safeguards remain.
3. **Font delivery:** fonts.googleapis.com returned 403. Downloaded the exact named variable fonts from Google Fonts' official google/fonts repository, converted them to WOFF2 without altering glyph designs, retained OFL licences and preloaded both local files with font-display:swap. No substitute fonts were selected.
4. **Dependency versions:** pinned the Jinja2/Markdown/Pillow versions used in this machine. Brotli/fontTools were only needed to produce the committed font files; normal site builds do not need them.
5. **Breakpoints:** phone layout below 600px; tablet 600–899px; desktop from 900px. The explicit under-900 menu/action-bar rule is preserved. Header gaps use 8px in the 900–1100px range to keep all desktop links and actions. Nav font uses the specified 1rem button size.
6. **Unspecified layout details:** used the 24px grid gap, the existing specified type sizes, and the brief's spacing steps. Team portraits/initials use 250px as the nearest specified portrait width. The Home doctor text spans six columns; its photo sits in four columns, at native width.
7. **Clinic-wall pattern:** rotations repeat -2°, 1.5°, -1°, 1.5°; row offsets repeat 0, 32, 16, 48px. Photos are limited to 235px or native width, whichever is smaller. The specified white border/shadow are the only decorative shadow used.
8. **Unspecified component dimensions:** map placeholder min-height 250px; loaded frame height 320px. Emergency dialog max-width 640px with 32px padding and a plain translucent ink backdrop. The phone menu uses the full viewport. The toast uses a plain bordered card, 16px padding and 2200ms visibility. No toast entrance animation was added.
9. **Mobile today line:** allows wrapping when the closed-hours sentence and Emergency link cannot fit into 32px. Safe-area padding is added to the phone action bar/content so phone system controls do not cover it.
10. **Service copy structure:** the source overview becomes the summary and What we do content; symptoms are placed under When to come in only where a source list supports them. Preparation is included only where supported, including the ultrasound/blood-sample fasting Q&As. Questions come from faq.md, matched to source service questions and relevant terms; no new medical answers were written.
11. **FAQ grouping:** the brief provides no question-to-group mapping. Used question subject matter. Skin, ear, chronic-pain and puppy-care questions remain included under the nearest broad prevention group. Answers end at complete sentences within 80 words. No question is answered with an invented clinic policy.
12. **Related links:** three other services from the same Home group in source order; two newest other posts. No medical relationship beyond the brief's groups is claimed.
13. **Article formatting:** removed source navigation, author/footer/promotional boilerplate and topic tags; retained article body, lists and tables. Applied the requested spelling, banned-word, exclamation-mark and em-dash cleanup. Used the real dates/read times from blog.md (all say 4 min read). TOC links are built at build time, so they work without JS.
14. **Forms:** only name and phone are marked required, as specified by the Google Form mapping. The remaining fields are optional. “Other” uses the entered species name, falling back to “Other”; unspecified date/time values are omitted. A preselected service is added to Note. Dates start tomorrow and run for 14 days; local visitor dates drive them. The draft storage key is `walnut-grove-booking-v2`.
15. **Review-mode success:** retained the mandated “Request sent” heading and immediately shows “Review mode: this request was not sent.” The network call is gated on `clinic.bookingLive === true`; the committed value remains false. Booking stays hidden until JS initialization succeeds, with a no-JS call fallback rather than a native accidental form submission.
16. **Copy-address fallback:** if the Clipboard API fails, selects the displayed address; does not falsely announce copying succeeded.
17. **Maps and recall links:** used standard Google/Apple Maps URL formats around the exact brief coordinates. The click-to-load iframe uses Google Maps only after the explicit click. Linked the named VIN recall resource at its recall-centre URL; the source names VIN but does not supply a URL.
18. **Footer logo:** used the explicitly permitted clinic name in Newsreader instead of assuming an inverted logo reads cleanly.
19. **Privacy and 404:** no privacy policy is supplied. Added a small Privacy route describing the implemented map/draft/review behavior and a visible owner-approval confirmation box. The 404 uses the specified sentence with plain Home, Services and Visit links.
20. **End-of-life CTA exception:** the sidebar uses “Call us to talk it through”. Shared header/menu/action-bar Book buttons are suppressed on this page to honour its no-Book-buttons instruction; the footer keeps its plain navigation link. Its phone action bar therefore has Call and Directions only.
21. **No-JS behavior:** page content and FAQ answers render server-side; JS adds the accordion/filter behavior. The visitor-date seasonal block appears only when JS can determine the date. Maps require the specified click and JS, with a normal map link fallback.
22. **Review screenshots:** no screenshot substitute was invented when Chromium was unavailable. The test produces them in review/ on the reviewer's machine.

## Source facts not placed / confirmation items

- The source biography's “licensed by the AVMA” wording is not asserted as a verified credential. A visible confirmation box asks for the licensing-body wording; the prescribed Canadian/BC association memberships are shown.
- Clinic founding year is not asserted. The footer uses the brief's exact since-2007 line.
- Kirsten's pet ages were omitted because the supplied ages are time-sensitive; pet names and species remain. Source pronoun inconsistency was normalised to family wording.
- The contact message form's “within the next 24 hours” is not reused as a booking callback promise. Booking keeps `[CONFIRM: how soon do you call back?]`.
- `resources_how-to-videos.md` and the source navigation's Pet Supplies/Pet Care Tips/promotional calls to action have no destination in the requested page plan and were not added as new sections.
- Extra source staff/marketing claims, dated headline statistics, source service-grid repetition and blog author/tag/sidebar boilerplate were omitted rather than turned into new claims or decorative sections.
- Other visible confirmations cover the emergency hospital and signs-list approval; newer Dr. Garg portrait; current team and Carrie's photo; holiday hours, parking, wheelchair access and email; accepting patients, payment/cancellation; Halloween wording; callback time; privacy policy. `SHOW_CONFIRM=True` in build_v2.py controls the shared confirmation helper.
