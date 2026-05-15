     1|#!/usr/bin/env python3
     2|"""Pythagorean Numerology Calculator."""
     3|import sys
     4|import json
     5|
     6|# Pythagorean letter-number mapping
     7|LETTER_VALUES = {
     8|    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
     9|    'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
    10|    's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8,
    11|}
    12|
    13|VOWELS = set('aeiou')
    14|
    15|NUMBER_MEANINGS = {
    16|    1: "Leadership, Independence, Individuality, Initiative, Pioneering spirit",
    17|    2: "Cooperation, Sensitivity, Diplomacy, Balance, Partnership, Receptivity",
    18|    3: "Creativity, Self-Expression, Communication, Optimism, Joy, Sociability",
    19|    4: "Stability, Discipline, Work, Structure, Foundation, Practicality, Order",
    20|    5: "Freedom, Change, Adventure, Versatility, Curiosity, Sensory experience",
    21|    6: "Responsibility, Love, Nurturing, Harmony, Service, Domesticity, Healing",
    22|    7: "Spirituality, Analysis, Wisdom, Introspection, Research, Seeking truth",
    23|    8: "Power, Material mastery, Authority, Achievement, Business, Abundance",
    24|    9: "Humanitarianism, Completion, Compassion, Universal love, Selflessness",
    25|    11: "Master Intuitive, Illumination, Spiritual insight, Inspiration, Idealism",
    26|    22: "Master Builder, Visionary creation, Practical idealism, Great achievement",
    27|    33: "Master Teacher, Spiritual upliftment, Compassionate service, Healing mastery",
    28|}
    29|
    30|def reduce(n):
    31|    """Reduce to single digit, preserving master numbers."""
    32|    if n in (11, 22, 33):
    33|        return n
    34|    while n > 9:
    35|        n = sum(int(d) for d in str(n))
    36|        if n in (11, 22, 33):
    37|            return n
    38|    return n
    39|
    40|def name_to_number(name, filter_func=None):
    41|    """Convert name to number using Pythagorean system."""
    42|    total = 0
    43|    for ch in name.lower():
    44|        if ch.isalpha() and ch in LETTER_VALUES:
    45|            if filter_func is None or filter_func(ch):
    46|                total += LETTER_VALUES[ch]
    47|    return reduce(total)
    48|
    49|def main():
    50|    if len(sys.argv) < 5:
    51|        print('Usage: numerology.py "Full Name" YYYY MM DD')
    52|        print('Example: numerology.py "Alex Morgan" 1990 6 15')
    53|        sys.exit(1)
    54|    
    55|    full_name = sys.argv[1]
    56|    year = int(sys.argv[2])
    57|    month = int(sys.argv[3])
    58|    day = int(sys.argv[4])
    59|    
    60|    # Life Path Number
    61|    life_path = reduce(reduce(month) + reduce(day) + reduce(sum(int(d) for d in str(year))))
    62|    
    63|    # Expression (Destiny) Number — all letters
    64|    expression = name_to_number(full_name, filter_func=None)
    65|    
    66|    # Soul Urge (Heart's Desire) — vowels only
    67|    soul_urge = name_to_number(full_name, filter_func=lambda ch: ch in VOWELS)
    68|    
    69|    # Personality Number — consonants only
    70|    personality = name_to_number(full_name, filter_func=lambda ch: ch not in VOWELS and ch.isalpha())
    71|    
    72|    # Birthday Number
    73|    birthday_num = reduce(day)
    74|    
    75|    # Maturity Number
    76|    maturity = reduce(life_path + expression)
    77|    
    78|    # Pinnacle cycles (4 periods in life)
    79|    # 1st pinnacle: month + day reduced, 2nd: day + year, 3rd: 1st+2nd, 4th: month + year
    80|    p1 = reduce(reduce(month) + reduce(day))
    81|    p2 = reduce(reduce(day) + reduce(sum(int(d) for d in str(year))))
    82|    p3 = reduce(p1 + p2)
    83|    p4 = reduce(reduce(month) + reduce(sum(int(d) for d in str(year))))
    84|    
    85|    # Pinnacle ages (based on life path)
    86|    if life_path in (11, 22, 33):
    87|        base_age = 36 - (life_path % 9)
    88|    else:
    89|        base_age = 36 - life_path
    90|    
    91|    output = {
    92|        "full_name": full_name,
    93|        "birth_date": f"{year}-{month:02d}-{day:02d}",
    94|        "system": "Pythagorean",
    95|        "core_numbers": {
    96|            "life_path": {"number": life_path, "meaning": NUMBER_MEANINGS.get(life_path, "?")},
    97|            "expression": {"number": expression, "meaning": NUMBER_MEANINGS.get(expression, "?")},
    98|            "soul_urge": {"number": soul_urge, "meaning": NUMBER_MEANINGS.get(soul_urge, "?")},
    99|            "personality": {"number": personality, "meaning": NUMBER_MEANINGS.get(personality, "?")},
   100|            "birthday": {"number": birthday_num, "meaning": NUMBER_MEANINGS.get(birthday_num, "?")},
   101|            "maturity": {"number": maturity, "meaning": NUMBER_MEANINGS.get(maturity, "?")},
   102|        },
   103|        "pinnacle_cycles": {
   104|            "first": {"number": p1, "ages": f"0 to {base_age}", "meaning": NUMBER_MEANINGS.get(p1, "?")},
   105|            "second": {"number": p2, "ages": f"{base_age+1} to {base_age+9}", "meaning": NUMBER_MEANINGS.get(p2, "?")},
   106|            "third": {"number": p3, "ages": f"{base_age+10} to {base_age+18}", "meaning": NUMBER_MEANINGS.get(p3, "?")},
   107|            "fourth": {"number": p4, "ages": f"{base_age+19}+", "meaning": NUMBER_MEANINGS.get(p4, "?")},
   108|        },
   109|    }
   110|    
   111|    print(json.dumps(output, indent=2))
   112|
   113|if __name__ == "__main__":
   114|    main()
   115|