# Annual Planning Forum 2026 invitation

Public invitation website for the Annual Planning Forum 2026 for Planning Officers.
Two people work on this repository, each with their own Claude. Neither Claude can
see the other's conversations, so anything the next person needs to know goes in
this file or in the pull request description.

Live site: https://chimileo.github.io/apf-2026-invitation/

## Confirmed facts (do not change without the organisers)

- Event: Annual Planning Forum 2026, for Planning Officers.
- Dates: Monday 7 to Friday 11 December 2026. Registration from 08:30 on the 7th (Bhutan time, UTC+6).
- Venue: Tashi Namgay Grand, Phuentsholing, Chhukha Dzongkhag.
- Host: Office of Cabinet Affairs and Strategic Coordination (OCASC).
- Dzongkha greeting: སྐུ་གཟུགས་བཟང་པོ་ལགས། (spelling given by OCASC). Farewell: བཀྲ་ཤིས་བདེ་ལེགས།
  Do not "correct" Dzongkha text; ask a Dzongkha speaker first.
- The agenda in `AGENDA` is a made-up placeholder, shown on purpose until the official
  programme arrives. Keep the "draft programme" wording until it is replaced.

## Layout

- `src/invitation.html` is the master page: all HTML, CSS and JavaScript in one file.
  Edit this, never `_site/`.
  - Event details live in the `EVENT` object near the top of the `<script>`.
  - The programme is the `AGENDA` array right after it: `[time, title, detail, type]`,
    where type is one of Arrival, Ceremony, Plenary, Working session, Field visit, Break, Social.
- `src/head.html` is the public `<head>`: page title, link-preview (Open Graph) tags and
  the robots `noindex` tag. If the site moves to a new address, update `og:url` and `og:image` here.
- `public/` is copied to the site as is: `og.jpg` (link-preview picture), `photos.json` and `photos/`.
- `build.py` joins head + page into `_site/index.html` and checks `photos.json`. It fails
  the build on mistakes, so run it before opening a pull request.
- `.github/workflows/pages.yml` runs the build on every pull request and deploys `main`
  to GitHub Pages about a minute after a merge.

## Preview locally

```
python build.py
python -m http.server 8000 --directory _site
```

Then open http://localhost:8000. Check the door entrance, every section, and a phone
width (375 px) before asking for review.

## How we work together

- Never push straight to `main`. Make a branch, push it, open a pull request, and let the
  other person review it. `main` is protected: it needs one approval and a passing build.
- Keep pull requests small and say in the description what changed and why.
- Pull `main` before starting work so you are not editing an old copy.
- Commit with your GitHub noreply email (Settings > Emails), never a personal or work
  email: this repository and its whole history are public.

## Rules for the page

- Everything committed here is public and stays in the git history even after deletion.
  No personal details (emails, phone numbers, ID numbers), no internal documents.
- Forum photos of people go up only with OCASC approval. To add one, put the JPG in
  `public/photos/` and add `{"src": "photos/name.jpg", "caption": "..."}` to
  `public/photos.json`. Resize to about 1800 px on the long side first.
- Keep the `noindex` robots tag in `src/head.html` (the organisers asked for it; `build.py` enforces it).
- The same `src/invitation.html` is also published to a private claude.ai artifact, so:
  - no `<!doctype>`, `<html>`, `<head>` or `<body>` tags in it (`build.py` enforces this);
  - no new external scripts, stylesheets, images or fetches to other sites. Only Google Fonts
    is loaded from outside. Draw graphics inline (SVG/canvas) or put files in `public/`;
  - no `alert()`, `confirm()` or `prompt()`; build confirmations into the page.
- The page runs in two modes. When `window.claude` exists (claude.ai), the selfie wall and
  Forum photos use claude.ai storage. On the public site it does not exist: selfies are
  framed and saved or shared on the guest's own device, and Forum photos come from
  `photos.json`. Test that changes work in public mode and do not break the claude.ai code paths.
- Keep it working at 375 px wide with no sideways scrolling, in light and dark themes, and
  with `prefers-reduced-motion`.
- Colours are CSS tokens on `:root` with dark-mode overrides; use the tokens, not literal colours,
  in the site sections. The entrance scene uses fixed colours on purpose.

## claude.ai copy (owner only)

The owner keeps a private copy at https://claude.ai/artifact/RLp2wBCrgVSXzeVFJ1MsM4 with a
signed-in selfie wall. Only the owner's Claude can update it: publish `src/invitation.html`
to that URL after a change is merged. A collaborator does not need to do anything for it.

## Known open items

- Move to an official address (a cabinet.gov.bt subdomain via CNAME, or the government web
  server). Then update `og:url` / `og:image` in `src/head.html`.
- Load the fonts from `public/fonts/` instead of Google Fonts.
- Add fallback font sizes for browsers without container query units (`cqw`, pre-2022 phones).
- GitHub Pages cannot send security headers; a government server should add CSP,
  `frame-ancestors 'none'`, `Referrer-Policy`, `X-Content-Type-Options` and HSTS.
