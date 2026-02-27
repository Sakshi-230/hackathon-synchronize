titles = [
    "The Hindu", "Indian Express", "Times of India",
    "Samachar", "Hindustan Times", "Dainik Bhaskar", "Morning Herald"
]

banned = ['police','crime','corruption','cbi','cid','army','government',
          'govt','state','national','ministry','bureau','administration',
          'magistrate','defence']

periodic = ["daily","weekly","monthly","yearly"]

smap = {
    'B':'1','F':'1','P':'1','V':'1',
    'C':'2','G':'2','J':'2','K':'2','Q':'2','S':'2','X':'2','Z':'2',
    'D':'3','T':'3','L':'4','M':'5','N':'5','R':'6'
}
skip = set('AEIOUHY W')


def word_scrub(t):
    for w in t.lower().split():
        if w in banned:
            return False, f"Rejected: forbidden word '{w}'."
    return True, "Clean!"


def soundex(t):
    t = t.upper()
    code = t[0]
    for c in t[1:]:
        if c in skip:
            continue
        d = smap.get(c)
        if d and d != code[-1]:
            code += d
    return (code + "000")[:4]


def soundex_check(t):
    nc = soundex(t)
    for e in titles:
        if soundex(e) == nc:
            return False, f"Rejected: sounds like '{e}'."
    return True, "OK"


def combo_check(t):
    tl = t.lower()
    for w in tl.split():
        if w in periodic:
            for e in titles:
                if e.lower() in tl:
                    return False, f"Rejected: periodicity on '{e}'."
    matched = [e for e in titles if e.lower() in tl]
    if matched:
        return False, f"Rejected: combination of {matched}."
    return True, "Unique!"


def validate(t):
    print(f"\n  Checking: '{t}'")
    for fn in [word_scrub, soundex_check, combo_check]:
        ok, msg = fn(t)
        if not ok:
            print(f"  RESULT → {msg}")
            return
    titles.append(t)
    print(f"  RESULT → APPROVED! '{t}' registered.")


print("=== PRGI Title Validation System ===")
while True:
    t = input("\nEnter title (or 'quit' to exit): ").strip()
    if t.lower() == "quit":
        break
    if t:
        validate(t)
