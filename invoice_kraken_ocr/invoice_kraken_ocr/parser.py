
import re

# Very simple Arabic-friendly parser:
# Examples:
# "فلتر زيت    2    150"   => name="فلتر زيت", qty=2, price=150
# "طلمبة ماء    1x250"     => name="طلمبة ماء", qty=1, rate=250
AR_LINE = re.compile(r'^(?P<name>.+?)\s+(?P<qty>\d+(?:[.,]\d+)?)\s*(?:x|×)?\s*(?P<rate>\d+(?:[.,]\d+)?)?$')

def parse_items(text: str):
    items = []
    for line in (text or "").splitlines():
        lt = line.strip()
        if not lt:
            continue
        m = AR_LINE.search(lt)
        if not m:
            continue
        d = m.groupdict()
        def f2(x):
            if not x: return None
            return float(x.replace(",","."))
        name = d.get("name") or lt
        qty = f2(d.get("qty")) or 1.0
        rate = f2(d.get("rate"))
        amount = rate * qty if (rate is not None) else None
        items.append({
            "line_text": lt,
            "name": name.strip(),
            "qty": qty,
            "rate": rate,
            "amount": amount,
        })
    return items
