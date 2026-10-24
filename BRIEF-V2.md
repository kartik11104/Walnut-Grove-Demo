# Walnut Grove Animal Hospital: Website V2 Brief

Owner: Claude (design director). Builder: Codex.
This brief replaces DESIGN.md, DESIGN-CHANGES.md and template.html. Do not reuse anything from the V1 template.

## 0. Rules for the builder (read first)

1. **You build and you do not design.** Every visual decision is set here. If something is not specified, pick the plainest option that fits this brief, then list it under "Unspecified" in your report. Never add anything decorative on your own: no icons, no badges, no animations, no gradients, no shadows, no emoji.
2. **Facts come only from `source/text/*.md`**, which is the clinic's current site. You may rewrite and shorten them, but never invent facts, prices, statistics, reviews, awards, years, staff details or medical claims. If you need a fact that is missing, put `[CONFIRM: what is needed]` in the page. It must render as a visible dotted-outline box, styled `.confirm`.
3. **Photos come only from `assets/photos/`.** These are the clinic's real photos. **Never use stock images or AI-generated images**, and never use anything in `source/img/` except through `assets/photos/`. Many photos are small (about 230–280 px). **Never show a photo larger than its native pixel width.** Section 4 says where each photo goes.
4. Use Canadian spelling (neighbourhood, colour, centre). Copy should read at about a grade 7–8 level. Use short sentences, write "we" and "you", and use no exclamation marks. Never use these words: "furry friends", "fur babies", "state-of-the-art", "cutting-edge", "comprehensive", "seamless", "elevate", "unparalleled", "journey", "peace of mind". Do not use em dashes in the copy.
5. Commit after each page with a clear message. Work on branch `v2-build` and push it.

## 1. The idea

Walnut Grove Animal Hospital is a small, long-running neighbourhood clinic: one vet, Dr. Rattan Garg, in practice since 1983 and at this clinic since 2007, with a few long-serving staff, in a strip-mall unit on 88 Avenue with a blue sign.

The site should feel like that place: **warm, plain-spoken, local and well made.** It should read like a good local bookshop or community paper, not a tech startup, and it must not look like an AI template.

Things that make a site look AI-made are **banned**:
- tiny UPPERCASE tracked "eyebrow" labels above headings
- pill badges or chips used as decoration (chips are allowed only as form controls on the booking page)
- rows of three identical cards that each end in "Learn more →"
- big-number stat strips such as "400k+ cases"
- icons inside circles
- gradient blobs or gradient text, glassmorphism, and soft drop shadows on everything
- stock photos
- centred text everywhere
- the same section rhythm repeated down the page
- teal-and-coral palettes
- Inter, Poppins or Fraunces fonts

What we use instead: editorial typography, real photos, hairline rules, asymmetric layouts, generous whitespace, honest and specific copy, and small acts of care in how things work.

## 2. Design tokens (exact)

```
--paper:#F7F3EC   page background
--card:#FFFDF9    raised surfaces (booking panel, menus)
--ink:#211E1A     body text
--ink-2:#57514A   secondary text
--ink-3:#7A7268   captions, meta (use only at 15px or larger)
--line:#E2DACC    hairlines, borders
--walnut:#5A3B2A  brand accent: rules under H1, link underlines, the active nav underline
--walnut-deep:#2B201A footer background (text on it is #F1EBE1)
--blue:#1E4E79    primary buttons and links (the colour of the clinic's real sign); hover #163C5E
--blue-soft:#E6EDF4 the selected state in forms
--alert:#A3361F   emergency text and borders only
--ok:#2F6B45      "Open now" dot and success text
```
Light theme only. No dark mode.

**Type** (Google Fonts, `display=swap`; preload both woff2 files):
- Headings: **Newsreader**, weight 500, optical sizing on, letter-spacing -0.01em.
  - H1: clamp(2.4rem, 5vw, 4rem), line-height 1.05
  - H2: clamp(1.75rem, 3vw, 2.4rem), line-height 1.15
  - H3: 1.35rem
- Body: **Public Sans** 400/600. Size 1.0625rem (17px), line-height 1.6. Text measure 64ch at most.
- Small text: 0.9375rem. Never smaller than 14px.
- Links in running text: `--blue` with an underline 1px, offset 3px. On hover the underline turns `--walnut`.

**Space:** a 4px base. Use the steps 4 8 12 16 24 32 48 64 96 128 px. Gaps between sections are 96px on desktop and 64px on phone.

**Layout:** a 12-column grid, max width 1200px, 24px gutters. The page gutter is 20px on phone and 32px on tablet.

**Radius:** 6px on buttons and inputs, 4px on photos, 0 on sections.

**Buttons:**
- Primary: `--blue` background, white text, height 48px, padding 0 22px, Public Sans 600 at 1rem.
- Secondary: transparent, with a 1.5px border in `--ink` and `--ink` text.
- Focus ring on everything: `outline:3px solid #1E4E79; outline-offset:3px`.
- Buttons must never take a full-width coloured band behind them.

**Rules:** use a 1px `--line` hairline between sections where a change is needed, instead of background colour blocks. Only the footer and the emergency sheet use their own backgrounds.

**Motion:** keep it minimal.
- Links and buttons: colour transitions only, 150ms.
- Accordion: height animation, 220ms ease-out.
- Clinic-wall photos: straighten on hover, 200ms.
- Nothing fades in on scroll.
- Respect `prefers-reduced-motion`.

## 3. Global components and behaviour

### Header (sticky, 72px tall, `--paper` background, hairline bottom border once scrolled)
- **Left:** the logo (`assets/logo.png`) at 40px tall, linking home.
- **Centre-right nav:** Services · Our team · Pet care · Blog · Visit. Use a 2px `--walnut` underline under the current page.
- **Right:** the phone as a text link `(604) 888-2628`, then the primary button "Book a visit".
- **Above the header:** a 32px "today line" in `--ink-2` at 0.9375rem, computed live in America/Vancouver time:
  - Open: `● Open today until 7 pm` (the dot is `--ok`).
  - Within 30 minutes of closing: `● Closing soon, at 7 pm` (amber #8A5200).
  - Closed: `Closed now · Opens tomorrow at 8:30 am`, or `Opens today at 9 am` when that is the case.
  - The right side of this line shows `Pet emergency?`, a link in `--alert` that opens the Emergency sheet.
- **Phone (under 900px):** keep the logo and a "Menu" text button (not a hamburger icon). The menu opens as a full-height sheet with the nav in large Newsreader, then Call and Book buttons. Trap focus in it, close it with Esc, and lock page scroll while it is open.

### Phone action bar (under 900px)
Fixed to the bottom, 64px tall, `--card` background with a top hairline. It has three equal buttons: **Call**, **Directions**, **Book**. Add bottom page padding so it never covers content. Hide it on /book/.

### Emergency sheet
A dialog (`role="dialog"`, `aria-modal`). Heading: "Is this an emergency?"
- "During our hours, call us now and tell us you're on the way: (604) 888-2628", with a big Call button.
- "After hours, go to the nearest 24-hour emergency hospital." Then `[CONFIRM: name, address and phone of the 24-hour emergency hospital Dr. Garg recommends]`.
- "Signs that need care right away:" difficulty breathing; collapse or seizure; suspected poisoning (chocolate, xylitol, lilies for cats, rat bait, medications); a swollen, hard belly with retching in dogs; a male cat straining to pee; heavy bleeding; hit by a car. This list is standard first-aid guidance; mark it `[CONFIRM: Dr. Garg approves this list]`.

### Footer (`--walnut-deep`, text #F1EBE1)
Four columns that stack on phone:
1. Logo (white version: apply CSS `filter: brightness(0) invert(1)` only if it reads cleanly; otherwise use the name in Newsreader) and one line: "Caring for Walnut Grove's pets since 2007." (Source: Dr. Garg joined in 2007. The clinic's founding year is `[CONFIRM]`, so the line says "since 2007" only.)
2. Visit: address, phone, Google Maps link.
3. Hours: the full week.
4. Links: Services, Our team, Pet care, FAQ, Blog, Book, Instagram, Facebook.
Bottom row: "© 2026 Walnut Grove Animal Hospital" · Privacy.

### Confirm boxes
`.confirm` is inline-block, with a 1.5px dotted `#8A5200` border, `#FBF3E6` background, `#6B4000` text, 0.9375rem, and 2px 8px padding. They must be easy to find in review. A single constant `SHOW_CONFIRM=true` in the build turns them all on and off.

### Hours data (one source of truth: `data/clinic.json`)
Mon–Fri 8:30–19:00; Sat–Sun 9:00–17:00. Holidays: `[CONFIRM]`.
- Phone: (604) 888-2628 (`tel:+16048882628`).
- Address: 101A-20995 88 Ave, Langley, BC V1M 2C9.
- Map: 49.16296, -122.63920.
- Instagram: walnutgroveanimalhospitalbc. Facebook: walnutgroveanimalhospitalbc.

## 4. Pages: structure and exact copy

Copy in quotes is final. Copy marked (from source) means: condense it from that `source/text/` file, following the rules in 0.4.

### 4.1 Home `/`

1. **Hero.** Two columns on desktop: text in 7 columns, photo in 5. On phone the text comes first.
   - H1: "Your neighbourhood vet in Walnut Grove."
   - Lead (1.25rem, `--ink-2`): "Dr. Rattan Garg and a small team who get to know your pet by name. Open seven days a week on 88 Avenue in Langley."
   - Buttons: **Book a visit** (primary) and **Call (604) 888-2628** (secondary).
   - Under the buttons, one quiet line: "New to us? Bring any past records. We'll take it from there."
   - Photo: `building-exterior.webp`, shown at its native width (see sizes in assets/photos; never upscaled), radius 4px. Caption in `--ink-3` below it: "101A-20995 88 Ave. Look for the blue sign."
2. **Three plain facts.** A row with 1px vertical rules between items; no icons and no big numbers. Body size, the first words bold:
   - "**Open 7 days.** Weekdays until 7 pm."
   - "**Dogs, cats and small mammals.** Rabbits and pocket pets too."
   - "**Tests on site.** In-house lab, digital X-ray and ultrasound."
3. **What we do.**
   - H2 "What we do", left-aligned, with a "See all services" link to the right of it.
   - Below: four columns (two on tablet, one on phone). Each column has an H3 and a plain list of text links, each link going to its service page:
     - **Everyday care:** Wellness exams · Vaccines · Parasite prevention · Puppy and kitten care · Microchipping
     - **Finding answers:** Bloodwork · Lab services · Digital X-ray · Ultrasound
     - **Surgery and dental:** Spay and neuter · Pet surgery · Soft tissue, eye and ear surgery · Dental care · Anesthesia
     - **Ongoing care:** Skin and ear problems · Chronic pain · Small mammal medicine · Dog breeding · Boarding · End-of-life care
4. **Meet Dr. Garg.**
   - Asymmetric layout: the photo `dr-rattan-garg.webp` at 250px native (do not enlarge) on the left, with the text in 6 columns.
   - H2 "Meet Dr. Garg".
   - Text: "Dr. Rattan Garg has worked in veterinary medicine since 1983, including years with the Canadian Food Inspection Agency and Metrotown Animal Hospital. He has looked after Walnut Grove's pets since 2007. His special interests are surgery and dog and cat medicine. At home there are two cats, Cinder and Emma, and a dog named Rocky."
   - Link: "Meet the whole team".
   - Add `[CONFIRM: a newer, larger portrait of Dr. Garg]` beside the photo.
5. **Your first visit.**
   - H2 "Your first visit".
   - An ordered list of three. Each item has a large Newsreader numeral in `--walnut` with a short H3 and one line:
     1. "Book" / "Pick a time online or call us. We'll confirm by phone."
     2. "Bring what you have" / "Past records, a list of food and medicines, and a leash or carrier."
     3. "Leave with a plan" / "We explain what we found, the options and the cost before any treatment."
6. **The clinic wall** (the signature section).
   - H2 "From our clinic". Sub: "Real patients, real thank-you cards. Follow along on Instagram."
   - A loose collage of 8 photos: `thank-you-card-1`, `golden-retriever`, `assistant-with-kitten`, `dachshunds`, `thank-you-card-2`, `poodle`, `kitten-held`, `tabby-on-table`.
   - Each photo has a white 8px border (like a print), a rotation of −2°, 1.5°, −1° and so on (a fixed pattern, not random), and a hairline shadow `0 1px 2px rgba(0,0,0,.12)`. On hover or focus it rotates to 0°.
   - Shown at native size or smaller. Desktop: a CSS grid of four columns with varied row offsets. Phone: a horizontal scroll-snap row.
   - Alt text must describe each photo.
7. **Reviews.** Render this section only if `data/reviews.json` has entries; ship it empty so the section is hidden. Never write reviews. When filled, show them as up to 3 quotes in Newsreader italic, each with the first name and "Google review".
8. **From the blog.** H2 "From the blog". The latest 3 posts as a text list: title (an H3 link), date, read time, and a one-line summary. No images.
9. **Visit block.**
   - Two columns. Left: H2 "Come and see us", the address, the full week of hours as a table with today's row bolded and a `--walnut` left rule, and the phone.
   - Right: a map. Load the map iframe only after a click on a "Show map" button, which is a static paper box with the address. This is for privacy and speed.
   - Buttons: Get directions (Google Maps) and Apple Maps.

### 4.2 Services `/services/`
- H1 "Services". Lead: "Everything we offer, from first vaccines to surgery. Not sure what you need? Call us and we'll help."
- A search input labelled "Find a service". It filters the list live and shows "No match. Call us at (604) 888-2628 and ask." when nothing matches.
- The same four groups as on the home page. Each item is a row: the service name as an H3 link, and one sentence (from source) beside it on desktop or below it on phone. Rows are separated by hairlines. No cards and no images.

### 4.3 Service page `/services/<slug>/` (19 pages; slugs exactly as in `source/text/services_<slug>.md`)
- Breadcrumb: Services / Name.
- Layout: content in 8 columns, a sticky sidebar in 4 (desktop).
- H1: the plain-English name, e.g. "Vaccines", "Spay and neuter".
- Summary: 1 paragraph, 45 words at most (from source).
- **"When to come in":** a bullet list (from source; if the source has none, omit the section).
- **"What we do":** from source, rewritten into short paragraphs and bullets.
- **"Before your visit":** only if the source supports it (fasting before ultrasound and anesthesia, and so on; the FAQ file has some of this). Otherwise omit.
- **"Questions":** the relevant Q&As from `source/text/faq.md` as accordions.
- **Sidebar card** (`--card`, hairline border): "Book this visit" (primary), the phone, today's hours line, and "Is it urgent? Call us first."
- **Related services:** 3 text links.
- No photos on service pages.
- End-of-life care page: gentle tone, no buttons labelled "Book"; use "Call us to talk it through" instead.

### 4.4 Our team `/team/`
- H1 "The people who'll look after your pet".
- Lead: "We're a small clinic on purpose. You'll see familiar faces at every visit."
- **Dr. Garg:** a feature row with the photo, the full bio from source, and credentials as plain text: "Member, Canadian and BC Veterinary Medical Associations." Then "Pets at home: Cinder and Emma (cats), Rocky (dog)."
- **Then each team member**, in a two-column grid with photo, name in an H3, role, a 2–3 sentence bio (from source), and "Pets at home: …" (from source; this is the human detail, so keep it):
  - **Kirsten Jensen**, Reception: `kirsten-jensen.webp`.
  - **Jasleen Gill**, Veterinary assistant: `jasleen-gill.webp`.
  - **Carrie Bartlett**, Veterinary assistant: no photo, so show a paper-coloured 4:5 box with her initials in Newsreader and `[CONFIRM: photo of Carrie]`.
  - Add `[CONFIRM: is this team list current?]` once, at the top of the grid.
- **"Inside the clinic":** three photos (`clinic-interior`, `treatment-room`, `exam-room`) at native size, each with a caption.
- **"What we believe":** the mission from source, at 3 sentences at most.

### 4.5 Visit `/visit/`
- H1 "Visit us".
- **Address block:** the address in large Newsreader, then the buttons "Copy address" (shows a toast reading "Address copied"), "Google Maps" and "Apple Maps".
- **Hours table:** as on the home page, plus the line `[CONFIRM: holiday hours]`.
- **"Finding us":** `storefront.webp` and `storefront-sign.webp` side by side, and the text "We're in the plaza on 88 Avenue. Look for the blue Walnut Grove Animal Hospital sign." Then `[CONFIRM: parking details]` and `[CONFIRM: wheelchair access]`.
- **Map:** the click-to-load map.
- **"Get in touch":** the phone; email `[CONFIRM: clinic email]`; Instagram; Facebook.

### 4.6 Pet care `/pet-care/`
- H1 "Pet care". Lead: "Practical advice from our team, and the places to check when you're worried."
- Then these blocks, each with an H2:
  1. **"Is this an emergency?"** The emergency signs list from the sheet, with a Call button (`--alert` border on the left, 4px).
  2. **"Plants that are poisonous to pets"** (from `resources_poisonous-plants.md`). The intro paragraph, then a filter input ("Search a plant"), then each group as an accordion that opens to a multi-column list. The note "If your pet ate something on this list, call us right away" stays visible.
  3. **"Halloween safety"** (seasonal; show it from Oct 1 to Nov 7, using the visitor's date). Text: "Chocolate, especially dark and baking chocolate, and anything sweetened with xylitol can poison dogs. Keep the candy bowl out of reach, keep pets inside and away from the door on the night, and make sure costumes don't limit breathing or movement." Then `[CONFIRM: Dr. Garg approves]`.
  4. **"Pet food recalls"** (from `resources_pet-food-recalls.md`). One paragraph plus links to the official recall sources named in the source file.
  5. **"Latest articles"**: the 3 newest blog posts, linking to /blog/.

### 4.7 FAQ `/faq/`
- H1 "Questions we hear a lot".
- Search input: "Search questions".
- Groups as H2s, each holding accordions (all Q&As from `faq.md`, rewritten plainly, with every answer 80 words at most):
  - Visiting us: hours, where we are, `[CONFIRM: are you accepting new patients?]`, `[CONFIRM: payment methods]`, `[CONFIRM: what if I'm late or need to cancel]`.
  - Surgery and anesthesia.
  - Vaccines and prevention.
  - Tests and imaging.
  - Spay and neuter.
  - Breeding.
  - End-of-life care.
- Accordions: a `<button aria-expanded>` with a plus/minus drawn in CSS (two 1.5px bars, no icon font). Opening one does not close the others. The URL hash opens a question directly (`/faq/#q-<slug>`).
- Add FAQPage JSON-LD.
- End: "Didn't find it? Call (604) 888-2628."

### 4.8 Blog `/blog/` and posts `/blog/<slug>/` (5 posts from `source/text/blog_*.md`)
- **Index:** H1 "Pet health blog". Lead: "Plain answers to common questions, from our team in Langley."
  - The featured post is the newest: a large Newsreader title (H2 size), date · read time, a 2-line summary, and a "Read the article" link.
  - Below it, the rest as a list with hairlines between items.
  - No cover images. The live site's covers are AI-generated, so do not use them.
- **Post page:**
  - Width 68ch, centred column.
  - Breadcrumb Blog / Title. Then the H1, then a meta line "Walnut Grove Animal Hospital · Oct 20, 2026 · 8 min read" (use the real dates from `blog.md`).
  - Desktop: a sticky "On this page" table of contents on the left, built from the H2s.
  - Body: from source, keeping the clinic's text. Clean only the formatting and remove the navigation junk at the top of each file.
  - End box: "Questions about this for your pet? Book a visit or call (604) 888-2628."
  - Then 2 related posts.
  - Add Article JSON-LD.

### 4.9 Book `/book/` (it must work for real)
The form submits to the clinic's existing Google Form, which is where requests already go today:
- Endpoint: `https://docs.google.com/forms/d/e/1FAIpQLScJA4N82tv0x5Ek5wLkXZteAvFi0kyf3CBZqdagPe8AmGja3w/formResponse`
- Fields:
  - `entry.2005620554` Name (required)
  - `entry.1313180264` Phone (required)
  - `entry.1065046570` Pet name
  - `entry.1166974658` Species
  - `entry.839337160` Breed
  - `entry.680478738` Reason and comments
  - `entry.1358010904` Preferred date: send `entry.1358010904_year`, `_month` and `_day`
  - `entry.898890459` Preferred time: send `entry.898890459_hour` and `_minute`
  - `entry.2096389996` Note

**Send method:** `fetch(endpoint,{method:'POST',mode:'no-cors',body:new URLSearchParams(...)})`. A thrown network error counts as a failure; an opaque response counts as success.

**Safety switch:** `data/clinic.json` → `"bookingLive": false`. While it is false, the form runs the whole flow but **does not send**. The success screen then adds "Review mode: this request was not sent." Claude switches this to true only after the owner approves. Never submit test data to the real form.

**Layout:** a centred `--card` panel, 640px max, with a hairline border and radius 6px. Above it: H1 "Book a visit" and the lead "Send a request and we'll call you to confirm a time. For anything urgent, call (604) 888-2628 now."

**Steps:** a progress line of 3 labelled steps as plain text with a 2px `--walnut` bar. Back and Next buttons. The URL hash follows the step so the browser back button works.

1. **You and your pet**
   - Your name; phone (it formats as you type, and is valid with 10 digits).
   - Pet's name.
   - Species: chips Dog, Cat, Rabbit, Other small mammal, Other. "Other" reveals a text field. The chips are radio inputs.
   - Breed (optional).
   - "Have you been here before?" Yes/No. This goes into Note.
2. **What it's for**
   - Reason chips: Wellness exam or vaccines, Sick or injured, Follow-up, Dental, Surgery consult, Other.
   - Choosing "Sick or injured" shows an inline `--alert`-bordered note: "If your pet is struggling to breathe, has collapsed, or may have eaten something toxic, call us now instead of booking." It includes a Call button.
   - A comments textarea (maximum 500 characters, with a counter).
   - Preferred date: a strip of the next 14 days as buttons, with closed days skipped (all days are open, so show all 14). The preferred time is a radio: Morning, Afternoon, Evening (weekdays only; disable it on Sat and Sun). Map Morning to 10:00, Afternoon to 14:00 and Evening to 17:30, and also write the word into Note.
3. **Check and send**
   - A summary list with "Edit" links back to each step.
   - The sentence "This is a request, not a confirmed appointment. We'll call you at {phone} to confirm."
   - The "Send request" button.

**Validation:** on blur and on Next. Errors appear under each field (`aria-invalid` and `aria-describedby`). On Next with errors, move focus to the first invalid field.

**Success:**
- H2 "Request sent", then "Thanks, {name}. We'll call you at {phone} to confirm a time for {pet}." Then `[CONFIRM: how soon do you call back?]`.
- Buttons: "Add our number to contacts" (download a vCard), "Back to home".

**Failure:** "That didn't go through. Please call us at (604) 888-2628." Keep everything the person entered.

**Draft:** save the form to localStorage (inside try/catch) and restore it on return. Clear it on success.

## 5. Technical
- **Static multi-page site.** Python 3 with Jinja2 (`build_v2.py`), templates in `templates/`, data in `data/` (clinic.json, services.json, faq.json, posts.json, plants.json, reviews.json). Output goes to `site/`.
- Commit the built `site/` (Vercel serves it as is; `vercel.json` already points at `site`).
- **One CSS file:** `site/assets/site.css`, 40 KB or less.
- **One JS file:** `site/assets/site.js`, 30 KB or less. Use no frameworks. Pages must work without JS, except the booking steps, filters and the today line.
- **Images:** `<img>` with width and height set, `loading="lazy"` below the fold, and `decoding="async"`.
- **Each page has:**
  - A unique `<title>` in the form "Vaccines | Walnut Grove Animal Hospital, Langley".
  - A meta description of 155 characters or fewer.
  - Open Graph tags, using `building-exterior.webp`.
  - A canonical link.
  - `lang="en-CA"`.
  - A skip link.
  - One H1.
- **Schema:** VeterinaryCare JSON-LD on every page (address, geo, hours, phone, sameAs).
- **Also generate:**
  - `sitemap.xml`.
  - `robots.txt`, which stays `Disallow: /` and is matched by the noindex header in vercel.json until the site moves to the clinic's domain. That keeps it from competing with the live site on Google.
  - A 404.html page in the same style: "We can't find that page." plus links.
- Old hash URLs (`/#services` and so on) redirect to the new pages with a tiny script on the home page.

## 6. Done means (self-check before you report)
Run `python3 tests/test_v2.py`. Write it with Playwright, using the Chromium already installed. It must check, at 390×844 and 1280×800:
- Every page loads with no console errors and no horizontal scroll.
- Every internal link returns 200.
- Every image has alt text.
- There is one H1 per page.
- The booking flow completes by keyboard alone, with bookingLive false.
- Validation errors appear.
- The Emergency sheet opens and closes with Esc.
- The FAQ hash opens the right question.
- The today line is right for 3 mocked times (Tue 10:00, Tue 18:45, Sun 18:00).

Report in this format:
- Files changed.
- Test output.
- A screenshot of each page at both sizes, saved to `review/` (do not commit them; attach them in your report or put them in a branch `v2-shots`).
- The list of "Unspecified" decisions.
- Any source facts you could not place.
