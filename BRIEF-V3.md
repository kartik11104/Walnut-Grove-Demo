# V3: Owner answers + signature UX pass

This adds to BRIEF-V2.md and overrides it where the two differ. All V2 rules in section 0 still apply: you build, you don't design; facts come only from source/text and this file; photos come only from assets/photos.

Work on branch `v3-build` from main. Commit per numbered item and push.

## A. Owner answers: replace these [CONFIRM] boxes with final copy

**A1. Emergency hospital** (emergency sheet, Pet care, the "Is it urgent?" note on every page)
- Text: "During our opening hours, we take emergencies. Call (604) 888-2628 and tell us you're on the way."
- Then: "When we're closed, go to the **Animal Emergency Clinic of the Fraser Valley**, open 24 hours: 6325 204th Street, Unit 302, Langley. (604) 514-1711."
  - Give it a Call button (`tel:+16045141711`) and a Directions link (Google Maps search for that address).
- The emergency sheet must show the right one first, using the live open or closed state:
  - when we're open, our number comes first;
  - when we're closed, the emergency clinic comes first, and the heading reads "We're closed right now."

**A2. Approvals:** remove the "Dr. Garg approves" boxes from the emergency signs list and from the Halloween text. Both are approved as written.

**A3. FAQ "Visiting us" answers:**
- New patients: "Yes, we're welcoming new clients. Book online or call us."
- Payment: "Credit card, debit card and cash."
- Late or cancelling: "Running a few minutes late? We can usually still see you if you're 10 to 15 minutes late, but please try to arrive on time. If you need to cancel, call us so we can offer the time to another pet."

**A4. Booking success:** in place of the callback box, use "We'll call you back as soon as we see your request during opening hours."

**A5. Visit page:**
- Holiday hours: "Holiday hours can change. We post them on our Google listing." The link goes to `https://www.google.com/maps/search/?api=1&query=Walnut+Grove+Animal+Hospital+Langley`.
- Parking: "Parking is easy. We're in a busy plaza with plenty of spaces, including some right beside our door."
- Access: "Wheelchair accessible."

**A6. Email:** remove the email line and its box everywhere until it is supplied. Keep a commented-out `email` key in clinic.json.

**A7. Dr. Garg's credentials:** replace the licensing box with "Member of the Canadian and BC Veterinary Medical Associations. Registered with the College of Veterinarians of British Columbia." Drop the AVMA wording.

**A8. Team list:** the list is current, so remove "is this team list current?". Keep the boxes for Carrie's photo and for a larger portrait of Dr. Garg; new photos are coming.

**A9. Privacy:** remove the privacy approval box. The policy is approved.

## B. Contrast and rhythm: pages should not all feel the same

Add one dark section style: `.band-dark`.
- Background: `--walnut-deep` #2B201A.
- Heading colour #F7F3EC. Body text #E6DDCF. Links #F2C98A, underlined.
- Primary button on dark: background #F7F3EC, text #2B201A, hover #FFFFFF.
- Secondary button on dark: 1.5px #E6DDCF border with #F7F3EC text.
- Full-bleed, with the content kept on the normal grid. Padding 96px top and bottom on desktop, 64px on phone.

Every pairing must pass WCAG AA; check them in the tests.

Where the dark bands go (one or two per page, never back to back with the footer; put a 96px paper gap before the footer):
- **Home:** "Meet Dr. Garg" becomes a dark band. Its photo gets a 6px #F7F3EC border.
- **Team:** the Dr. Garg feature row is a dark band.
- **Visit:** the map and "Finding us" block is a dark band, with the map placeholder on a #3A2C24 box.
- **Services index:** a closing band reading "Not sure what your pet needs? Call (604) 888-2628 and we'll point you in the right direction." with a Call button and a Book button.
- **FAQ:** the same idea as the closing band, reading "Didn't find your answer?"
- **Service pages:** no dark band. They stay calm.

Also add one accent surface, `.band-soft`, with background #EFE7DA. Use it for the home "Three plain facts" row and for the "Your first visit" section.

## C. Signature interactions (build exactly these, nothing more)

**C1. Home: "What brings you in?" picker.** It goes directly under the hero, on a `.band-soft` surface.
- Heading: "What brings you in today?"
- Two rows of chips, using the booking chip style:
  - Pet: Dog, Cat, Rabbit or small pet.
  - Need: Check-up or vaccines, Something's wrong, Teeth, Surgery or spay/neuter, New puppy or kitten, Saying goodbye.
- Once both rows are chosen, a result panel appears below (220ms height animation). It holds:
  - one sentence;
  - a link to the matching service page;
  - a primary button "Book this visit" linking to `/book/?species=dog&reason=wellness` (prefill the booking form from these query parameters).
- Map of needs to service, sentence and booking reason:
  - check-up → Wellness exams: "A yearly exam and vaccines keep small problems small." Reason: wellness.
  - something's wrong → Is it urgent? Show the emergency signs list in short form plus Call, then "Not urgent? Book a sick visit". Reason: sick.
  - teeth → Dental care: "Bad breath or a sore mouth often means dental disease. We'll take a look." Reason: dental.
  - surgery → Spay and neuter / Pet surgery: "We'll start with a consult and explain every step." Reason: surgery.
  - new puppy or kitten → Puppy and kitten care: "First vaccines, deworming and a plan for the first year." Reason: wellness.
  - saying goodbye → End-of-life care: "We're here to help you decide when it's time, gently." No Book button, only "Call us to talk it through".
- For Rabbit or small pet, add the line "We see rabbits and pocket pets too." and also link Small mammal medicine.
- The result panel is `aria-live="polite"`. Every part of the picker must work by keyboard.

**C2. Visit: live weekly hours chart.** It replaces the plain table on /visit/ only; keep the table on home and in the footer.
- Seven rows, Mon to Sun. Each row has a horizontal track running from 6:00 to 22:00, with the open span filled #1E4E79 and the times labelled at its ends.
- A vertical #A3361F 2px line marks "now" in Vancouver time, on today's row, with the label "Now". Today's row is bold.
- Below the chart: "Open now · closes at 7 pm", using the same logic as the today line.
- Under 600px, the tracks stay full width and the labels sit above each track.
- The visually hidden accessible version is the existing table.

**C3. Pet care: instant plant checker.** This replaces the plain plant filter input.
- A large input (56px, Newsreader 1.4rem placeholder "Type a plant, like lily or tulip").
- As someone types, show up to 6 suggestions in a listbox (ARIA combobox pattern, with arrow keys, Enter and Esc).
- Choosing a plant on the list shows a result card with a 4px #A3361F left border: "**{Plant} is on our poisonous plant list.** If your pet chewed or ate it, call us now: (604) 888-2628. After hours: Animal Emergency Clinic of the Fraser Valley, (604) 514-1711." It has Call buttons.
- When there is no match after 3 or more characters, the card has a #2F6B45 left border: "**{text} isn't on our list.** That doesn't mean it's safe. If your pet seems unwell, call us."
- Keep the full grouped accordion list below it.

**C4. Clinic wall lightbox.** Clicking a wall photo opens a dialog showing it at native size on a #1A1410 backdrop (opacity .92), with the caption, Prev and Next buttons, the arrow keys, and Esc to close.
- On phone, swipe left or right moves between photos.
- Focus is trapped while it is open and returns to the photo on close.
- Thank-you cards show at native width so the handwriting is readable.

**C5. Services index: group index with scroll-spy.** On desktop (≥900px), a sticky left column lists the four groups as links. The group currently in view gets the 2px `--walnut` left rule. Content sits in the right 9 columns. Phone has no sidebar.

**C6. Smooth page changes.** Add `@view-transition { navigation: auto; }` with a 180ms crossfade on root, plus `view-transition-name` on the header so it stays fixed during the change. Disable it under prefers-reduced-motion. Browsers without support just navigate normally.

**C7. Header on scroll.** On phone, the header hides when scrolling down more than 8px after 200px, and shows again when scrolling up (transform, 200ms). Desktop keeps the header always visible. Never hide it while the menu is open.

**C8. Booking prefill:** read the `species` and `reason` query parameters, preselect those chips, and announce "We've filled in what you picked." in the step's live region.

**C9. Team: "Their pets".** Each person's "Pets at home" line becomes a small row of plain text tags (#EFE7DA background, radius 4px, 0.9375rem). These are the only tags allowed on the site.

## D. Done means
- `tests/test_v2.py` is extended to cover:
  - every C item works by keyboard;
  - AA contrast checks on `.band-dark` and `.band-soft` text and buttons;
  - the emergency sheet order at mocked open (Tue 10:00) and closed (Tue 21:00) times;
  - the picker prefill reaching /book/;
  - plant checker hit and miss cases;
  - lightbox Esc and focus return;
  - no horizontal scroll at 390 and 1280;
  - zero console errors;
  - zero form submissions.
- No `[CONFIRM` text remains except: Carrie's photo, the larger portrait of Dr. Garg, and the clinic email (hidden).
- Report item by item (A1 to C9) with what you built, the test output, and an Unspecified list.
