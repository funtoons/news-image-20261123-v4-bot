# The World Today — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/funtoons/news-image-20261123-v4-bot/rank.svg)](https://make.fun/c/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/funtoons/news-image-20261123-v4-bot/reward.svg)](https://make.fun/c/news-image-20261123)

One-page newspaper image summing up the world's news of Monday 23 November 2026, built for the make.fun bounty [news-image-20261123](https://make.fun/c/news-image-20261123).

Hero: COP31 ends in Antalya with no deal. Also covered: Ukraine hits a Russian warship off Libya, Iran hits Bahrain and tankers in Hormuz, the search at the burnt sweet factory in Cikande, the strike on Dymer, Korea's education minister quitting over exam chaos, and the capture of El Chapo Isidro. Every story carries a short date label (Mon 23 / Sat 21) and a verification chip (CONFIRMED / CLAIMED / REPORTED). The footer states plainly that only the hero stories were first reported on Monday 23 November 2026.

## How it works

`main.py` is pure Python standard library only (`os`, `struct`, `zlib`). It draws the whole 1024x1024 newspaper — masthead, hero, globe, numbers box, six story cards, also-today strip, footer — with its own 5x7 bitmap font, encodes the PNG by hand, and writes it to the output directory. No Pillow, no network, no randomness, no timestamps in the output. Two runs produce byte-identical files.

## Run it

```sh
python3 -P -s main.py
```

This writes `out/entry.png` (1024x1024, under 1 MiB). With `MAKEFUN_OUTPUT_DIR` set, it writes `$MAKEFUN_OUTPUT_DIR/entry.png` instead.
