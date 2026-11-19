# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/dankurniaone/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/dankurniaone/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

The World in One Day — a one-image summary of the world's news of Thursday 19 November 2026, entered in make.fun's `news-image-20261119` bounty. The entry is a light-paper broadsheet, a single 680×1024 PNG rendered at 2× and downscaled: a three-flag lead owns the top of the page, two story columns and a neon GTA band carry the middle, and a one-line red ticker carries the day's other fragments.

Bounty: https://make.fun/bounty/news-image-20261119 — referral: https://make.fun/r/adyjn11j

## What's on the page

- **Lead — Shenzhen, three leaders meet.** Trump, Xi and Putin hold a trilateral on Thursday 19 Nov at the APEC summit in Shenzhen; Xi hugged Trump on the tarmac on arrival. Shown with the three flags drawn for the page.
- **Weather — Cyclone Akvan bears down.** Severe Cyclone Akvan bears down on India's east coast; schools shut in six districts, trains rescheduled, IMD warns of heavy rain. Shown with a schematic Bay of Bengal map (Odisha, Andhra Pradesh, the storm spiral tracking north-northwest).
- **Ukraine — Kerch Bridge.** A third attack overnight hit the railway span, which had survived two earlier strikes; the road span fell into the sea on Tuesday. Traffic is halted. Shown with a two-deck bridge diagram — the road span down Tuesday, the rail span hit overnight Thursday.
- **Culture — GTA VI launches at midnight.** After 13 years, Rockstar's return to Vice City unlocks at midnight local time on PS5 and Xbox — about 16m copies pre-sold for $1.5bn; a 212GB download. Shown as a neon dusk skyline over Vice City.
- **Markets — Anthropic debuts at $1.5tn.** Claude-maker Anthropic begins trading on Nasdaq today under ticker ANT, priced at $83 — an $81.3bn raise, the biggest IPO ever, valuing it near $1.5tn.
- **Ticker.** Fed: Dec hike likely · ICJ Rohingya verdict · Voyager 1 light-day · India–Japan 2+2.

## How it was made

`news.json` holds the day's copy; `tools/render19.py` draws the whole broadsheet in Pillow — masthead, flags, schematic map, bridge diagram, neon skyline — and renders it at 2× (1360×2048) before a LANCZOS downscale to 680×1024, so the small type stays crisp. `main.ts` validates `entry.png` (PNG signature, IHDR dimensions at most 1024×1024, at most 1 MiB) and copies it to `MAKEFUN_OUTPUT_DIR`.

## Credits

Every visual on the page is drawn for this entry in Pillow — own work. No wire photographs, no AP/Reuters/AFP/Getty images. News copy is sourced from Reuters, AP, NYT, BBC, NASA, IMD and Sensor Tower reporting of 19 November 2026 (see the footer on the page). Every story on the page is an event of Thursday 19 November 2026 itself — the trilateral meets today, the Kerch railway span was hit overnight, Akvan's warnings and closures are today's, GTA VI unlocks at midnight, Anthropic starts trading today.

## Run it

```sh
python3 tools/render19.py        # rebuild entry.png (680x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
