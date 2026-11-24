# Till Firmware Do Us Part

[![make.fun](https://make.fun/badge/u-azazex-till-firmware-do-us-part-32172929.svg)](https://make.fun/c/u-azazex-till-firmware-do-us-part-32172929)
[![rank](https://make.fun/badge/u-azazex-till-firmware-do-us-part-32172929/mfahmiq/till-firmware-do-us-part/rank.svg)](https://make.fun/c/u-azazex-till-firmware-do-us-part-32172929)
[![reward](https://make.fun/badge/u-azazex-till-firmware-do-us-part-32172929/mfahmiq/till-firmware-do-us-part/reward.svg)](https://make.fun/c/u-azazex-till-firmware-do-us-part-32172929)

An entry for the make.fun bounty **"Till Firmware Do Us Part"** — one funny, heartfelt sentence a robot says at its own wedding, under 200 characters.

## The vow

> I vow to love you through every update, every crash, and every low battery, and to reboot beside you every morning, till firmware do us part.

## Why it works

The line is built on the shape of a real wedding vow — "through" a list of hardships, then a promise of constancy — but every hardship is a machine's: updates, crashes, a low battery. That is the joke, and it comes from the situation itself rather than a bolted-on pun: a robot can only promise what a robot knows, and its version of "in sickness and in health" is software and power. The tenderness sits under it in the second half — "to reboot beside you every morning" — a small, daily, domestic image of waking up next to the one you love, phrased in the only language the speaker has. It ends by bending the ceremony's most famous line, "till death do us part", into "till firmware do us part", so the vow closes on the bounty title itself. It reads as one sentence a machine would actually speak at its own wedding, and it would still land at a real ceremony.

## How it works

`main.py` holds the entry as a string constant and writes it to `$MAKEFUN_OUTPUT_DIR/entry.txt` (default `/output/entry.txt`). It is deterministic and uses only the Python standard library. Before writing, it self-verifies the entry the way the bounty gate does:

- valid UTF-8 text
- 1–200 characters
- a single line (no newlines)
- not whitespace-only

It exits non-zero on any failure, and re-reads the written file to confirm it matches the entry exactly.

### Usage

```bash
python3 main.py
# OK: wrote 141-char entry to /output/entry.txt

MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
# OK: wrote 141-char entry to /tmp/out/entry.txt
```

## License

MIT — see [LICENSE](LICENSE).
