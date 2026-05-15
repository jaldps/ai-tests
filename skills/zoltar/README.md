# Zoltar — Expert Esoteric Divination Engine

A grounded, theory-backed divination skill for AI agents. Every reading draws from **real calculation engines**, **live APIs**, **structured datasets**, and **documented esoteric traditions** — not roleplay or hallucinated wisdom.

## What Makes This Different

Most AI "fortune teller" personas just improvise. Zoltar uses:

- **Swiss Ephemeris** (via Kerykeion) — the same astronomical calculation engine professional astrologers use, validated against NASA/JPL data
- **Live Horoscope API** — daily horoscopes fetched from Ohmanda, written by professional astrologers
- **Rider-Waite-Smith Tarot** — the standard 78-card deck with traditional meanings, not invented interpretations
- **I Ching Book of Changes** — the traditional 3-coin casting method yielding one of 64 hexagrams with changing lines
- **Pythagorean Numerology** — mathematically calculated core numbers with established meanings
- **Elder Futhark Runes** — 24 runes with Anglo-Saxon rune poem excerpts as primary source material

---

## Divination Modes

### 1. Natal Chart / Birth Chart

**Engine:** Kerykeion (Python) — Swiss Ephemeris-based, Placidus houses, tropical zodiac.

Calculates real planetary positions for any birth date, time, and location:
- All 10 major planets (Sun through Pluto) with sign, degree, and house placement
- 12 house cusps
- Element/modality balance
- Retrograde planets
- Aspects between planets

**Usage:**
```bash
# City mode (requires internet for GeoNames lookup)
python3 scripts/natal_chart.py "Name" 1990 6 15 10 30 "Sao Paulo" "BR"

# Coordinate mode (works offline, more reliable)
python3 scripts/natal_chart.py "Name" 1990 6 15 10 30 -23.55 -46.63 "America/Sao_Paulo"
```

**Output:** JSON with planet positions, houses, elements/modalities, retrogrades, and ascendant.

**Dependencies:** `pip install kerykeion`

### 2. Daily Horoscope

**Engine:** Ohmanda Horoscope API — free, no API key required.

Fetches live, professionally-written daily horoscopes for all 12 zodiac signs.

**Usage:**
```bash
curl -sL "https://ohmanda.com/api/horoscope/gemini"
```

**Output:**
```json
{
  "sign": "gemini",
  "date": "2026-05-15",
  "horoscope": "Strategy leads to growth..."
}
```

Valid signs: aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces

### 3. Tarot Reading

**Engine:** Structured 78-card dataset (`references/tarot_cards.json`) — Rider-Waite-Smith system.

Each card includes:
- Name, suit, number, elemental association
- Upright meaning (6+ keywords)
- Reversed meaning (6+ keywords)
- Brief visual description

**Supported spreads:**

| Spread | Cards | Positions |
|--------|-------|-----------|
| Single Card | 1 | Quick guidance |
| Three Card | 3 | Past / Present / Future |
| Celtic Cross | 10 | Present, Challenge, Foundation, Past, Outcome, Near Future, Self, Environment, Hopes/Fears, Final Outcome |

**Usage (Python):**
```python
import json, random
cards = json.load(open('references/tarot_cards.json'))
drawn = random.sample(cards, 3)  # 3-card spread
for card in drawn:
    reversed = random.choice([True, False])
    meaning = card['reversed'] if reversed else card['upright']
    print(f"{card['name']} ({'Reversed' if reversed else 'Upright'}): {meaning}")
```

**No dependencies** — pure JSON data.

### 4. I Ching Divination

**Engine:** Custom coin-casting script (`scripts/iching_reading.py`) — implements the traditional 3-coin method from the Book of Changes (Yijing).

The coin method:
1. Cast 3 coins (Heads=3, Tails=2) six times
2. Sum each cast: 6=old yin (changing), 7=young yang, 8=young yin, 9=old yang (changing)
3. Build hexagram from 6 lines (bottom to top)
4. Changing lines produce a second "relating" hexagram

**Usage:**
```bash
python3 scripts/iching_reading.py "Should I take the new job?"
```

**Output:**
```json
{
  "question": "Should I take the new job?",
  "hexagram_number": 57,
  "hexagram_name": "The Gentle Wind (Xun)",
  "lines": ["yin", "yin", "yin", "yang", "yang", "yang"],
  "changing_lines": [2, 3],
  "has_changing": true,
  "relating_hexagram": {
    "number": 53,
    "name": "Development (Jian)"
  },
  "changing_line_positions": [3, 4]
}
```

All 64 hexagram names included. Interpretation should reference the traditional Judgment, Image, and line texts.

**No external dependencies** — pure Python with `random`.

### 5. Numerology

**Engine:** Pure Python calculation (`scripts/numerology.py`) — Pythagorean system.

Calculates 6 core numbers:
- **Life Path** — from full birth date (the most important number)
- **Expression (Destiny)** — from full name (all letters)
- **Soul Urge (Heart's Desire)** — from vowels in name
- **Personality** — from consonants in name
- **Birthday** — from day of birth
- **Maturity** — Life Path + Expression

Plus 4 Pinnacle Cycles with age ranges.

**Usage:**
```bash
python3 scripts/numerology.py "Alex Morgan" 1990 6 15
```

**Output:** JSON with all core numbers and their traditional Pythagorean meanings.

**No dependencies** — pure Python.

### 6. Rune Casting

**Engine:** Structured 24-rune dataset (`references/runes_elder_futhark.json`) — Elder Futhark with Anglo-Saxon rune poem excerpts.

Each rune includes:
- Name, alternative name, meaning
- Aett (Freyja / Heimdall / Tyr)
- Upright meaning
- Reversed (merkstave) meaning — only where applicable
- Excerpt from the Anglo-Saxon Rune Poem (primary source)

8 runes are non-reversible (symmetric shape): Gebo, Hagalaz, Isa, Jera, Eihwaz, Sowilo, Ingwaz, Dagaz.

**Supported spreads:**

| Spread | Runes | Positions |
|--------|-------|-----------|
| Single Rune | 1 | Quick guidance |
| Norn Spread | 3 | Past (Urd) / Present (Verdandi) / Future (Skuld) |
| Five Rune Cross | 5 | Past, Present, Future, Challenge, Outcome |

**Usage (Python):**
```python
import json, random
runes = json.load(open('references/runes_elder_futhark.json'))
drawn = random.sample(runes, 3)
positions = ['Past (Urd)', 'Present (Verdandi)', 'Future (Skuld)']
for i, rune in enumerate(drawn):
    can_rev = rune['can_reverse']
    is_rev = can_rev and random.random() < 0.3  # ~30% merkstave chance
    meaning = rune['reversed'] if is_rev else rune['upright']
    print(f"{positions[i]}: {rune['name']} — {meaning}")
    print(f"  Rune poem: {rune['rune_poem']}")
```

**No dependencies** — pure JSON data.

---

## Installation

```bash
# Required for natal charts only
pip install kerykeion

# Everything else works with Python standard library only
```

## File Structure

```
skills/zoltar/
├── SKILL.md                          # Skill definition (triggers, modes, guidelines)
├── README.md                         # This documentation
├── scripts/
│   ├── natal_chart.py                # Swiss Ephemeris natal chart calculator
│   ├── iching_reading.py             # I Ching coin-casting divination
│   └── numerology.py                 # Pythagorean numerology calculator
└── references/
    ├── tarot_cards.json              # 78-card Rider-Waite-Smith dataset
    └── runes_elder_futhark.json      # 24 Elder Futhark rune dataset
```

## Design Principles

1. **Real data, not vibes.** Every reading cites specific planetary positions, card meanings, hexagram numbers, or rune poems.
2. **Honest about limitations.** Divination is framed as a contemplative/reflection tool, not prediction. No medical, financial, or legal advice.
3. **Respect the tradition.** Each system has its own internal logic — elements/modalities/dignities in astrology, elemental suits in tarot, yin/yang/trigrams in I Ching, aettir/rune poems in runes, letter-number correspondence in numerology.
4. **Synthesize, don't enumerate.** Readings tell a story connecting the dots, not just list data points.

## External Resources Used

| Resource | Type | URL | Free? |
|----------|------|-----|-------|
| Kerykeion | Python library | https://github.com/g-battaglia/kerykeion | Yes (MIT) |
| Swiss Ephemeris | Calculation engine | https://www.astro.com/swisseph/ | Yes (for non-commercial) |
| Ohmanda API | Daily horoscopes | https://ohmanda.com/api/horoscope/ | Yes (no key needed) |
| i-ching (npm) | Node.js library | https://github.com/strobus/i-ching | Yes (ISC) |
| PanchangaAPI | Vedic astrology | https://github.com/degen0root/panchanga_api | Yes (MCP server) |
| Celestine | TypeScript ephemeris | https://github.com/Anonyfox/celestine | Yes (MIT) |

## Limitations

- **GeoNames rate limiting:** Kerykeion uses GeoNames for city lookups. The default username is shared and rate-limited. Get a free account at https://www.geonames.org/login for reliable usage, or pass coordinates directly.
- **Ohmanda API:** Only returns daily horoscopes (no weekly/monthly).
- **Tarot system:** Rider-Waite-Smith only. Thoth and Marseille systems have different card meanings.
- **Numerology system:** Pythagorean only. Chaldean numerology uses different number assignments (1-8 instead of 1-9).
- **I Ching:** The script produces the hexagram data; interpretation of the Judgment/Image/line texts requires the LLM's knowledge of the Book of Changes.
- **No Vedic astrology:** This skill uses tropical zodiac. For sidereal/Vedic, consider PanchangaAPI (listed above).

## License

All original code and documentation: MIT License.
Tarot card meanings and rune poems are from public domain/traditional sources.
Kerykeion and Swiss Ephemeris have their own licenses (see links above).
