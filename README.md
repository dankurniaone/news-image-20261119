# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/dankurniaone/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/dankurniaone/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

The World in One Day — a one-image summary of the world's news of Thursday 19 November 2026, entered in make.fun's `news-image-20261119` bounty. The entry is a light-paper broadsheet, a single 680×1024 PNG rendered at 2× and downscaled: a three-flag lead owns the top of the page, two story columns and a neon GTA band carry the middle, and a one-line red ticker carries the day's other fragments.

Bounty: https://make.fun/bounty/news-image-20261119 — referral: https://make.fun/r/adyjn11j

## What's on the page

- **Lead — Shenzhen, three leaders meet.** Trump, Xi and Putin hold a trilateral on Thursday 19 Nov at the APEC summit in Shenzhen; Xi hugged Trump on the tarmac on arrival. Shown with the three flags drawn for the page.
- **The Gulf — war widens.** Houthi cruise missiles aimed at Riyadh were shot down by Saudi defences; Reuters, Thu 19 Nov: the escalation goes on as diplomacy to end the nine-month war stays deadlocked. Shown with a schematic Gulf map (Kuwait, Bahrain, Qeshm, Riyadh, Strait of Hormuz).
- **Ukraine — Kerch Bridge.** A third attack in a week: traffic suspended after a new attack, Crimea's Russian-installed governor said on Telegram on Thursday; the road span fell into the sea earlier in the week. Shown with a bridge diagram — the deck with its road span down.
- **Culture — GTA VI launches at midnight.** After 13 years, Rockstar's return to Vice City unlocks at midnight local time on PS5 and Xbox — about 16m copies pre-sold for $1.5bn; a 212GB download. Shown as a neon dusk skyline over Vice City.
- **Washington — Jeffries nominated, 251–11.** House Democrats chose Hakeem Jeffries for Speaker in a closed-door vote on Wednesday; if the full House elects him on 3 Jan, he is the first Black Speaker.
- **Ticker.** EU €45bn Ukraine loan · Gaza ground op · Eisenkot tapped · Van Gogh $190.4m record sale.

## How it was made

`news.json` holds the day's copy; `tools/render19.py` draws the whole broadsheet in Pillow — masthead, flags, schematic map, bridge diagram, neon skyline — and renders it at 2× (1360×2048) before a LANCZOS downscale to 680×1024, so the small type stays crisp. `main.ts` validates `entry.png` (PNG signature, IHDR dimensions at most 1024×1024, at most 1 MiB) and copies it to `MAKEFUN_OUTPUT_DIR`.

## Credits

Every visual on the page is drawn for this entry in Pillow — own work. No wire photographs, no AP/Reuters/AFP/Getty images. News copy is sourced from Reuters, AP, CNN, NYT, BBC, Sensor Tower and NASA reporting of 19 November 2026 (see the footer on the page).

## Run it

```sh
python3 tools/render19.py        # rebuild entry.png (680x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
