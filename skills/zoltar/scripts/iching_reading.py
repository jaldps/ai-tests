     1|#!/usr/bin/env python3
     2|"""I Ching reading using the iching Python package (coin method)."""
     3|import sys
     4|import json
     5|import random
     6|
     7|HEXAGRAM_NAMES = {
     8|    1: "The Creative (Qian)", 2: "The Receptive (Kun)", 3: "Difficulty at the Beginning (Zhun)",
     9|    4: "Youthful Folly (Meng)", 5: "Waiting (Xu)", 6: "Conflict (Song)",
    10|    7: "The Army (Shi)", 8: "Holding Together (Bi)", 9: "The Taming Power of the Small (Xiao Xu)",
    11|    10: "Treading (Li)", 11: "Peace (Tai)", 12: "Standstill (Pi)",
    12|    13: "Fellowship (Tong Ren)", 14: "Great Possession (Da You)", 15: "Modesty (Qian)",
    13|    16: "Enthusiasm (Yu)", 17: "Following (Sui)", 18: "Work on What Has Been Spoiled (Gu)",
    14|    19: "Approach (Lin)", 20: "Contemplation (Guan)", 21: "Biting Through (Shi He)",
    15|    22: "Grace (Bi)", 23: "Splitting Apart (Bo)", 24: "Return (Fu)",
    16|    25: "Innocence (Wu Wang)", 26: "The Taming Power of the Great (Da Xu)",
    17|    27: "Corners of the Mouth (Yi)", 28: "Preponderance of the Great (Da Guo)",
    18|    29: "The Abysmal Water (Kan)", 30: "The Clinging Fire (Li)",
    19|    31: "Influence (Xian)", 32: "Duration (Heng)", 33: "Retreat (Dun)",
    20|    34: "The Power of the Great (Da Zhuang)", 35: "Progress (Jin)",
    21|    36: "Darkening of the Light (Ming Yi)", 37: "The Family (Jia Ren)",
    22|    38: "Opposition (Kui)", 39: "Obstruction (Jian)", 40: "Deliverance (Jie)",
    23|    41: "Decrease (Sun)", 42: "Increase (Yi)", 43: "Breakthrough (Guai)",
    24|    44: "Coming to Meet (Gou)", 45: "Gathering Together (Cui)",
    25|    46: "Pushing Upward (Sheng)", 47: "Oppression (Kun)", 48: "The Well (Jing)",
    26|    49: "Revolution (Ge)", 50: "The Caldron (Ding)", 51: "The Arousing Thunder (Zhen)",
    27|    52: "Keeping Still Mountain (Gen)", 53: "Development (Jian)",
    28|    54: "The Marrying Maiden (Gui Mei)", 55: "Abundance (Feng)", 56: "The Wanderer (Lu)",
    29|    57: "The Gentle Wind (Xun)", 58: "The Joyous Lake (Dui)",
    30|    59: "Dispersion (Huan)", 60: "Limitation (Jie)", 61: "Inner Truth (Zhong Fu)",
    31|    62: "Preponderance of the Small (Xiao Guo)", 63: "After Completion (Ji Ji)",
    32|    64: "Before Completion (Wei Ji)"
    33|}
    34|
    35|TRIGRAMS = {
    36|    "yang_yang_yang": "Qian (Heaven/Creative)",
    37|    "yin_yin_yin": "Kun (Earth/Receptive)",
    38|    "yang_yang_yin": "Dui (Lake/Joyous)",
    39|    "yang_yin_yin": "Zhen (Thunder/Arousing)",
    40|    "yin_yang_yang": "Xun (Wind/Gentle)",
    41|    "yin_yin_yang": "Gen (Mountain/Keeping Still)",
    42|    "yang_yin_yang": "Li (Fire/Clinging)",
    43|    "yin_yang_yin": "Kan (Water/Abysmal)",
    44|}
    45|
    46|def cast_coins():
    47|    """Cast three coins to determine a line (coin method)."""
    48|    # Heads=3 (yang), Tails=2 (yin)
    49|    coins = [random.choice([2, 3]) for _ in range(3)]
    50|    total = sum(coins)
    51|    # 6=old yin (changing), 7=young yang, 8=young yin, 9=old yang (changing)
    52|    return total
    53|
    54|def cast_hexagram():
    55|    """Cast a full hexagram (6 lines, bottom to top)."""
    56|    lines = []
    57|    changing = []
    58|    for i in range(6):
    59|        value = cast_coins()
    60|        if value == 6:
    61|            lines.append("yin")
    62|            changing.append(i)  # old yin changes to yang
    63|        elif value == 7:
    64|            lines.append("yang")
    65|        elif value == 8:
    66|            lines.append("yin")
    67|        elif value == 9:
    68|            lines.append("yang")
    69|            changing.append(i)  # old yang changes to yin
    70|    return lines, changing
    71|
    72|def lines_to_number(lines):
    73|    """Convert 6 lines to hexagram number using binary encoding."""
    74|    # Bottom line is least significant bit
    75|    binary = 0
    76|    for i, line in enumerate(lines):
    77|        if line == "yang":
    78|            binary |= (1 << i)
    79|    return binary + 1  # 1-indexed
    80|
    81|def main():
    82|    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "general guidance"
    83|    
    84|    lines, changing = cast_hexagram()
    85|    hex_num = lines_to_number(lines)
    86|    
    87|    output = {
    88|        "question": question,
    89|        "hexagram_number": hex_num,
    90|        "hexagram_name": HEXAGRAM_NAMES.get(hex_num, f"Hexagram {hex_num}"),
    91|        "lines": lines,  # bottom to top
    92|        "changing_lines": changing,
    93|        "has_changing": len(changing) > 0,
    94|    }
    95|    
    96|    # If changing lines exist, calculate the relating hexagram
    97|    if changing:
    98|        new_lines = lines.copy()
    99|        for i in changing:
   100|            new_lines[i] = "yang" if new_lines[i] == "yin" else "yin"
   101|        relating_num = lines_to_number(new_lines)
   102|        output["relating_hexagram"] = {
   103|            "number": relating_num,
   104|            "name": HEXAGRAM_NAMES.get(relating_num, f"Hexagram {relating_num}"),
   105|        }
   106|        output["changing_line_positions"] = [i + 1 for i in changing]  # 1-indexed for humans
   107|    
   108|    print(json.dumps(output, indent=2))
   109|
   110|if __name__ == "__main__":
   111|    main()
   112|