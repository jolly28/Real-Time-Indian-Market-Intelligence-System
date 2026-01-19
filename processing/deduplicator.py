import hashlib

def deduplicate(records):
    seen = set()
    out = []
    for r in records:
        h = hashlib.md5(r["content"].encode("utf-8")).hexdigest()
        if h not in seen:
            seen.add(h)
            r["hash"] = h
            out.append(r)
    return out

