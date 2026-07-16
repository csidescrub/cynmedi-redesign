# CYN Website — Conventions

## Typography rule: English inside Thai copy = Poppins

Any font stack that styles Thai copy (headings, paragraphs, buttons, labels,
forms) must list **'Poppins' immediately before the Thai font**, so Latin
words embedded in Thai sentences render Poppins while Thai glyphs fall through
to the Thai font:

```css
/* body copy */        font-family:'Poppins','Kanit','Inter',system-ui,sans-serif
/* display headings */ font-family:'NumSans','Poppins','Kanit',sans-serif
/* LP (Anuphan pages) */ font-family:'Poppins','Anuphan',sans-serif
```

Every page must import Poppins in its Google Fonts URL:
`family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500`

**Deliberate exceptions — do NOT add Poppins in front of these:**

- **English-only serif display accents** (Cormorant Garamond): work-page `<h1>`
  client-name lockups (inline style), `.italic-serif`, `.en-serif`, `.sc-name`,
  `.cvx-name`, `.cvx-mark`, serif stat numerals (`.hero-stat-num`,
  `.result-num`, `.serif-num`), `about.html` display headings (English brand
  page), `index.html` hero H1 (English), LP `--serif-en` elements.
  If you ever put Thai+English mixed copy into one of these, restyle that
  element with the Poppins-first stack instead.
- **Numerals**: `NumSans` (digit-only local-Inter alias) stays first in display
  stacks; `.num`/`.usfx` (Inter, tabular figures) stay Inter.
- **Coded dashboard/phone mockup UI** (`dash-*`, `p3d-*`, `lead-*`,
  `phone3d-*`, `order-amt` on aesthetic-clinic/v2): mimics an app UI — Inter
  stays.

Thai must never fall through to a serif or loop font: every stack that can
receive Thai text keeps 'Kanit' (or 'Anuphan' on the LP) before any generic
fallback.

## Other conventions

- Each page is self-contained (own `<head>` fonts + inline styles); the shared
  file is `assets/tailwind.css`. Changing a convention means sweeping all 30
  HTML files — `work/*.html` share one identical template (same selectors,
  same line numbers).
- Accent color by background: light bg → navy `#2D4DB1` (`text-cobalt`);
  dark bg → light blue `#94A6DB` (`text-royal-300`).
- Deploy: `git push` + `npx wrangler pages deploy . --project-name cyn-2026`.
  Live at cynmedi.com (Cloudflare Pages, propagation can lag ~1 min per edge).
