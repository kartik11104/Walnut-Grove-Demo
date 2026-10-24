# DESIGN.md  Walnut Grove Animal Hospital demo
Written by the design lead (Claude). Codex is the builder. READ THIS WHOLE FILE BEFORE EVERY TICKET.

## 0. The builder contract (most important)
- You are a builder, not a designer. Implement exactly what is written here. Do not choose colors, sizes, spacing, copy, icons, motion, or layout yourself.
- If something is not specified: use the nearest token from section 3, change nothing else, and list it under "Unspecified" in your report. Never invent.
- Never add facts. Clinic facts are fixed: Walnut Grove Animal Hospital, 101A-20995 88 Ave, Langley BC V1M 2C9, (604) 888-2628, Mon-Fri 8:30am-7pm, Sat-Sun 9am-5pm. Anything unknown stays as a visible [CONFIRM: ...] box.
- Keep AGENTS.md hard rules. Where this file is stricter, this file wins.
- Plain HTML, CSS, JS only. One file: template.html. No libraries, no new network calls, no new external fonts (the existing Google font link stays as is).
- Every ticket ends: run `python3 build.py dist/index.html`, commit on branch task/<ticket-id> from the latest main, push, report (what changed, what not changed, Unspecified, build output).

## 1. Design intent: "calm care, in one glance"
Visitors are often worried. The site must feel like the best front desk: calm, clear, quick, and kind. Beauty here means three things at once.
1. Outer beauty: generous space, one strong typeface pairing, real photography, restrained color.
2. Inner beauty: every state is designed (hover, pressed, focus, disabled, empty, error, success), nothing jumps, nothing is cut off, everything works by keyboard, screen reader, thumb and slow network.
3. Honest craft: no fake claims, no dark patterns, no clutter. Fewer things, each done properly.
Signature details (these make it feel crafted): the live "Open now / closes soon" status; a thumb-reach action bar on phones; step transitions in booking; a drawn check mark on success; smooth accordion; one-tap copy of the phone number on desktop; focus moves to the page title on every page change.

## 2. Principles the builder must preserve
P1 Calm: max one primary action per screen area. Never two competing filled buttons in the same row except Call + Book on Home.
P2 Hierarchy: one h1 per page. Headings in order. Text blocks max 62ch wide. Lead text 1 to 2 lines on phone.
P3 Thumb first: primary actions reachable at the bottom on phones. Tap targets min 44x44px, min 8px apart.
P4 Motion with meaning: motion explains change (where something came from, what changed). Never decoration that loops. Respect prefers-reduced-motion (section 6).
P5 No layout shift: images have width/height or aspect-ratio. Reserve space before content appears.
P6 Words: short, active, kind. Sentence case. No exclamation marks. No hype words. Numbers as numerals.
P7 Contrast: body text at least 7:1 on its background in both themes; large text and UI at least 4.5:1.
P8 Honesty: placeholders are visible and labelled; demo banner stays on every page.

## 3. Tokens (put these in :root, light and dark, replace the existing ones with these names; keep old names as aliases until every use is migrated)
Color roles (light / dark)
--bg #F6F8F7 / #0E1416 | --surface #FFFFFF / #162024 | --sunk #E9EFED / #1C292E | --line #D3DDDA / #2A3A40
--ink #1B100C / #EEF3F2 | --ink-2 #4F413B / #B3C0C2 | --ink-3 #6F625C / #8FA0A3 (captions only)
--teal #0B5E70 / #5BBBCB | --teal-ink #FFFFFF / #052329 | --teal-soft #DAECEF / #173338 | --teal-press #084A59 / #7FCBD8
--amber #A86806 / #E6B050 | --amber-soft #FBF0DC / #33281A | --alert #B42318 / #F4766C | --alert-soft #FDECEA / #3A1E1C | --ok #1B7249 / #62C795 | --ok-soft #E2F3EA / #14301F
Space (4pt grid): --s1 4px, --s2 8px, --s3 12px, --s4 16px, --s5 24px, --s6 32px, --s7 48px, --s8 72px, --s9 112px
Radius: --r-sm 8px, --r 14px, --r-lg 22px, --r-pill 999px
Type: display Young Serif; body Figtree; mono IBM Plex Mono (existing).
--fs-display clamp(38px, 6.2vw, 64px) line 1.04 letter-spacing -0.01em
--fs-h1 clamp(32px, 4.6vw, 48px) line 1.08 | --fs-h2 clamp(26px, 3.2vw, 36px) line 1.12 | --fs-h3 21px line 1.2
--fs-lead clamp(18px, 1.6vw, 20px) line 1.5 | --fs-body 17px line 1.6 | --fs-small 14.5px line 1.5 | --fs-eyebrow 12.5px mono uppercase letter-spacing .08em
Headings use text-wrap:balance; paragraphs text-wrap:pretty.
Elevation: --e1 0 1px 2px rgba(27,16,12,.06) | --e2 0 2px 4px rgba(27,16,12,.05), 0 12px 28px rgba(27,16,12,.08) | --e3 0 4px 8px rgba(27,16,12,.08), 0 24px 56px rgba(27,16,12,.16) (dark mode: same shapes with rgba(0,0,0,.35/.45))
Motion: --ease cubic-bezier(.2,.8,.2,1); --ease-in-out cubic-bezier(.65,0,.35,1); --d1 120ms; --d2 220ms; --d3 360ms; --d4 520ms
Layout: content max width 1160px; gutters 16px phone, 24px tablet, 32px desktop; section vertical rhythm 72px phone, 112px desktop (--s8 / --s9).

## 4. Component specs (state by state)
Button .btn: min-height 48px (56px for hero), padding 14px 22px, radius --r, font 600 16px Figtree, gap 8px.
primary: bg --teal, text --teal-ink. hover: bg --teal-press (pointer:fine only), translateY(-1px), --e2. active: translateY(0) scale(.98), --e1. focus-visible: 3px outline --teal, 3px offset. disabled: opacity .5, no pointer. All transitions --d1 --ease.
ghost: transparent, 1.5px --line border, text --ink; hover bg --sunk; active scale .98.
Icon buttons: 44x44 minimum.
Status pill .status: inline-flex, gap 8px, padding 6px 12px, radius pill, --sunk background, small text. Dot 8px. States: Open (dot --ok, text "Open now, until 5pm"), Closing soon (within 60 min of close; dot --amber, "Closing soon, at 5pm"), Closed (dot --ink-3, "Closed now, opens 8:30am tomorrow" or correct next opening). Computed in America/Vancouver time using the fixed hours. aria-live="polite" updates each minute.
Card .card: bg --surface, 1px --line border, radius --r, padding 24px, --e1. Interactive card: hover (pointer:fine) translateY(-2px) --e2, image scale 1.03 inside overflow hidden over --d3; active scale .99; focus-visible outline as button.
Input: min-height 48px, padding 12px 14px, radius --r-sm, 1.5px --line border, bg --surface, font 17px (prevents iOS zoom). focus: border --teal + 3px ring rgba(teal,.25). error: border --alert, message below in --alert with icon "!" and role="alert" text e.g. "Enter your pet's name." Labels always visible above (no placeholder-only labels). Helper text --ink-2 small.
Chip/pill filter: min-height 44px, padding 10px 16px, radius pill, 1.5px --line; selected: bg --ink text --bg. aria-pressed.
Accordion (FAQ): button row min-height 56px, plus/minus icon rotates 45deg over --d2. Panel opens by animating grid-template-rows 0fr to 1fr over --d3 --ease with inner overflow hidden. Multiple may be open. Reduced motion: instant.
Drawer (service details): right side panel width min(520px, 100vw), radius --r-lg on the left corners (desktop), full height; bottom sheet on phones (max-height 88vh, top radius --r-lg, drag handle bar 40x4px --line at top). Enter: slide from edge over --d3 --ease with scrim fade --d2. Focus trapped inside; Escape and scrim click close; body scroll locked; focus returns to the opener (re-find the opener by data-slug if the list re-rendered). aria-modal="true", role="dialog", labelled by its title.
Toast: bottom center, 16px above the action bar/safe area, radius pill, --ink bg, --bg text, 12px 18px, role="status". Enter fade+translateY 8px over --d2, auto hide after 2200ms.
Callout (emergency): bg --alert-soft, 1px --alert border at 40% alpha, radius --r, left 4px --alert bar, icon "!" in 28px circle. Title "Emergency?" 600.
Placeholder box [CONFIRM]: 1.5px dashed --amber, bg --amber-soft, radius --r, padding 14px 16px, mono tag "To confirm" then the [CONFIRM: ...] text.
Skeleton/empty states: Empty search: centered block: 40px circle icon "magnifier" outline, title "No match", text "Try another word, or call us on (604) 888-2628.", ghost button "Clear search".

## 5. Global behaviors (build in R1)
1. View routing: crossfade between views (old fades out --d1 then new fades in --d2 with translateY 8px to 0). On change: scroll to top (instant), set document.title to "<Page> | Walnut Grove Animal Hospital", move focus to the page h1 (tabindex=-1, no visible outline on programmatic focus), announce via a visually-hidden aria-live region "Page: <Page>".
2. Scroll reveal: elements with [data-reveal] fade up (opacity 0 to 1, translateY 14px to 0, --d4 --ease), once, via IntersectionObserver with rootMargin 0px 0px -8% 0px; stagger siblings by 60ms (max 5). If IntersectionObserver is missing or reduced motion is on, show immediately. Content must never be hidden if JS fails after load.
3. Mobile action bar: on phones (max-width 720px) a fixed bottom bar with "Call" (ghost) and "Book a visit" (primary), height 64px + safe-area-inset-bottom, bg --surface, top border --line, --e2. Slides up after the Home hero leaves view; always visible on other pages except Book. Hides when the keyboard is open (focus in an input) and on the Book page. Page content gets bottom padding so nothing is covered.
4. Copy phone: on pointer:fine devices, a small ghost button "Copy number" next to the phone on Visit and in the footer; copies (604) 888-2628; shows toast "Number copied". Fallback: select the text.
5. Header: sticky below the demo banner; on scroll down past 80px adds --e1 and shrinks logo height 38px to 32px over --d2. Nav active item has a teal-soft pill. Phone menu is a full-width sheet with 56px rows, Escape closes, focus trapped, scroll locked.
6. Print: @media print hides demo banner, nav, action bar, drawer; shows clinic name, address, phone, hours in black on white. Visit page prints cleanly.
7. Image handling: every img has alt (decorative: alt=""), width/height or aspect-ratio, loading=lazy except the hero (fetchpriority=high). Photos get radius --r-lg. Stock photos keep the "Stock photo, replace" tag.
8. Links to Google Maps use target=_blank rel=noopener and say "(opens in a new tab)" in the aria-label.

## 6. Reduced motion and no-JS safety
@media (prefers-reduced-motion: reduce): all durations become 0.01ms, no translate/scale, crossfades become instant, drawer appears without slide. Verify with the test (emulate reduced motion).

## 7. Page specs (exact order top to bottom)
### Home (#v-home)
1 Status pill. 2 h1 (display size): "Veterinary care in Walnut Grove". 3 Lead (max 36ch): "Care for dogs, cats and small mammals in Langley, seven days a week." 4 Actions: [Call the clinic (604) 888-2628] primary, [Book a visit] primary, [Get directions] ghost full width below; hero buttons 56px high. Phone: actions directly under lead, before the photo. 5 Hero photo (existing cat photo) radius --r-lg, 4:3 on phone, fills right column on desktop (two columns 55/45 from 960px). Stock tag bottom-left.
6 Facts strip: 4 cells (Today's hours, Address, Phone, We see) as a single card with hairline dividers; 2x2 on phone. Today's hours reflects the real day.
7 Emergency callout (copy: "Emergency?" / "During opening hours, call (604) 888-2628 on your way in." / "After hours, call the nearest 24-hour emergency clinic." / placeholder box [CONFIRM: after-hours emergency clinic name]).
8 "Some of our services": 6 interactive cards (existing slugs), each opens the drawer; link "See all services".
9 "Your first visit, in three steps": 3 numbered cards (existing copy).
10 "Find us": photo of storefront + address + two buttons (Hours and directions, Open in Google Maps). 11 Footer.
### Services (#v-services)
h1; search field (label "Search services", placeholder "e.g. dental"; clear X button appears when text present, 44px); category chips (All + 5); result count line "20 services" updating via aria-live; grid 1 col phone, 2 col tablet, 3 col desktop from 1040px, gap 24px; card = image 16:10, category eyebrow, name (h3), 2-line clamp intro, "Learn more" text with arrow that nudges 4px right on hover. Empty state per section 4. Drawer per section 4 with "Book this service" primary and "Call" ghost.
### Book a visit (#v-book)  (demo: sends nothing)
Layout: left form column (max 640px), right sticky summary card (from 960px); phone shows a collapsible summary above the action button.
Stepper: 4 labeled steps (Pet, Reason, Time, You) with a 4px progress track filling over --d3; completed steps show a check and are clickable to go back; aria-current="step".
Step 1 Pet: species as 3 large radio cards (Dog, Cat, Small mammal) 96px high with simple inline SVG icons; pet name input; client type radio "New client" / "Existing client".
Step 2 Reason: select from the 20 services plus "Not sure"; notes textarea (label "Anything we should know?"); emergency-word detection (chocolate, poison, toxic, breathing, seizure, collapsed, bleeding, hit by a car, can't walk, bloat) shows the Callout inline above the Next button: "This may be an emergency. Please call (604) 888-2628 now." with a primary Call button; the form still allows continuing.
Step 3 Time: 14-day date strip (horizontally scrollable, snap, arrow-key navigation, today labelled), closed days disabled with a reason in aria-label; time slots every 30 minutes within real hours as a radio group (arrow keys move, 44px tall, 3 columns on phone, 4 on desktop); slot in the past or last 30 minutes before closing disabled.
Step 4 You: owner name, phone (inputmode=tel), optional email, checkbox "Send me reminders" (default unchecked, plain label). Next button label "Review request".
Transitions: forward slides content from right 24px + fade --d3; back slides from left. Focus moves to the step heading. Back button on steps 2 to 4 keeps all typed values.
Done: SVG circle + check that draws (stroke-dashoffset, --d4), title "Request ready for <pet>", summary list, and the honest line: "This is a demo. Nothing was sent. To book now, call (604) 888-2628." with Call primary and "Start over" ghost. No data leaves the page; no localStorage.
Errors: inline per field per section 4, summary of errors not needed for single-field steps.
### Our team (#v-team)
h1 "Our team"; Dr. Rattan Garg card with [CONFIRM: short bio] and [CONFIRM: photo] placeholder boxes; "What to expect on your first visit" three short items (existing wording); no invented staff.
### Pet care (#v-petcare)
h1; "Signs of poisoning" callout first with the five signs as a list and a Call primary button; then two groups (Dogs, Cats) each a set of accordions (existing plant groups) with 56px rows; a short note "This list is not complete. If you are unsure, call us." [CONFIRM: Halloween wording] placeholder.
### FAQ (#v-faq)
h1; accordion list per section 4; items marked confirm show the placeholder tag; nothing in schema that is unconfirmed.
### Visit us (#v-visit)
h1; two columns: Hours card (table, today row highlighted with --teal-soft, "Open now" pill) and Address card (address, Copy number, Call, Get directions); [CONFIRM: parking], [CONFIRM: holiday hours]; storefront and entrance photos.
### Footer
Logo, address, phone, hours summary, links to the 7 pages, "Demo for review" line.

## 8. Build tickets (do them in order; one branch each, from the latest main)
R1 Foundation. Files: template.html. Tokens (section 3), buttons/inputs/cards/pills/toast/callout/placeholder components (4), global behaviors 1 to 8, reduced motion (6), print. Done when: every existing page renders with new tokens, no console errors, routing focus/title works, action bar works, toast works.
R2 Home page per section 7. Files: template.html (#v-home and CSS it uses).
R3 Services page + drawer per section 7. Files: template.html.
R4 Booking per section 7. Files: template.html.
R5 Team and Pet care per section 7. Files: template.html.
R6 FAQ and Visit and Footer per section 7. Files: template.html, build.py (FAQ list and schema only).
R7 Final polish: Lighthouse-style checks by hand (no new tools): no layout shift, image sizes, reduced motion, print, keyboard path through every page, 390px and 1300px in light and dark. Files: template.html, tests/test.py. Add tests: every page loads with no console errors; no horizontal overflow at 390px in both themes; every img has alt; Tab reaches every interactive element; reduced-motion emulation shows content.
Acceptance for every ticket is the reviewer's 7-point checklist (REVIEW.md) PLUS fidelity to this file. Anything off-spec is sent back with the exact line.
