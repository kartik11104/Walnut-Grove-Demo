# V3 build report

Branch: `v3-build`, from main `cf61706`. Each A item, B, and C item has a separate implementation commit. Booking remains in review mode (`bookingLive: false`). No real Google Form request was sent. Original source text and photos remain unchanged.

## Item-by-item implementation

| Item | Implemented |
| --- | --- |
| A1 | Approved clinic and Fraser Valley emergency contacts, Call buttons and address-specific Directions. The currently available contact is first; the closed sheet heading reads “We're closed right now.” Minute updates preserve focused links. Service urgency notes and Pet care share the same contact component. |
| A2 | Removed emergency-list and Halloween approval boxes; approved copy retained. |
| A3 | Published all three exact Visiting us answers inside their accordions. |
| A4 | Replaced the callback placeholder with the exact approved opening-hours callback sentence. |
| A5 | Published holiday-hours Google listing, parking and wheelchair-access copy. |
| A6 | Removed visible clinic email. Kept the pending email as inactive `_comment_email` JSON metadata, without an active email field. |
| A7 | Published the approved Canadian/BC associations and College registration wording; no AVMA claim. |
| A8 | Removed team-list approval; kept only the pending Carrie and larger Dr. Garg photo boxes. |
| A9 | Removed privacy approval box; approved policy retained. |
| B | Full-bleed dark bands at Home doctor, Team doctor, Visit finding/map, and Services/FAQ closing sections. Applied specified text/link/button colours, Home portrait border, map surface and paper gap before the footer. Home facts and first-visit sections use the soft surface. Content remains on the normal grid. |
| C1 | Two keyboard-native radio rows below the Home hero; animated polite result panel; all six need branches, emergency guidance, rabbit supplement and service links. Query links feed booking. Saying goodbye has only the prescribed Call action, with no Book button. |
| C2 | Seven-row Vancouver hours chart, 06:00–22:00 tracks, labelled opening spans, current-time marker and bold current day. Accessible table retained; Home/footer hours remain unchanged. |
| C3 | 56px Newsreader combobox, six source-order suggestions, Arrow/Enter/Escape handling, red hit and green miss results with exact safety wording, and both emergency Call links. Full accordion lists retained. Fixed an inherited extraction bug so all 13 source groups and 88 entries are available. |
| C4 | Clinic-wall native-size dialog, captions, Prev/Next, arrow keys, touch swipe, Escape, focus trap and opener restoration. Thank-you cards retain their native width. |
| C5 | Sticky three-column group index and nine-column service content from 900px; current group left rule and aria-current; no phone sidebar. |
| C6 | Native cross-document view transitions: 180ms root crossfade, separately named stationary header, reduced-motion opt-out and normal-navigation fallback. |
| C7 | Phone header hides after more than 8px of downward movement beyond 200px; returns on upward movement; remains visible on desktop or while the menu is open. |
| C8 | Species/reason query mapping preselects booking chips, with “We've filled in what you picked.” announcements on the relevant step. Other saved draft fields are preserved. |
| C9 | Four team pet rows use plain soft-background text tags, preserving source pet names/species. |
| D | Extended tests for keyboard interactions, native navigation/reduced motion, contrast, emergency state ordering, picker-to-book prefill, plant hit/miss/Escape, lightbox keyboard/swipe/focus, hours chart, pet tags and allowed confirmations. Existing page/link/image/copy/overflow/form-safety tests remain. |

## Build and test output

`python3 build_v2.py` succeeded:

```
V2 build: 35 pages; 20 services; 5 posts; bookingLive=False; SHOW_CONFIRM=True
CSS: 17296 bytes; JS: 21367 bytes
Canonical origin: https://walnut-grove-demo.vercel.app
```

The established build command/output label remains `build_v2.py` because V3 extends V2 rather than replacing its build system.

`python3 tests/test_v2.py` passed (exit 0), using system Chromium:

```
Static checks: 35 pages, 0 errors
V3 keyboard/interaction checks completed at 390px
V3 keyboard/interaction checks completed at 1280px
Page loads: 70; screenshots: 70; real form submissions: 0
ERRORS: []
```

Computed foreground/background checks pass AA for visible dark/soft-band text and controls, including dark primary hover. Exact prescribed colour pairs are also checked. Mocked tests cover Tue 10:00/Tue 21:00 emergency ordering, chart state, and the existing three today-line times. Reduced-motion and keyboard navigation remain functional. JavaScript syntax, Python compilation and `git diff --check` passed.

Screenshots: `review/` contains 70 page captures at 390×844 and 1280×800. They remain ignored and uncommitted.

## Unspecified

1. JSON does not support comments. The requested commented-out email is stored as the inert string `_comment_email`, containing the disabled email reminder. It renders nowhere and is not a booking payload field.
2. Soft-band padding was not separately specified: reused the prescribed dark-band 96px desktop / 64px phone spacing. Existing 600px/900px responsive boundaries remain.
3. The combined picker choice “Rabbit or small pet” uses `species=rabbit` and preselects Rabbit. The form still lets the owner change this to Other small mammal. Valid explicit `species=small-pet` selects Other small mammal. Invalid query values are ignored.
4. “Is it urgent?” has no service-page slug. Its picker link opens the shared emergency sheet; nonurgent booking uses `reason=sick`. Surgery links both named service pages. The sick branch uses the more specific prescribed “Not urgent? Book a sick visit” button label.
5. Picker result-height animation uses the existing accordion grid-row technique, 220ms ease-out. Booking-style chips retain the approved 44px states.
6. Closed chart status reuses the today-line closed sentence. Outside 06:00–22:00 the Now marker is hidden rather than showing a misleading time on the track; accessible live status remains. Unspecified chart geometry uses existing 16px/24px/32px/128px spacing values.
7. Plant suggestions retain source order and deduplicate repeated names, with a maximum of six. Arrow selection wraps. A miss never asserts safety. The full source list, including repeated group contents, remains below.
8. Lightbox Prev/Next wrap at the ends. Swipe threshold is 48px, using the existing spacing scale. Narrow screens keep native images in an internally scrollable image area instead of upscaling or reducing the thank-you cards.
9. Scroll-spy activates at the sticky header plus 24px gap; sidebar top is the existing 96px offset. Links work as ordinary anchors without JavaScript.
10. Native page crossfades use the browser's default easing because only their duration was specified. Unsupported browsers use normal links; reduced-motion disables the transition.
11. Phone header movement accumulates small downward deltas until they exceed 8px. Any upward movement reveals it. The existing 900px phone boundary is unchanged.
12. Explicit prefill parameters override only species/reason in a restored draft; name, phone and other entered fields are preserved. The live announcement is repeated when its corresponding step is entered.
13. Pet tags use 4px/8px padding and 8px gaps from the existing spacing scale. Source-paired pets remain paired (Cinder and Emma; Stewie and Louis); no pet facts were invented.
14. Services' closing sentence is split into its question heading and the remaining sentence. FAQ uses its exact requested closing heading with Call and Book actions. Call is primary and Book secondary, following the single-primary rule.

## Remaining confirmations

Only the larger Dr. Garg portrait and Carrie's photo are visibly pending. Clinic email is retained only in hidden inactive metadata. No other confirmation placeholders render.
