# OpenPak catalog

`catalog.json` introduces titles and features to the website and the app: name, console,
category, backend, and the status they start with. The website fetches this file from `main`
every ten minutes and adds anything new.

**Status is owned by the website's database, not by this file.** Once a title exists there,
its status and notes change from the titles page (an admin picks the status on the row, or
promotes a requestable title from the Request-a-game dialog) and the site and the app read
the row at once; the catalog's status for an existing title is ignored on refresh. Edit here to
add a title or fix its category; run `python3 gen.py` to regenerate the Markdown views; commit,
push.

Status words: `live` works end to end on hardware, `beta` is deployed but not
console-verified, `alpha` is partial, `scaffold` is code waiting on a fact, `requestable` is
listed for votes only.
