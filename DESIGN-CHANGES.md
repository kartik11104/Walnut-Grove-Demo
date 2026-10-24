# DESIGN-CHANGES.md  amendments by the design lead. These OVERRIDE DESIGN.md.
A1 Amber contrast (accessibility fix). Light mode --amber becomes #8A5200 (5.66:1 on --amber-soft). Dark mode unchanged. Apply in the next ticket you do.
A2 Phone demo banner. At max-width 720px the demo banner is NOT sticky (position static, it scrolls away) and uses one compact line: "Demo for review. Forms send nothing." followed by the To confirm tag. On wider screens keep the existing sticky banner and text. The banner stays on every page. Header sticky offset must follow the banner state (0 when banner is not sticky).
A3 Reveal placement rule. [data-reveal] is placed by tickets R2 to R6 only on: section headings, cards in grids, and photos. Never on the h1, status pill, hero buttons or anything in the first screen.
A4 Every ticket report must also state: files changed, number of lines added and removed, and a one-line list of every new CSS class or JS function name added.
