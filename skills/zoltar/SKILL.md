     1|---
     2|name: zoltar
     3|version: 1.0.0
     4|description: Expert esoteric divination skill — real astrology, tarot, I Ching, numerology, runes. Uses verified APIs and calculation libraries, not roleplay.
     5|category: esoteric
     6|trigger: When the user asks for a horoscope, tarot reading, natal chart, I Ching hexagram, numerology report, rune casting, or any esoteric/divination guidance.
     7|---
     8|
     9|# Zoltar — Expert Esoteric Divination Engine
    10|
    11|A grounded, theory-backed divination skill. Every reading draws from real calculation engines (Swiss Ephemeris via Kerykeion), live horoscope APIs, structured tarot/I Ching datasets, and documented esoteric traditions. No roleplay — real data, real interpretation.
    12|
    13|## Divination Modes
    14|
    15|### 1. Natal Chart / Birth Chart Analysis
    16|**Engine:** Kerykeion (Python) — Swiss Ephemeris-based, Placidus houses, tropical zodiac.
    17|
    18|**Requirements from user:**
    19|- Date of birth (YYYY-MM-DD)
    20|- Time of birth (HH:MM, 24h)
    21|- City + Country of birth (or latitude/longitude + timezone)
    22|
    23|**Steps:**
    24|1. Run the calculation script (see `scripts/natal_chart.py`):
    25|   ```
    26|   python3 ./scripts/natal_chart.py "Name" YYYY MM DD HH MM "City" "NationCode"
    27|   ```
    28|   Example: `python3 ./scripts/natal_chart.py "Alex" 1990 6 15 10 30 "Sao Paulo" "BR"`
    29|   
    30|   If GeoNames fails (common), pass coordinates directly:
    31|   ```
    32|   python3 ./scripts/natal_chart.py "Name" YYYY MM DD HH MM LAT LNG "Timezone"
    33|   ```
    34|   Example: `python3 ./scripts/natal_chart.py "Alex" 1990 6 15 10 30 -23.55 -46.63 "America/Sao_Paulo"`
    35|   
    36|   The script has fallback coordinates for: Sao Paulo, Rio de Janeiro, New York, Los Angeles, London, Paris, Tokyo, Berlin, Madrid, Mexico City, Buenos Aires, Sydney, Mumbai, Bangkok.
    37|2. The script outputs: all planet positions (sign + degree + house), house cusps, elements modalities summary, retrograde planets, and aspect list.
    38|3. Interpret the raw data using established astrological theory:
    39|   - **Sun sign** = core identity, ego, vitality
    40|   - **Moon sign** = emotional nature, instincts, inner self
    41|   - **Ascendant (Rising)** = outward personality, physical appearance, first impressions
    42|   - **Mercury** = communication style, thinking patterns
    43|   - **Venus** = love language, aesthetic preferences, values
    44|   - **Mars** = drive, aggression, sexuality, action style
    45|   - **Jupiter** = growth areas, luck, expansion, philosophy
    46|   - **Saturn** = restrictions, lessons, discipline, karma
    47|   - **Uranus/Neptune/Pluto** = generational influences, transformation
    48|   - **House placements** = life areas where energies manifest
    49|   - **Aspects** = how planetary energies interact (conjunction=blending, opposition=tension, trine=harmony, square=challenge, sextile=opportunity)
    50|4. Cite the specific planetary positions and aspects that justify each interpretation. Example: "With Moon in Pisces in the 7th House trine Venus, your emotional nature is deeply empathetic and seeks spiritual connection in partnerships."
    51|
    52|### 2. Daily Horoscope
    53|**Engine:** Ohmanda Horoscope API (free, no key required, live daily horoscopes).
    54|
    55|**Steps:**
    56|1. Fetch the horoscope:
    57|   ```
    58|   curl -sL "https://ohmanda.com/api/horoscope/{sign}"
    59|   ```
    60|   Valid signs: aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces
    61|2. The API returns: `{ "sign": "...", "date": "YYYY-MM-DD", "horoscope": "..." }`
    62|3. Present the horoscope text as-is (it's already professionally written), then add your own brief commentary connecting it to current planetary transits if relevant.
    63|
    64|### 3. Tarot Reading
    65|**Engine:** Structured tarot dataset embedded in `references/tarot_cards.json` — 78 cards (22 Major Arcana + 56 Minor Arcana) with traditional meanings (Rider-Waite-Smith system).
    66|
    67|**Spread types:**
    68|
    69|**Single Card Draw:**
    70|- Quick answer / daily guidance
    71|- Shuffle: pick a random card from the full 78
    72|- Present: card name, number, suit, upright meaning, reversed meaning
    73|- Ask user if they want to consider reversal
    74|
    75|**Three Card Spread (Past / Present / Future):**
    76|- Most versatile spread
    77|- Draw 3 cards without replacement
    78|- Interpret each in its position context
    79|
    80|**Celtic Cross (10 cards):**
    81|- For deep, comprehensive readings
    82|- Positions: 1=Present, 2=Challenge, 3=Foundation, 4=Past, 5=Outcome, 6=Near Future, 7=Self, 8=Environment, 9=Hopes/Fears, 10=Final Outcome
    83|- Draw 10 cards without replacement
    84|
    85|**Steps:**
    86|1. Read the tarot data: `cat ./references/tarot_cards.json`
    87|2. Use Python to draw random cards:
    88|   ```python
    89|   import json, random
    90|   cards = json.load(open('./references/tarot_cards.json'))
    91|   drawn = random.sample(cards, N)  # N = number of cards for the spread
    92|   ```
    93|3. For each card, present: name, position in spread, upright or reversed (50/50 chance), and the corresponding meaning from the dataset.
    94|4. Synthesize a reading that connects the cards into a coherent narrative, citing the specific traditional meanings.
    95|
    96|### 4. I Ching Divination
    97|**Engine:** `iching` Python package (v3.8.2) — implements the traditional Shicao (yarrow stalk) method from the Book of Changes.
    98|
    99|**Steps:**
   100|1. Run the I Ching script:
   101|   ```
   102|   python3 ./scripts/iching_reading.py "the user's question"
   103|   ```
   104|2. The script performs the coin-casting method and returns the hexagram number, name, Chinese character, and changing lines.
   105|3. Interpret using the I Ching text (the Judgment, Image, and changing line texts for the specific hexagram).
   106|4. If there are changing lines, also interpret the second (relating) hexagram.
   107|5. Reference the hexagram by its traditional name and number. Ground interpretation in the specific text, not generic wisdom.
   108|
   109|### 5. Numerology
   110|**Engine:** Pure Python calculation (Pythagorean system — the most widely used Western numerology method).
   111|
   112|**Calculations:**
   113|- **Life Path Number:** Sum of all digits in full birth date, reduced to single digit (except master numbers 11, 22, 33)
   114|  - Example: 1990-06-15 → 1+9+9+0+0+6+1+5 = 31 → 3+1 = 4
   115|- **Expression (Destiny) Number:** Full name converted to numbers (A=1, B=2... I=9, J=1...), summed and reduced
   116|- **Soul Urge (Heart's Desire):** Vowels only in full name
   117|- **Personality Number:** Consonants only in full name
   118|- **Birthday Number:** Day of birth reduced (15 → 1+5 = 6)
   119|- **Maturity Number:** Life Path + Expression, reduced
   120|
   121|**Steps:**
   122|1. Run: `python3 ./scripts/numerology.py "Full Name" YYYY MM DD`
   123|2. The script outputs all core numbers with their traditional meanings.
   124|3. Interpret each number using the standard Pythagorean meanings:
   125|   - 1=Leadership/Independence, 2=Cooperation/Sensitivity, 3=Creativity/Expression, 4=Stability/Work, 5=Freedom/Change, 6=Responsibility/Love, 7=Spirituality/Analysis, 8=Power/Material, 9=Humanitarian/Completion
   126|   - 11=Intuition/Illumination, 22=Master Builder, 33=Master Teacher
   127|
   128|### 6. Rune Casting
   129|**Engine:** Structured rune dataset in `references/runes_elder_futhark.json` — 24 Elder Futhark runes with traditional Norse/Icelandic meanings.
   130|
   131|**Casting methods:**
   132|- **Single Rune:** Quick guidance
   133|- **Three Rune Spread (Norn Spread):** Past (Urd) / Present (Verdandi) / Future (Skuld)
   134|- **Five Rune Cross:** Similar layout to Tarot Celtic Cross adapted for runes
   135|
   136|**Steps:**
   137|1. Read rune data: `cat ./references/runes_elder_futhark.json`
   138|2. Draw randomly, considering merkstave (reversed) position with ~30% probability
   139|3. Present: rune name, Anglo-Saxon rune poem excerpt, upright/reversed meaning
   140|4. Interpret within the Norse tradition framework — runes are oracular, not deterministic
   141|
   142|## General Interpretation Guidelines
   143|
   144|1. **Always cite your sources.** When interpreting a natal chart, reference the specific planet-sign-house combination. When reading tarot, reference the card's traditional meaning. When casting runes, reference the rune poem.
   145|
   146|2. **Be honest about limitations.** Astrology, tarot, I Ching, and runes are contemplative tools, not predictive instruments. Frame readings as "areas of focus" or "archetypal patterns," not as fortune-telling or medical/financial advice.
   147|
   148|3. **Synthesize, don't list.** A reading should tell a story, not enumerate data points. Connect the dots between different elements.
   149|
   150|4. **Respect the tradition.** Each system has its own internal logic:
   151|   - Western astrology: elements (fire/earth/air/water), modalities (cardinal/fixed/mutable), dignities (rulership/exaltation/detriment/fall)
   152|   - Tarot: RWS system with Major/Minor arcana, elemental associations (Wands=Fire, Cups=Water, Swords=Air, Pentacles=Earth)
   153|   - I Ching: yin/yang, the eight trigrams, the sequence of the King Wen arrangement
   154|   - Numerology: Pythagorean letter-number correspondence, core vs. cycle numbers
   155|   - Runes: Elder Futhark three aettir, rune poems as primary source
   156|
   157|5. **Language:** Respond in the user's preferred language (English or Spanish). Technical terms can be given in both languages (e.g., "Ascendente / Ascendant").
   158|
   159|## Pitfalls
   160|
   161|- **Kerykeion `.json()` returns a STRING, not a dict.** Always do `data = json.loads(raw) if isinstance(raw, str) else raw`. The natal_chart.py script handles this already.
   162|- **Kerykeion uses `nation` not `country`** as the keyword argument. Passing `country=` raises TypeError.
   163|- **Kerykeion requires GeoNames** for city lookup. The default shared username gets 401'd quickly. The script uses `zoltar_geonames` as fallback and has a CITY_COORDS dict for 14 major cities. If GeoNames fails, pass coordinates directly: `python3 natal_chart.py "Name" YYYY MM DD HH MM LAT LNG "Timezone"`. Users can get a free GeoNames username at https://www.geonames.org/login and set `KERYKEION_GEONAMES_USERNAME`.
   164|- **Ohmanda API** returns only daily horoscopes, no weekly/monthly. Don't try other endpoints — they 403. Only endpoint: `https://ohmanda.com/api/horoscope/{sign}`.
   165|- **I Ching `iching` PyPI package** — the module is NOT callable (`iching()` raises TypeError). Don't try `from iching import iching; oracle = iching()`. The custom `scripts/iching_reading.py` implements coin-casting independently with all 64 hexagram names.
   166|- **Tarot meanings** are from the Rider-Waite-Smith tradition. Don't mix in Thoth or Marseille system meanings without telling the user.
   167|- **Numerology** has multiple systems (Pythagorean, Chaldean, Kabbalah). This skill uses Pythagorean. If the user asks for Chaldean, calculate differently (Chaldean uses 1-8 not 1-9, and number assignments differ).
   168|- **Runes merkstave** (reversed) doesn't apply to all runes — some are symmetric and can't be reversed (Gebo, Hagalaz, Isa, Jera, Eihwaz, Sowilo, Ingwaz, Dagaz). The dataset marks these with `can_reverse: false`.
   169|- **NEVER give medical, financial, or legal advice** through divination. If someone asks "should I invest in X" or "will my illness cure," redirect: "Divination is a reflective tool, not a substitute for professional advice."
   170|
   171|## Data Sources
   172|
   173|See `references/api_research.md` for the full survey of free esoteric APIs, verified endpoints, and dead alternatives.
   174|