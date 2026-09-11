# OpenPak catalog

`catalog.json` is the honest status of every title and network feature OpenPak knows about:
`live` works end to end on hardware, `beta` is deployed but not console-verified, `scaffold`
is code waiting on a fact, `requestable` is listed for votes only. Edit the JSON, run
`python3 gen.py` to regenerate the Markdown views, commit, push.

The website fetches this file from `main` on a timer and reseeds its title list, and the app
reads the website's API, so a status change here reaches both without a release. The website
also embeds a copy as a fallback for when GitHub is unreachable at start-up.
