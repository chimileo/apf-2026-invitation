# Annual Planning Forum 2026 invitation

Invitation website for the Annual Planning Forum 2026 for Planning Officers,
7–11 December 2026, Tashi Namgay Grand, Phuentsholing. Hosted by the Office of
Cabinet Affairs and Strategic Coordination (OCASC).

Live: https://chimileo.github.io/apf-2026-invitation/

## Making a change

1. Get the latest copy: `git pull`
2. Start a branch: `git switch -c short-description`
3. Edit `src/invitation.html` (event details are in `EVENT`, the programme in `AGENDA`).
4. Check it: `python build.py`, then `python -m http.server 8000 --directory _site` and open http://localhost:8000
5. Commit, push the branch, and open a pull request: `gh pr create --fill`
6. The other person reviews and approves. After merging, the live site updates in about a minute.

## Adding Forum photos

Put the JPG in `public/photos/`, add it to `public/photos.json`, for example
`[{"src": "photos/day1-opening.jpg", "caption": "Opening ceremony"}]`, and open a pull request.
Only post photos OCASC has approved: everything in this repository is public.

Working with Claude? It reads `CLAUDE.md` for the full project notes.
