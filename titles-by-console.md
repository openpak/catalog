# Titles by console — the ten non-Switch networks

Survey date: 2026-09-10. Purpose: give the website and the app a real games list for every console in
the platform matrix, not just Switch, so a visitor can find their game and vote for it. This document
is the *why* behind those rows; `catalog.json` is the source of truth and `catalog.md` is generated
from it. Network-level prior art, licences and reuse verdicts live in
[`../../research-third-party-networks.md`](../../research-third-party-networks.md) — that survey is
about servers, this one is about games.

**282 titles added**, across Wii (32), DS (36), Wii U (23), 3DS (30), Xbox (28), Xbox 360 (30),
PS2 (30), PS3 (31), PSP (22) and Vita (20). Every one of them is `requestable`: a candidate with
nothing built. None of these consoles has a network past `alpha`, so any other status would be a lie.

## Method

- **What counts as a title.** Online multiplayer or online co-op. A few entries have no online play
  at all (Pikmin 3, Ninja Gaiden Black, Picross DS, Super Mario 3D World) — they are in because
  leaderboards, content delivery or sharing *is* their whole online surface, and their notes say so.
  A vote for one of them should land somewhere honest rather than nowhere.
- **Not exhaustive, deliberately.** The full populations are much larger: ~219 retail DS titles and
  ~124 retail Wii titles used Nintendo WFC, ~399 PS2 games had online modes, 381 Xbox games used
  Xbox Live 1.0, and Xenia's netplay fork claims 500+ 360 titles working in some capacity. Listing
  all of them would bury the signal in sports-franchise year editions. Each console gets the titles
  that are either famous, or technically interesting, or already proven by a revival project — a list
  a visitor can scan. The long tail is a vote away: the request flow is how it gets in.
- **Backend over console.** The `backend` column is the network a title actually talked to, which is
  frequently *not* the console's own service. That distinction is the single most useful thing in
  this research and is spelled out below.

## Per-console summary

| Console | Official service | What we would have to serve | Open prior art (licence) | First target |
|---|---|---|---|---|
| Wii | WFC dead since 2014-05-20 (GameSpy shutdown) | GameSpy-style auth, matchmaking, NAT negotiation, friend codes | WiiLink `wfc-server` (Go, open); Wiimmfi is closed | Wii Chess, then Mario Kart Wii |
| DS | WFC dead since 2014-05-20 | Same stack as Wii, plus Pokémon GTS/Dream World persistence | same `wfc-server` | Mario Kart DS (already full in wfc-server) |
| Wii U | Nintendo Network dead since 2024-04-08 | NEX (PRUDP/RMC), DataStore, friends, Miiverse | Pretendo (AGPL, depend+fork) — `nn-account`/`nn-friends` already ours | Pikmin 3 (rankings only, no session layer) |
| 3DS | Nintendo Network dead since 2024-04-08 | NEX + NASC, DataStore, Pokémon Bank | Pretendo (AGPL) | Steel Diver: Sub Wars, Tri Force Heroes |
| Xbox | Xbox Live 1.0 dead since 2010-04-15 | Kerberos auth, matchmaking, leaderboards, clans, UGC | Insignia is **closed** (199/381 titles, 34k users) — it proves feasibility, gives us no code | Halo 2 is the prize; something small is the first build |
| Xbox 360 | **still live** (marketplace closed 2024) | Xbox Live REST title services, per-title servers | Xenia-WebServices (MIT, TypeScript) is the only open one | emulator-first, via a Go reimpl of that REST API |
| PS2 | dead in waves, most by 2016-03-31 | Medius lobbies, or GameSpy, depending on the title | Horizon (MIT), MultiServer3 (GPL-3.0), OpenSpy | SOCOM II (Medius) or a GameSpy title via OpenSpy |
| PS3 | **still live**; stores close Aug 2026 → Jul 2027 | PSN rooms/scores/TUS; plus per-title servers | RPCN (AGPL, Rust) — be wire-compatible; ProjectLighthouse (AGPL) for LBP | Demon's Souls (RPCN-proven) |
| PSP | infrastructure dead; ad-hoc never needed a server | an ad-hoc relay, and Medius for the infrastructure titles | aemu / Pro Online (GPL), PPSSPP's relay | the ad-hoc relay — it unlocks dozens of titles at once |
| Vita | **still live**; store closes Jul 2027 | PSN, same shapes as PS3, plus cross-play with it | ProjectLighthouse (Vita LBP); Phony Network announced, no code | LittleBigPlanet PS Vita, by federating |

## Five findings that change the plan

**1. The publisher-backend wall is bigger than the console networks.** A working console network is
not enough for a large slice of these games, because they never used it:

| Backend | Consoles it spans in this list |
|---|---|
| Demonware (Activision) | Wii, DS*, Wii U, Xbox 360, PS3, Vita |
| EA Nucleus | Wii, Wii U, Xbox, Xbox 360, PS2, PS3 |
| Capcom servers | Wii, 3DS, Xbox, Xbox 360, PS2, PS3, Vita |
| Rockstar Social Club | Xbox 360, PS3 |
| Konami / Square Enix / Sega own servers | Wii, Wii U, PS2, PS3, PSP |
| 4J Studios (Minecraft console editions) | Wii U, Xbox 360, PS3, Vita |

\* the DS build of Black Ops went through WFC; the Wii build did not. Same name, same year, different
network — which is exactly why the catalogue now keys a title by (name, console).

Insignia states plainly that it cannot serve EA titles because EA ran its own servers. We would hit
the identical wall. The flip side is leverage: **one Demonware server would light up six consoles**,
which is better value than any single title. Worth its own PRD before any per-title work.

**2. Ship the cross-play pairs together or not at all.** Final Fantasy Crystal Chronicles: Echoes of
Time cross-plays Wii↔DS. Monster Hunter 3 Ultimate cross-plays Wii U↔3DS. LittleBigPlanet,
PlayStation All-Stars, Minecraft and Dragon's Crown cross-play PS3↔Vita. Pokémon Battle Revolution
(Wii) is fed teams from DS Diamond/Pearl. Half a pair is a bug report waiting to happen.

**3. The titles with the strongest case are the ones that are *nothing* without a server.** Devil's
Third, Chromehounds, Steel Battalion: Line of Contact, Warhawk, Starhawk, Hardware: Online Arena,
Front Mission Online, Metal Gear Online, Monster Hunter Frontier G, Twisted Metal: Black Online.
These have no single-player worth the disc; a replacement network is the only way they exist at all.
That is the same argument that put Super Mario Bros. 35 on the Switch list.

**4. Several of these are storage services wearing a game's clothes.** Pokémon GTS and Pokémon Bank,
Super Mario Maker (both versions), LittleBigPlanet, ModNation Racers, Trials Evolution, Far Cry
Instincts' map sharing, Advance Wars: Days of Ruin's map trading, Forza 4's design marketplace. They
need durable per-user storage with quotas and moderation, not matchmaking — the DataStore shape we
are already defining with Super Mario Maker 2. Every console has at least one, and they are the rows
most likely to be under-estimated.

**5. Two of these networks are not dead, and the catalogue should not pretend otherwise.** Xbox Live
still serves 360 consoles, and PSN still serves PS3 and Vita; Sony is closing the PS3/Vita *stores*
in waves from August 2026 to July 2027, which is the warning shot, not the shutdown. For those three
consoles our value today is (a) emulator players, who cannot reach the official service at all, and
(b) insurance for the day it goes. For Wii, DS, Wii U, 3DS, Xbox and PS2 the service is already gone
and the work is rescue. That ordering is a better prioritisation input than vote counts alone.

## Per-console notes

### Wii and DS — one stack, two consoles
Both died the same day for the same reason: GameSpy's shutdown took Nintendo WFC with it. One Go
server covers both, and WiiLink's `wfc-server` is already that server, open and live. Its honest
current coverage is small (full: Wii Chess, Puyo Puyo Tsu, Tetris Party Deluxe, Mario Kart DS, Open
Season; partial: Mario Kart Wii, Brawl, City Folk, Dr. Mario, Fortune Street, Puyo Puyo 7), while
closed-source Wiimmfi reports 380 games fully working. So the protocol is a solved problem and the
gap is implementation, not research. Two traps: the Pokémon titles are a persistence product (GTS,
Dream World, Global Link), not a lobby; and Monster Hunter Tri never used WFC at all — it used
Capcom's servers, which the open MH3SP project reimplements separately.

### Wii U and 3DS — already our roadmap
These are NEX, the same protocol family our Switch servers speak, and `nn-account` plus `nn-friends`
are already being ported from Pretendo. Pretendo's own per-title progress list names the titles with
real protocol work behind them — Mario Kart 7 and 8, Splatoon, Super Mario Maker on both consoles,
Super Smash Bros. 4 (DataStore + Ranking), Pokkén, Kid Icarus: Uprising, Steel Diver: Sub Wars,
IRONFALL, Tri Force Heroes, Team Kirby Clash Deluxe, Pokémon Rumble World, Pokémon X/Y and Pokémon
Bank DataStores, Monster Hunter XX matchmaking, Pikmin 3, Yo-kai Watch 2 and Miiverse. Those are the
cheapest titles in this whole document, because the protocol work exists under a licence we can use.
Pikmin 3 is the single cheapest: rankings and content delivery, no session layer.

### Xbox — feasibility proven, code unavailable
Insignia has restored 199 of the 381 Xbox Live 1.0 titles for 34,000 users, including matchmaking,
leaderboards, friends, invites, clans, UGC and voice. That is the strongest possible evidence that a
clean-room Xbox Live 1.0 is achievable, and it is also a wall: Insignia's server is closed, so the
only public material is the archived XboxLive.Server's Kerberos AS-REQ/REP notes. Xbox is therefore
our most from-scratch console. Note the interesting precedent that Insignia serves Phantasy Star
Online Episode I & II, a game whose backend was Sega's, not Microsoft's.

### Xbox 360 — emulator-first, and honest about hardware
Xenia-WebServices (MIT) is the only open Xbox Live-shaped backend in existence, and the netplay fork
around it claims 500+ titles working in some capacity. Our plan stands: a Go reimplementation of that
REST API, emulator-first. Real-hardware stealth servers stay out of scope. The titles here are
weighted toward those that are already netplay-listed (CoD 4, MW2, World at War, Blur, Armored Core
4, Chromehounds) plus the ones people will actually ask for (Halo 3, Reach, Gears, Minecraft).

### PS2 — three different networks wearing one label
"PS2 online" is really Medius (Sony's own lobby middleware: SOCOM, Jak X, Ratchet, Killzone,
Syphon Filter, ATV, Warhawk later on PS3), GameSpy (Call of Duty, Midnight Club, Mortal Kombat, Star
Wars: Battlefront), and publishers' own stacks (Capcom's Outbreak and Monster Hunter, Konami's MGS3,
SOE's EverQuest, Square's FFXI and Front Mission Online). Each has different prior art — Horizon and
MultiServer3 for Medius, OpenSpy for GameSpy, and a named fan project for most of the publisher ones
(SaveMGO, Outbreak Server Resurrection, MH Oldschool, SWBFspy, TMBOSVR, Sandstorm). For several of
these titles the right OpenPak answer is "point at the existing server", exactly as we decided for
Among Us.

### PS3 and Vita — federate, do not rebuild
RPCN (AGPL, Rust) already serves PSN-shaped rooms, scores and TUS to stock RPCS3, and
ProjectLighthouse (AGPL) already serves every LittleBigPlanet on PS3, Vita and RPCS3. The plan of
record — be wire-compatible with RPCN rather than invent a protocol, and federate Lighthouse rather
than clone it — survives this survey intact. What RPCN does not cover is the titles that needed a
dedicated server (Warhawk, Starhawk, Metal Gear Online, Armored Core V) or a publisher's backend
(Demonware, EA, Capcom, Rockstar, Polyphony). Hardware still waits on Phony Network or our own RE.

### PSP — the relay is the product
Most PSP multiplayer is ad-hoc wireless, which never had a server: the whole job is tunnelling
ad-hoc over the internet, which aemu/Pro Online (GPL) and PPSSPP's relay already do, and which is
latency-forgiving for exactly the titles people want (Monster Hunter, Ridge Racer, GTA, CoD: Roads
to Victory). One relay unlocks every ad-hoc title at once, which makes it the best effort-to-titles
ratio in this entire document. The smaller infrastructure set is Medius (the SOCOM Fireteam Bravos,
Killzone: Liberation, Resistance: Retribution, Wipeout Pulse) or a publisher's own (Phantasy Star
Portable 2, already revived by the PSP2i project).

## What changed in the repos

- `docs/catalog/catalog.json` — 282 new `requestable` title rows; `gen.py` no longer claims the
  games list is Switch-only and now prints a per-console breakdown.
- `website/internal/store/catalog.json` — refreshed copy (it is embedded in the binary).
- `requests` is now unique per **(kind, name, console)**, not (kind, name). Fourteen names repeat
  across consoles — Call of Duty: Black Ops appears three times on three different networks — and
  each deserves its own row and its own votes. Migration `0004_requests_per_console`; migrations are
  now applied in sorted order, which the comment always claimed and the code did not do.
- Console logos for all ten consoles, in `website/web/static/consoles/` and `app/assets/consoles/`,
  wired into `consoleSlug` (Go) and `consoleAsset` (Dart). The titles page and the app's Titles tab
  already filtered by console; they were just drawing a generic gamepad for everything but Switch.

## Sources

- [Insignia — supported games](https://insignia.live/games) (199 titles, read 2026-09-10) and
  [Insignia (Wikipedia)](https://en.wikipedia.org/wiki/Insignia_(Xbox)) for the 34k users / 381 total
  and the EA-servers limitation.
- [List of WiiLink WFC supported games](https://wiilink.wiki.gg/wiki/List_of_WiiLink_WFC_supported_games)
  — the open server's real coverage; [Wiimmfi](https://wiimmfi.de/) for the 380-full/22-partial/671-testing
  counts.
- [List of Nintendo DS Wi-Fi Connection games](https://en.wikipedia.org/wiki/List_of_Nintendo_DS_Wi-Fi_Connection_games)
  and [List of Wii Wi-Fi Connection games](https://en.wikipedia.org/wiki/List_of_Wii_Wi-Fi_Connection_games)
  — the full WFC populations.
- [Pretendo Network progress](https://pretendo.network/progress) — the per-title Wii U/3DS protocol work.
- [Xenia-WebServices](https://github.com/AdrianCassar/Xenia-WebServices) (MIT) and
  [Xenia netplay guide](https://xeniamanager.wiki/xenia-netplay/) — the 500+ claim and its caveats.
- [RPCN compatibility list](https://wiki.rpcs3.net/index.php?title=RPCN_Compatibility_List) and
  [RPCN browser](https://rpcs3.net/rpcn) — PS3 titles that already work.
- [List of PlayStation 2 online games](https://en.wikipedia.org/wiki/List_of_PlayStation_2_online_games)
  — the ~399 titles, their shutdown dates and the fan servers keeping some alive.
- [MH3SP](https://github.com/sepalani/MH3SP) — Monster Hunter Tri's non-WFC servers, reimplemented.
- [PPSSPP ad-hoc multiplayer](https://www.ppsspp.org/docs/multiplayer/how-to-play/) and
  [PPSSPP ad-hoc compatibility list](https://github.com/AkiraJkr/PPSSPP-Adhoc-Compatibility-List).
- [PlayStation Store on PS3 and PS Vita is closing](https://blog.playstation.com/2026/07/01/an-update-on-playstation-store-for-ps3-and-ps-vita/)
  — August 2026 through July 2027, by region.
