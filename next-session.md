# Next session — catalog

Updated 2026-09-15.

The catalog repository: `catalog.json` introduces titles and features (name, console,
category, backend, starting status) to the website, which fetches it from `main` every ten
minutes and adds anything new. Status is owned by the website's database once a title exists
there; `gen.py` regenerates `catalog.md` so the two never drift. Three commits; last sync
2026-09-12.

## Where things stand

- `gen.py` writes `catalog.md` (summary, A titles, B network features, C console-network
  matrix) from `catalog.json`; `titles-by-console.md` holds the per-console research and
  sources.
- 2026-09-12 sync (8d0f116): nimbus built, `openpak-v1` release, 3DS network notes updated —
  `catalog.json` regenerated wholesale (360 rows), the per-title status rows reconciled then.
- `CHANGELOG.md` is a generated summary of git history (2026-09-15).

## Next steps

- After any JSON edit: `python3 gen.py`, commit, push to `main` — the ten-minute fetch picks
  it up.
- Reconcile rows again after the next title bring-ups; edit status here only for titles not
  yet in the website DB (existing rows change on the titles page).
- Honesty rule stands (gen.py header): cross-checked against the repos, not a wish list.

## Pointers

- `README.md` — the contract with the website (status words, edit flow).
- `../../emulators/prds/README.md` and `../../prds/README.md` — cross-system PRDs; none live
  here (`prds/` in this repo says so).
