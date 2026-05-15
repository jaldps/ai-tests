     1|#!/usr/bin/env python3
     2|"""Natal chart calculator using Kerykeion (Swiss Ephemeris)."""
     3|import sys
     4|import json
     5|import warnings
     6|import os
     7|warnings.filterwarnings("ignore")
     8|os.environ.setdefault("KERYKEION_GEONAMES_USERNAME", "zoltar_geonames")
     9|
    10|# Common city coordinates fallback (when GeoNames is unavailable)
    11|CITY_COORDS = {
    12|    "sao paulo": {"lat": -23.5505, "lng": -46.6333, "tz": "America/Sao_Paulo", "nation": "BR"},
    13|    "rio de janeiro": {"lat": -22.9068, "lng": -43.1729, "tz": "America/Sao_Paulo", "nation": "BR"},
    14|    "new york": {"lat": 40.7128, "lng": -74.0060, "tz": "America/New_York", "nation": "US"},
    15|    "los angeles": {"lat": 34.0522, "lng": -118.2437, "tz": "America/Los_Angeles", "nation": "US"},
    16|    "london": {"lat": 51.5074, "lng": -0.1278, "tz": "Europe/London", "nation": "GB"},
    17|    "paris": {"lat": 48.8566, "lng": 2.3522, "tz": "Europe/Paris", "nation": "FR"},
    18|    "tokyo": {"lat": 35.6762, "lng": 139.6503, "tz": "Asia/Tokyo", "nation": "JP"},
    19|    "berlin": {"lat": 52.5200, "lng": 13.4050, "tz": "Europe/Berlin", "nation": "DE"},
    20|    "madrid": {"lat": 40.4168, "lng": -3.7038, "tz": "Europe/Madrid", "nation": "ES"},
    21|    "mexico city": {"lat": 19.4326, "lng": -99.1332, "tz": "America/Mexico_City", "nation": "MX"},
    22|    "buenos aires": {"lat": -34.6037, "lng": -58.3816, "tz": "America/Argentina/Buenos_Aires", "nation": "AR"},
    23|    "sydney": {"lat": -33.8688, "lng": 151.2093, "tz": "Australia/Sydney", "nation": "AU"},
    24|    "mumbai": {"lat": 19.0760, "lng": 72.8777, "tz": "Asia/Kolkata", "nation": "IN"},
    25|    "bangkok": {"lat": 13.7563, "lng": 100.5018, "tz": "Asia/Bangkok", "nation": "TH"},
    26|}
    27|
    28|def main():
    29|    if len(sys.argv) < 8:
    30|        print('Usage: natal_chart.py "Name" YYYY MM DD HH MM "City" "Nation"')
    31|        print('Example: natal_chart.py "Alex" 1990 6 15 10 30 "Sao Paulo" "BR"')
    32|        print("")
    33|        print("Alternatively, pass coordinates directly:")
    34|        print('natal_chart.py "Name" YYYY MM DD HH MM LAT LNG "Timezone"')
    35|        print('Example: natal_chart.py "Alex" 1990 6 15 10 30 -23.55 -46.63 "America/Sao_Paulo"')
    36|        sys.exit(1)
    37|    
    38|    name = sys.argv[1]
    39|    year = int(sys.argv[2])
    40|    month = int(sys.argv[3])
    41|    day = int(sys.argv[4])
    42|    hour = int(sys.argv[5])
    43|    minute = int(sys.argv[6])
    44|    
    45|    from kerykeion import AstrologicalSubject
    46|    
    47|    subject = None
    48|    
    49|    # Try coordinate mode first (8th arg is a number)
    50|    try:
    51|        lat = float(sys.argv[7])
    52|        lng = float(sys.argv[8])
    53|        tz_str = sys.argv[9] if len(sys.argv) > 9 else "UTC"
    54|        subject = AstrologicalSubject(
    55|            name, year, month, day, hour, minute,
    56|            city="Custom", nation="XX",
    57|            lat=lat, lng=lng, tz_str=tz_str,
    58|            geonames_username="zoltar_geonames"
    59|        )
    60|    except (ValueError, IndexError):
    61|        pass
    62|    
    63|    # Try city name mode
    64|    if subject is None:
    65|        city = sys.argv[7]
    66|        nation = sys.argv[8] if len(sys.argv) > 8 else "US"
    67|        city_key = city.lower().strip()
    68|        
    69|        # Try GeoNames first
    70|        try:
    71|            subject = AstrologicalSubject(
    72|                name, year, month, day, hour, minute, city=city, nation=nation,
    73|                geonames_username="zoltar_geonames"
    74|            )
    75|        except Exception:
    76|            # Fallback to known coordinates
    77|            if city_key in CITY_COORDS:
    78|                coords = CITY_COORDS[city_key]
    79|                subject = AstrologicalSubject(
    80|                    name, year, month, day, hour, minute,
    81|                    city=city, nation=coords["nation"],
    82|                    lat=coords["lat"], lng=coords["lng"],
    83|                    tz_str=coords["tz"],
    84|                    geonames_username="zoltar_geonames"
    85|                )
    86|            else:
    87|                print(json.dumps({"error": f"Cannot resolve city '{city}'. Try coordinates: natal_chart.py \"Name\" YYYY MM DD HH MM LAT LNG \"Timezone\""}))
    88|                sys.exit(1)
    89|    
    90|    raw = subject.json()
    91|    data = json.loads(raw) if isinstance(raw, str) else raw
    92|    
    93|    # Extract key info
    94|    output = {
    95|        "name": data["name"],
    96|        "birth_info": {
    97|            "date": data["iso_formatted_local_datetime"],
    98|            "city": data["city"],
    99|            "nation": data["nation"],
   100|            "coordinates": {"lat": data["lat"], "lng": data["lng"]},
   101|            "zodiac_type": data["zodiac_type"],
   102|            "houses_system": data["houses_system_name"],
   103|        },
   104|        "planets": {},
   105|        "houses": {},
   106|        "elements": {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0},
   107|        "modalities": {"Cardinal": 0, "Fixed": 0, "Mutable": 0},
   108|        "retrograde_planets": [],
   109|    }
   110|    
   111|    planet_keys = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
   112|    sign_names = {
   113|        "Ari": "Aries", "Tau": "Taurus", "Gem": "Gemini", "Can": "Cancer",
   114|        "Leo": "Leo", "Vir": "Virgo", "Lib": "Libra", "Sco": "Scorpio",
   115|        "Sag": "Sagittarius", "Cap": "Capricorn", "Aqu": "Aquarius", "Pis": "Pisces"
   116|    }
   117|    
   118|    for key in planet_keys:
   119|        p = data.get(key, {})
   120|        if not p:
   121|            continue
   122|        sign = p.get("sign", "?")
   123|        output["planets"][key] = {
   124|            "sign": sign_names.get(sign, sign),
   125|            "degree": round(p.get("position", 0), 2),
   126|            "house": p.get("house", "?"),
   127|            "element": p.get("element", "?"),
   128|            "quality": p.get("quality", "?"),
   129|            "retrograde": p.get("retrograde", False),
   130|        }
   131|        output["elements"][p.get("element", "?")] += 1
   132|        output["modalities"][p.get("quality", "?")] += 1
   133|        if p.get("retrograde"):
   134|            output["retrograde_planets"].append(key.capitalize())
   135|    
   136|    # Houses
   137|    for i, h in enumerate(data.get("houses", [])[:12], 1):
   138|        sign = h.get("sign", "?")
   139|        output["houses"][f"House_{i}"] = {
   140|            "sign": sign_names.get(sign, sign),
   141|            "degree": round(h.get("position", 0), 2),
   142|        }
   143|    
   144|    # Aspects (if available in the model)
   145|    if "aspects" in data:
   146|        output["aspects"] = []
   147|        for a in data["aspects"]:
   148|            output["aspects"].append({
   149|                "planet1": a.get("p1_name", "?"),
   150|                "aspect": a.get("aspect", "?"),
   151|                "planet2": a.get("p2_name", "?"),
   152|                "orb": round(a.get("orbit", 0), 1),
   153|            })
   154|    
   155|    # Ascendant from 1st house
   156|    first_house = data.get("first_house", data.get("houses", [{}])[0] if data.get("houses") else {})
   157|    if first_house:
   158|        asc_sign = first_house.get("sign", "?")
   159|        output["ascendant"] = {
   160|            "sign": sign_names.get(asc_sign, asc_sign),
   161|            "degree": round(first_house.get("position", 0), 2),
   162|        }
   163|    
   164|    print(json.dumps(output, indent=2))
   165|
   166|if __name__ == "__main__":
   167|    main()
   168|